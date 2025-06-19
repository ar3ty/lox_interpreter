from typing import Any, Protocol
from tokentype import Token
from expr import Expr

class StmtVisitor(Protocol):
    def visit_expression_stmt(self, stmt: "Expression") -> Any: ...
    def visit_print_stmt(self, stmt: "Print") -> Any: ...

class Stmt:
    def accept(self, visitor: StmtVisitor) -> Any:
        raise NotImplementedError("Method accept() must be realized")

class Expression(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_expression_stmt(self)

class Print(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_print_stmt(self)

