"""Tree-walking evaluator for the TFWR subset — the pure core, no game world.

Each behaviour here is one the `language/` pages already assert in prose. Where the official
sources are silent, this raises `Unspecified` (via the registry) instead of quietly taking
CPython's answer. Two examples that keep the corpus honest:

* **Truthiness is boolean-only.** operators.md never defines what a non-boolean means in a
  condition, so a non-bool in `if`/`while`/`and`/`or`/`not` raises `Unspecified('truthiness')`.
* **Ordering is numbers-only.** `< <= > >=` on non-numbers is a runtime error, per operators.md.

The world layer (`world.py` + `builtins.py`) adds the game verbs on top of this core.
"""

from . import nodes
from .errors import (
    NotSupported,
    Registry,
    TfwrNameError,
    TfwrRuntimeError,
    Unspecified,
)


# -- control-flow signals --------------------------------------------------------------------
class _Break(Exception):
    pass


class _Continue(Exception):
    pass


class _Return(Exception):
    def __init__(self, value):
        self.value = value


# -- runtime values --------------------------------------------------------------------------
class Function:
    """A user-defined function value. `def` binds one of these — `def f():` reads as
    `f = <a new function>`, exactly as functions.md says. It captures its defining environment,
    which is what makes the closure-factory pattern work."""

    def __init__(self, node, env, interp):
        self.node = node
        self.env = env
        self.interp = interp

    @property
    def name(self):
        return self.node.name

    def __call__(self, *args):
        return self.interp.call_function(self, list(args))

    def __repr__(self):
        return f"<function {self.node.name}>"


class Namespace:
    """A dotted constant group like `Entities` or `Items`, or an imported module."""

    def __init__(self, name, members):
        self.name = name
        self.members = members

    def get(self, attr):
        if attr not in self.members:
            raise TfwrRuntimeError(f"{self.name} has no member {attr!r}")
        return self.members[attr]

    def __repr__(self):
        return f"<namespace {self.name}>"


class Environment:
    """A lexical scope: a name→value map plus a link to the enclosing scope.

    Reading walks outward to the global scope (that's how a function reads `ws`). Writing lands
    locally unless the name was declared `global`."""

    def __init__(self, parent=None, global_env=None):
        self.vars = {}
        self.parent = parent
        self.global_env = global_env if global_env is not None else self
        self.global_names = set()

    def get(self, name):
        env = self
        while env is not None:
            if name in env.vars:
                return env.vars[name]
            env = env.parent
        raise TfwrNameError(
            f"name {name!r} is not defined (reading an unassigned name is a runtime error)"
        )

    def set(self, name, value):
        if name in self.global_names:
            self.global_env.vars[name] = value
        else:
            self.vars[name] = value

    def declare_global(self, name):
        self.global_names.add(name)


def _contains_call(node):
    """Whether an expression could have a side effect — used to decide when the short-circuit
    choice is actually observable."""
    if isinstance(node, nodes.Call):
        return True
    for field in node._fields:
        val = getattr(node, field)
        if isinstance(val, nodes.Node) and _contains_call(val):
            return True
        if isinstance(val, list):
            for item in val:
                if isinstance(item, nodes.Node) and _contains_call(item):
                    return True
                if isinstance(item, tuple):  # (name, default) pairs
                    for sub in item:
                        if isinstance(sub, nodes.Node) and _contains_call(sub):
                            return True
    return False


def tfwr_str(value):
    """String form used by `str()` and `print`. Whole floats render without a trailing `.0`
    (`3.0` -> `"3"`), matching how the game shows integral values. This is a modelling choice —
    the docs don't pin down formatting — kept small and local on purpose."""
    if isinstance(value, bool):
        return "True" if value else "False"
    if value is None:
        return "None"
    if isinstance(value, float):
        return str(int(value)) if value.is_integer() else repr(value)
    if isinstance(value, str):
        return value
    if isinstance(value, tuple):
        return "(" + ", ".join(tfwr_str(v) for v in value) + ")"
    return str(value)


