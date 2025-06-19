from typing import Any, Protocol
from tokentype import Token

class ExprVisitor(Protocol):
    def visit_binary_expr(self, expr: "Binary") -> Any: ...
    def visit_grouping_expr(self, expr: "Grouping") -> Any: ...
    def visit_literal_expr(self, expr: "Literal") -> Any: ...
    def visit_unary_expr(self, expr: "Unary") -> Any: ...

class Expr:
    def accept(self, visitor: ExprVisitor) -> Any:
        raise NotImplementedError("Method accept() must be realized")

class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_binary_expr(self)

class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_grouping_expr(self)

class Literal(Expr):
    def __init__(self, value: Any):
        self.value = value

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_literal_expr(self)

class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_unary_expr(self)

