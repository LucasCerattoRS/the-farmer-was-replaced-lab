"""Recursive-descent parser for the TFWR subset.

The precedence table is the one on `language/operators.md` (itself derived from the official
`operators.md`): `or` < `and` < `not` < comparisons < `+ -` < `* / // %` < unary < `**`, with
`**` right-associative. Nothing here invents syntax the `language/` pages don't describe; a
construct outside that subset should fail to parse rather than be silently accepted.
"""

from . import nodes
from .errors import NotSupported, TfwrSyntaxError
from .lexer import tokenize

KEYWORDS = {
    "def", "return", "if", "elif", "else", "while", "for", "in", "break", "continue",
    "pass", "global", "import", "and", "or", "not", "True", "False", "None",
}
_COMPARE_OPS = {"==", "!=", "<", "<=", ">", ">="}
_AUGASSIGN = {"+=", "-=", "*=", "/=", "%="}
_ADD_OPS = {"+", "-"}
_MUL_OPS = {"*", "/", "//", "%"}


class Parser:
    def __init__(self, tokens, filename="<tfwr>"):
        self.toks = tokens
        self.pos = 0
        self.filename = filename

    # -- cursor helpers ----------------------------------------------------------------------
    @property
    def cur(self):
        return self.toks[self.pos]

    def advance(self):
        t = self.toks[self.pos]
        self.pos += 1
        return t

    def is_op(self, *vals):
        t = self.cur
        return t.type == "OP" and t.value in vals

    def is_kw(self, *vals):
        t = self.cur
        return t.type == "NAME" and t.value in vals

    def expect_op(self, val):
        if not self.is_op(val):
            self._err(f"expected {val!r}")
        return self.advance()

    def expect_type(self, typ):
        if self.cur.type != typ:
            self._err(f"expected {typ}")
        return self.advance()

    def _err(self, msg):
        t = self.cur
        got = t.value if t.value else t.type
        raise TfwrSyntaxError(f"{msg}, got {got!r}", t.line, t.col)

    # -- entry -------------------------------------------------------------------------------
    def parse_module(self):
        body = []
        while self.cur.type != "ENDMARKER":
            if self.cur.type == "NEWLINE":
                self.advance()
                continue
            body.append(self.parse_statement())
        return nodes.Module(body)

    # -- statements --------------------------------------------------------------------------
    def parse_statement(self):
        if self.is_kw("def"):
            return self.parse_funcdef()
        if self.is_kw("if"):
            return self.parse_if()
        if self.is_kw("while"):
            return self.parse_while()
        if self.is_kw("for"):
            return self.parse_for()
        stmt = self.parse_simple_stmt()
        self.expect_type("NEWLINE")
        return stmt

    def parse_simple_stmt(self):
        line = self.cur.line
        if self.is_kw("return"):
            self.advance()
            if self.cur.type == "NEWLINE" or self.is_op(";"):
                return nodes.Return(None, line=line)
            return nodes.Return(self.parse_testlist(), line=line)
        if self.is_kw("pass"):
            self.advance()
            return nodes.Pass(line=line)
        if self.is_kw("break"):
            self.advance()
            return nodes.Break(line=line)
        if self.is_kw("continue"):
            self.advance()
            return nodes.Continue(line=line)
        if self.is_kw("global"):
            self.advance()
            names = [self.expect_type("NAME").value]
            while self.is_op(","):
                self.advance()
                names.append(self.expect_type("NAME").value)
            return nodes.Global(names, line=line)
        if self.is_kw("import"):
            self.advance()
            return nodes.Import(self.expect_type("NAME").value, line=line)
        return self.parse_expr_or_assign()

    def parse_expr_or_assign(self):
        line = self.cur.line
        first = self.parse_testlist()
        if self.is_op("="):
            chain = [first]
            while self.is_op("="):
                self.advance()
                chain.append(self.parse_testlist())
            *targets, value = chain
            return nodes.Assign([nodes.as_target(t) for t in targets], value, line=line)
        if self.cur.type == "OP" and self.cur.value in _AUGASSIGN:
            op = self.advance().value
            value = self.parse_testlist()
            return nodes.AugAssign(nodes.as_target(first), op, value, line=line)
        return nodes.ExprStmt(first, line=line)

    def parse_funcdef(self):
        line = self.advance().line  # 'def'
        name = self.expect_type("NAME").value
        self.expect_op("(")
        params, defaults = [], []
        if not self.is_op(")"):
            self._parse_param(params, defaults)
            while self.is_op(","):
                self.advance()
                if self.is_op(")"):
                    break
                self._parse_param(params, defaults)
        self.expect_op(")")
        body = self.parse_suite()
        return nodes.FunctionDef(name, params, defaults, body, line=line)

    def _parse_param(self, params, defaults):
        pname = self.expect_type("NAME").value
        params.append(pname)
        if self.is_op("="):
            self.advance()
            defaults.append((pname, self.parse_expr()))
        elif defaults:
            self._err("non-default parameter follows a default parameter")

    def parse_if(self):
        line = self.advance().line  # 'if'
        test = self.parse_expr()
        body = self.parse_suite()
        orelse = self._parse_elif_else()
        return nodes.If(test, body, orelse, line=line)

    def _parse_elif_else(self):
        if self.is_kw("elif"):
            line = self.advance().line
            test = self.parse_expr()
            body = self.parse_suite()
            return [nodes.If(test, body, self._parse_elif_else(), line=line)]
        if self.is_kw("else"):
            self.advance()
            return self.parse_suite()
        return []

    def parse_while(self):
        line = self.advance().line
        test = self.parse_expr()
        body = self.parse_suite()
        return nodes.While(test, body, line=line)

    def parse_for(self):
        line = self.advance().line  # 'for'
        target = nodes.as_target(self.parse_target_list())
        if not self.is_kw("in"):
            self._err("expected 'in' in for statement")
        self.advance()
        it = self.parse_testlist()
        body = self.parse_suite()
        return nodes.For(target, it, body, line=line)

    def parse_target_list(self):
        first = self.parse_postfix()
        if not self.is_op(","):
            return first
        elts = [first]
        while self.is_op(","):
            self.advance()
            if self.is_kw("in"):
                break
            elts.append(self.parse_postfix())
        return nodes.Tuple(elts)

    def parse_suite(self):
        self.expect_op(":")
        if self.cur.type == "NEWLINE":
            self.advance()
            self.expect_type("INDENT")
            body = []
            while self.cur.type != "DEDENT":
                if self.cur.type == "NEWLINE":
                    self.advance()
                    continue
                body.append(self.parse_statement())
            self.expect_type("DEDENT")
            if not body:
                self._err("empty block")
            return body
        # inline suite: one or more simple statements, ';'-separated
        body = [self.parse_simple_stmt()]
        while self.is_op(";"):
            self.advance()
            if self.cur.type == "NEWLINE":
                break
            body.append(self.parse_simple_stmt())
        self.expect_type("NEWLINE")
        return body

    # -- expressions -------------------------------------------------------------------------
    def parse_testlist(self):
        first = self.parse_expr()
        if not self.is_op(","):
            return first
        elts = [first]
        while self.is_op(","):
            self.advance()
            if self._at_expr_end():
                break
            elts.append(self.parse_expr())
        return nodes.Tuple(elts, line=first.line)

    def _at_expr_end(self):
        return self.cur.type in ("NEWLINE", "ENDMARKER") or self.is_op(")", "]", "}", "=", ":", ";")

    def parse_expr(self):
        return self.parse_or()

    def parse_or(self):
        left = self.parse_and()
        while self.is_kw("or"):
            line = self.advance().line
            left = nodes.BoolOp("or", left, self.parse_and(), line=line)
        return left

    def parse_and(self):
        left = self.parse_not()
        while self.is_kw("and"):
            line = self.advance().line
            left = nodes.BoolOp("and", left, self.parse_not(), line=line)
        return left

    def parse_not(self):
        if self.is_kw("not"):
            line = self.advance().line
            return nodes.UnaryOp("not", self.parse_not(), line=line)
        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_arith()
        while True:
            if self.cur.type == "OP" and self.cur.value in _COMPARE_OPS:
                op = self.advance().value
                left = nodes.Compare(op, left, self.parse_arith(), line=left.line)
            elif self.is_kw("in"):
                self.advance()
                left = nodes.Compare("in", left, self.parse_arith(), line=left.line)
            elif self.is_kw("not"):
                # only valid as 'not in'
                if self.toks[self.pos + 1].type == "NAME" and self.toks[self.pos + 1].value == "in":
                    self.advance()
                    self.advance()
                    left = nodes.Compare("not in", left, self.parse_arith(), line=left.line)
                else:
                    break
            else:
                break
        return left

    def parse_arith(self):
        left = self.parse_term()
        while self.cur.type == "OP" and self.cur.value in _ADD_OPS:
            op = self.advance().value
            left = nodes.BinOp(op, left, self.parse_term(), line=left.line)
        return left

    def parse_term(self):
        left = self.parse_unary()
        while self.cur.type == "OP" and self.cur.value in _MUL_OPS:
            op = self.advance().value
            left = nodes.BinOp(op, left, self.parse_unary(), line=left.line)
        return left

    def parse_unary(self):
        if self.cur.type == "OP" and self.cur.value in ("-", "+"):
            op = self.advance()
            return nodes.UnaryOp(op.value, self.parse_unary(), line=op.line)
        return self.parse_power()

    def parse_power(self):
        base = self.parse_postfix()
        if self.is_op("**"):
            line = self.advance().line
            return nodes.BinOp("**", base, self.parse_unary(), line=line)
        return base

    def parse_postfix(self):
        node = self.parse_atom()
        while True:
            if self.is_op("("):
                self.advance()
                args = self._parse_call_args()
                self.expect_op(")")
                node = nodes.Call(node, args, line=node.line)
            elif self.is_op("["):
                self.advance()
                if self.is_op(":"):
                    raise NotSupported("slicing (a[i:j]) is not part of the documented subset")
                index = self.parse_expr()
                if self.is_op(":"):
                    raise NotSupported("slicing (a[i:j]) is not part of the documented subset")
                self.expect_op("]")
                node = nodes.Subscript(node, index, line=node.line)
            elif self.is_op("."):
                self.advance()
                attr = self.expect_type("NAME").value
                node = nodes.Attribute(node, attr, line=node.line)
            else:
                return node

    def _parse_call_args(self):
        args = []
        if self.is_op(")"):
            return args
        args.append(self.parse_expr())
        while self.is_op(","):
            self.advance()
            if self.is_op(")"):
                break
            args.append(self.parse_expr())
        return args

    def parse_atom(self):
        t = self.cur
        if t.type == "NUMBER":
            self.advance()
            return nodes.Num(float(t.value), line=t.line)
        if t.type == "STRING":
            self.advance()
            return nodes.Str(t.value, line=t.line)
        if t.type == "NAME":
            if t.value in ("True", "False", "None"):
                self.advance()
                return nodes.Const({"True": True, "False": False, "None": None}[t.value], line=t.line)
            if t.value in KEYWORDS:
                self._err(f"unexpected keyword {t.value!r}")
            self.advance()
            return nodes.Name(t.value, line=t.line)
        if self.is_op("("):
            return self._parse_paren()
        if self.is_op("["):
            return self._parse_list()
        if self.is_op("{"):
            return self._parse_brace()
        self._err("expected an expression")

    def _parse_paren(self):
        line = self.advance().line  # '('
        if self.is_op(")"):
            self.advance()
            return nodes.Tuple([], line=line)
        inner = self.parse_testlist()
        self.expect_op(")")
        return inner  # grouping, or a Tuple built by parse_testlist

    def _parse_list(self):
        line = self.advance().line  # '['
        elts = []
        if not self.is_op("]"):
            elts.append(self.parse_expr())
            while self.is_op(","):
                self.advance()
                if self.is_op("]"):
                    break
                elts.append(self.parse_expr())
        self.expect_op("]")
        return nodes.List(elts, line=line)

    def _parse_brace(self):
        line = self.advance().line  # '{'
        if self.is_op("}"):
            self.advance()
            return nodes.Dict([], [], line=line)  # {} is an empty dict
        first = self.parse_expr()
        if self.is_op(":"):
            self.advance()
            keys = [first]
            values = [self.parse_expr()]
            while self.is_op(","):
                self.advance()
                if self.is_op("}"):
                    break
                keys.append(self.parse_expr())
                self.expect_op(":")
                values.append(self.parse_expr())
            self.expect_op("}")
            return nodes.Dict(keys, values, line=line)
        elts = [first]
        while self.is_op(","):
            self.advance()
            if self.is_op("}"):
                break
            elts.append(self.parse_expr())
        self.expect_op("}")
        return nodes.Set(elts, line=line)


def parse(src, filename="<tfwr>"):
    """Parse TFWR source into a `Module` node."""
    return Parser(tokenize(src), filename).parse_module()