class Interpreter:
    def __init__(self, extra_builtins=None, registry=None, max_call_depth=None,
                 max_loop_iterations=None):
        self.registry = registry if registry is not None else Registry()
        self.max_call_depth = max_call_depth  # None => the game's limit is Unspecified
        # A test-suite guard, NOT a game behaviour: the real game imposes no iteration cap (it
        # slows each tick instead), so this defaults to None. Tests set it so that a regression
        # which breaks `break`/loop-exit fails fast instead of hanging CI. Not an Unspecified
        # topic — it models nothing the docs leave open, it only bounds a runaway test.
        self.max_loop_iterations = max_loop_iterations
        self.depth = 0
        self.output = []
        self.global_env = Environment()
        self.builtins = {}
        self._install_pure_builtins()
        if extra_builtins:
            self.builtins.update(extra_builtins)

    # -- public API --------------------------------------------------------------------------
    def run(self, module):
        for stmt in module.body:
            self.exec_stmt(stmt, self.global_env)

    def run_source(self, src, filename="<tfwr>"):
        from .parser import parse
        self.run(parse(src, filename))

    # -- statements --------------------------------------------------------------------------
    def exec_stmt(self, node, env):
        getattr(self, "exec_" + type(node).__name__)(node, env)

    def exec_block(self, body, env):
        for stmt in body:
            self.exec_stmt(stmt, env)

    def exec_ExprStmt(self, node, env):
        self.eval(node.value, env)

    def exec_Pass(self, node, env):
        pass

    def exec_Assign(self, node, env):
        value = self.eval(node.value, env)
        for target in node.targets:
            self.assign(target, value, env)

    def exec_AugAssign(self, node, env):
        target = node.target
        if isinstance(target, nodes.Subscript):
            # Evaluate container and index once: `a[f()] += 1` must call f() a single time.
            obj = self.eval(target.value, env)
            key = self.eval(target.index, env)
            target = nodes.Subscript(nodes.Const(obj), nodes.Const(key), line=target.line)
        current = self.eval(target, env)
        rhs = self.eval(node.value, env)
        result = self.binary_op(node.op[:-1], current, rhs, node)
        self.assign(target, result, env)

    def exec_Global(self, node, env):
        for name in node.names:
            env.declare_global(name)

    def exec_FunctionDef(self, node, env):
        env.set(node.name, Function(node, env, self))

    def exec_Return(self, node, env):
        raise _Return(self.eval(node.value, env) if node.value is not None else None)

    def exec_Break(self, node, env):
        raise _Break()

    def exec_Continue(self, node, env):
        raise _Continue()

    def exec_If(self, node, env):
        if self.as_bool(self.eval(node.test, env), node):
            self.exec_block(node.body, env)
        else:
            self.exec_block(node.orelse, env)

    def exec_While(self, node, env):
        iterations = 0
        while self.as_bool(self.eval(node.test, env), node):
            iterations = self._tick_loop(iterations)
            try:
                self.exec_block(node.body, env)
            except _Break:
                break
            except _Continue:
                continue

    def exec_For(self, node, env):
        iterations = 0
        for item in self.iterate(self.eval(node.iter, env), node):
            iterations = self._tick_loop(iterations)
            self.assign(node.target, item, env)
            try:
                self.exec_block(node.body, env)
            except _Break:
                break
            except _Continue:
                continue

    def _tick_loop(self, iterations):
        iterations += 1
        if self.max_loop_iterations is not None and iterations > self.max_loop_iterations:
            raise TfwrRuntimeError(
                f"loop iteration budget ({self.max_loop_iterations}) exceeded"
            )
        return iterations

    def exec_Import(self, node, env):
        self.registry.raise_(
            "module-by-window-name",
            f"import {node.name}",
        )

    # -- assignment --------------------------------------------------------------------------
    def assign(self, target, value, env):
        if isinstance(target, nodes.Name):
            env.set(target.id, value)
        elif isinstance(target, nodes.Subscript):
            obj = self.eval(target.value, env)
            key = self.eval(target.index, env)
            if isinstance(obj, tuple):
                raise TfwrRuntimeError("tuples are immutable and cannot be changed after creation")
            if isinstance(obj, (list, dict)):
                if isinstance(obj, list):
                    key = self._as_index(key)
                obj[key] = value
            else:
                raise TfwrRuntimeError(f"cannot assign into {type(obj).__name__}")
        elif isinstance(target, nodes.Tuple):
            items = list(self.iterate(value, target))
            if len(items) != len(target.elts):
                raise TfwrRuntimeError(
                    f"cannot unpack {len(items)} values into {len(target.elts)} targets"
                )
            for sub, item in zip(target.elts, items):
                self.assign(sub, item, env)
        elif isinstance(target, nodes.Attribute):
            raise NotSupported("assigning to an attribute is not part of the documented subset")
        else:
            raise TfwrRuntimeError(f"cannot assign to {type(target).__name__}")

    # -- expressions -------------------------------------------------------------------------
    def eval(self, node, env):
        return getattr(self, "eval_" + type(node).__name__)(node, env)

    def eval_Num(self, node, env):
        return node.value

    def eval_Str(self, node, env):
        return node.value

    def eval_Const(self, node, env):
        return node.value

    def eval_Name(self, node, env):
        try:
            return env.get(node.id)
        except TfwrNameError:
            if node.id in self.builtins:
                return self.builtins[node.id]
            raise

    def eval_Tuple(self, node, env):
        return tuple(self.eval(e, env) for e in node.elts)

    def eval_List(self, node, env):
        return [self.eval(e, env) for e in node.elts]

    def eval_Set(self, node, env):
        return set(self.eval(e, env) for e in node.elts)

    def eval_Dict(self, node, env):
        return {self.eval(k, env): self.eval(v, env) for k, v in zip(node.keys, node.values)}

    def eval_BoolOp(self, node, env):
        left = self.as_bool(self.eval(node.left, env), node)
        if node.op == "and":
            if not left:
                if _contains_call(node.right):
                    self.registry.record("boolean-short-circuit", "skipped right of 'and'")
                return False
            return self.as_bool(self.eval(node.right, env), node)
        else:  # or
            if left:
                if _contains_call(node.right):
                    self.registry.record("boolean-short-circuit", "skipped right of 'or'")
                return True
            return self.as_bool(self.eval(node.right, env), node)

    def eval_UnaryOp(self, node, env):
        val = self.eval(node.operand, env)
        if node.op == "not":
            return not self.as_bool(val, node)
        if not isinstance(val, float):
            raise TfwrRuntimeError(f"unary {node.op!r} needs a number, got {type(val).__name__}")
        return -val if node.op == "-" else +val

    def eval_BinOp(self, node, env):
        return self.binary_op(node.op, self.eval(node.left, env), self.eval(node.right, env), node)

    def eval_Compare(self, node, env):
        left = self.eval(node.left, env)
        right = self.eval(node.right, env)
        op = node.op
        if op == "==":
            return left == right
        if op == "!=":
            return left != right
        if op == "in":
            return self._member(left, right)
        if op == "not in":
            return not self._member(left, right)
        # ordering: numbers only
        if not (isinstance(left, float) and isinstance(right, float)):
            raise TfwrRuntimeError("ordering (< <= > >=) is defined on numbers only")
        return {"<": left < right, "<=": left <= right, ">": left > right, ">=": left >= right}[op]

    def eval_Call(self, node, env):
        if isinstance(node.func, nodes.Attribute):
            obj = self.eval(node.func.value, env)
            args = [self.eval(a, env) for a in node.args]
            if isinstance(obj, (list, dict, set)):
                return self.call_method(obj, node.func.attr, args, node)
            if isinstance(obj, Namespace):
                return self.invoke(obj.get(node.func.attr), args, node)
            raise TfwrRuntimeError(f"cannot call method on {type(obj).__name__}")
        func = self.eval(node.func, env)
        args = [self.eval(a, env) for a in node.args]
        return self.invoke(func, args, node)

    def eval_Subscript(self, node, env):
        obj = self.eval(node.value, env)
        key = self.eval(node.index, env)
        if isinstance(obj, (list, tuple, str)):
            try:
                return obj[self._as_index(key)]
            except IndexError:
                raise TfwrRuntimeError("index out of range")
        if isinstance(obj, dict):
            if key not in obj:
                raise TfwrRuntimeError(f"key {tfwr_str(key)} not in dictionary")
            return obj[key]
        raise TfwrRuntimeError(f"{type(obj).__name__} is not subscriptable")

    def eval_Attribute(self, node, env):
        obj = self.eval(node.value, env)
        if isinstance(obj, Namespace):
            return obj.get(node.attr)
        raise TfwrRuntimeError(f"{type(obj).__name__} has no attribute {node.attr!r}")

    # -- operators ---------------------------------------------------------------------------
    def binary_op(self, op, a, b, node):
        if op == "+":
            if isinstance(a, float) and isinstance(b, float):
                return a + b
            if isinstance(a, str) and isinstance(b, str):
                return a + b
            if isinstance(a, list) and isinstance(b, list):
                return a + b
            raise TfwrRuntimeError(f"cannot add {type(a).__name__} and {type(b).__name__}")
        if not (isinstance(a, float) and isinstance(b, float)):
            raise TfwrRuntimeError(
                f"arithmetic {op!r} needs numbers, got {type(a).__name__} and {type(b).__name__}"
            )
        try:
            if op == "-":
                return a - b
            if op == "*":
                return a * b
            if op == "/":
                return a / b
            if op == "//":
                return float(a // b)
            if op == "%":
                return a % b
            if op == "**":
                return float(a ** b)
        except ZeroDivisionError:
            raise TfwrRuntimeError("division by zero")
        raise TfwrRuntimeError(f"unknown operator {op!r}")

    # -- calls -------------------------------------------------------------------------------
    def invoke(self, func, args, node):
        if isinstance(func, Function):
            return self.call_function(func, args)
        if callable(func):
            return func(*args)
        raise TfwrRuntimeError(f"{type(func).__name__} is not callable")

    def call_function(self, func, args):
        node = func.node
        params, defaults = node.params, node.defaults
        required = len(params) - len(defaults)
        if len(args) < required or len(args) > len(params):
            raise TfwrRuntimeError(
                f"{node.name}() takes {required}..{len(params)} args, got {len(args)}"
            )
        self.depth += 1
        if self.max_call_depth is not None and self.depth > self.max_call_depth:
            self.depth -= 1
            raise TfwrRuntimeError(
                f"call stack limit ({self.max_call_depth}) exceeded"
            )
        try:
            frame = Environment(parent=func.env, global_env=self.global_env)
            for i, pname in enumerate(params):
                if i < len(args):
                    frame.vars[pname] = args[i]
                else:
                    _, default_expr = defaults[i - required]
                    self.registry.record("default-arg-eval-time", f"{node.name}.{pname}")
                    frame.vars[pname] = self.eval(default_expr, frame)
            try:
                self.exec_block(node.body, frame)
            except _Return as r:
                return r.value
            return None
        finally:
            self.depth -= 1

    def call_method(self, obj, method, args, node):
        table = self._method_tables.get(type(obj))
        impl = table.get(method) if table else None
        if impl is None:
            raise NotSupported(
                f"{type(obj).__name__}.{method}() is not a documented collection method"
            )
        return impl(self, obj, args)

    # -- helpers -----------------------------------------------------------------------------
    def as_bool(self, value, node):
        if isinstance(value, bool):
            return value
        self.registry.raise_(
            "truthiness",
            f"non-boolean {tfwr_str(value)} ({type(value).__name__}) used in boolean context",
        )

    def iterate(self, value, node):
        if isinstance(value, dict):
            return list(value.keys())
        if isinstance(value, (list, tuple, set, str)):
            return list(value)
        raise TfwrRuntimeError(f"{type(value).__name__} is not iterable")

    def _member(self, item, container):
        if isinstance(container, (list, tuple, set, str, dict)):
            return item in container
        raise TfwrRuntimeError(f"'in' needs a collection, got {type(container).__name__}")

    def _as_index(self, key):
        if isinstance(key, bool) or not isinstance(key, float):
            raise TfwrRuntimeError(f"list index must be a number, got {type(key).__name__}")
        return int(key)

    # -- pure built-ins ----------------------------------------------------------------------
    def _install_pure_builtins(self):
        def _range(*a):
            ints = [int(x) for x in a]
            return [float(i) for i in range(*ints)]

        def _len(x):
            return float(len(x))

        def _min(*a):
            return min(a[0]) if len(a) == 1 else min(a)

        def _max(*a):
            return max(a[0]) if len(a) == 1 else max(a)

        def _abs(x):
            return abs(x)

        def _print(*a):
            self.output.append(" ".join(tfwr_str(x) for x in a))

        self.builtins.update({
            "range": _range,
            "len": _len,
            "str": tfwr_str,
            "min": _min,
            "max": _max,
            "abs": _abs,
            "print": _print,
            "quick_print": _print,  # same output; the cost difference lives in the world layer
        })

    # collection methods, keyed by python type -----------------------------------------------
    def _m_append(self, obj, args):
        obj.append(args[0]); return None

    def _m_insert(self, obj, args):
        obj.insert(self._as_index(args[0]), args[1]); return None

    def _m_pop(self, obj, args):
        if isinstance(obj, dict):
            key = args[0]
            if key not in obj:
                raise TfwrRuntimeError(f"key {tfwr_str(key)} not in dictionary")
            return obj.pop(key)
        if args:
            try:
                return obj.pop(self._as_index(args[0]))
            except IndexError:
                raise TfwrRuntimeError("pop index out of range")
        if not obj:
            raise TfwrRuntimeError("pop from empty list")
        return obj.pop()

    def _m_remove(self, obj, args):
        try:
            obj.remove(args[0])
        except (ValueError, KeyError):
            raise TfwrRuntimeError(f"{tfwr_str(args[0])} not present to remove")
        return None

    def _m_add(self, obj, args):
        obj.add(args[0]); return None


Interpreter._method_tables = {
    list: {
        "append": Interpreter._m_append,
        "insert": Interpreter._m_insert,
        "pop": Interpreter._m_pop,
        "remove": Interpreter._m_remove,
    },
    dict: {"pop": Interpreter._m_pop},
    set: {"add": Interpreter._m_add, "remove": Interpreter._m_remove},
}
