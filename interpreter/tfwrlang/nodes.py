"""AST node types — one per construct the `language/` pages document, and nothing else.

Named `nodes`, not `ast`, so it never shadows the stdlib `ast` module inside the package.
"""

from .errors import TfwrSyntaxError


class Node:
    _fields = ()

    def __init__(self, *args, line=0):
        if len(args) != len(self._fields):
            raise TypeError(f"{type(self).__name__} expects {self._fields}, got {len(args)} args")
        for name, val in zip(self._fields, args):
            setattr(self, name, val)
        self.line = line

    def __repr__(self):
        inner = ", ".join(f"{f}={getattr(self, f)!r}" for f in self._fields)
        return f"{type(self).__name__}({inner})"

    def __eq__(self, other):
        return (
            type(self) is type(other)
            and all(getattr(self, f) == getattr(other, f) for f in self._fields)
        )


# -- Module ----------------------------------------------------------------------------------
class Module(Node):
    _fields = ("body",)


# -- Statements ------------------------------------------------------------------------------
class FunctionDef(Node):
    # params: list[str]; defaults: list[(str, expr)] for the trailing defaulted params
    _fields = ("name", "params", "defaults", "body")


class Return(Node):
    _fields = ("value",)  # expr or None


class If(Node):
    _fields = ("test", "body", "orelse")  # orelse: list of statements (possibly a single If for elif)


class While(Node):
    _fields = ("test", "body")


class For(Node):
    _fields = ("target", "iter", "body")


class Break(Node):
    _fields = ()


class Continue(Node):
    _fields = ()


class Pass(Node):
    _fields = ()


class Global(Node):
    _fields = ("names",)  # list[str]


class Import(Node):
    _fields = ("name",)  # str — the module/window name


class Assign(Node):
    _fields = ("targets", "value")  # targets: list of target exprs (chained a = b = v)


class AugAssign(Node):
    _fields = ("target", "op", "value")  # op: '+=' '-=' '*=' '/=' '%='


class ExprStmt(Node):
    _fields = ("value",)


# -- Expressions -----------------------------------------------------------------------------
class Num(Node):
    _fields = ("value",)  # python float


class Str(Node):
    _fields = ("value",)


class Const(Node):
    _fields = ("value",)  # True, False or None


class Name(Node):
    _fields = ("id",)


class Tuple(Node):
    _fields = ("elts",)


class List(Node):
    _fields = ("elts",)


class Dict(Node):
    _fields = ("keys", "values")


class Set(Node):
    _fields = ("elts",)


class BoolOp(Node):
    _fields = ("op", "left", "right")  # op: 'and' | 'or'


class UnaryOp(Node):
    _fields = ("op", "operand")  # op: 'not' | '-' | '+'


class BinOp(Node):
    _fields = ("op", "left", "right")  # + - * / // % **


class Compare(Node):
    _fields = ("op", "left", "right")  # == != < <= > >= in 'not in'


class Call(Node):
    _fields = ("func", "args")


class Subscript(Node):
    _fields = ("value", "index")


class Attribute(Node):
    _fields = ("value", "attr")


# -- helpers ---------------------------------------------------------------------------------

_TARGET_TYPES = (Name, Subscript, Attribute)


def as_target(expr):
    """Validate that an expression is assignable, returning it unchanged.

    Names, subscripts, attributes, and tuples of those are valid targets. Anything else — a
    number, a call, a literal list — is a syntax error, exactly as in Python.
    """
    if isinstance(expr, Tuple):
        for elt in expr.elts:
            as_target(elt)
        return expr
    if isinstance(expr, _TARGET_TYPES):
        return expr
    raise TfwrSyntaxError(
        f"cannot assign to {type(expr).__name__}", getattr(expr, "line", None)
    )
