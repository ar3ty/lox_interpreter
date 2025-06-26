from typing import Any, Protocol
from tokentype import Token

class ExprVisitor(Protocol):
    def visit_assign_expr(self, expr: "ExprAssign") -> Any: ...
    def visit_binary_expr(self, expr: "ExprBinary") -> Any: ...
    def visit_call_expr(self, expr: "ExprCall") -> Any: ...
    def visit_grouping_expr(self, expr: "ExprGrouping") -> Any: ...
    def visit_literal_expr(self, expr: "ExprLiteral") -> Any: ...
    def visit_logical_expr(self, expr: "ExprLogical") -> Any: ...
    def visit_unary_expr(self, expr: "ExprUnary") -> Any: ...
    def visit_variable_expr(self, expr: "ExprVariable") -> Any: ...

class Expr:
    def accept(self, visitor: ExprVisitor) -> Any:
        raise NotImplementedError("Method accept() must be realized")

class ExprAssign(Expr):
    def __init__(self, name: Token, value: Expr) -> None:
        self.name = name
        self.value = value

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_assign_expr(self)

class ExprBinary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_binary_expr(self)

class ExprCall(Expr):
    def __init__(self, callee: Expr, paren: Token, arguments: list[Expr]) -> None:
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_call_expr(self)

class ExprGrouping(Expr):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_grouping_expr(self)

class ExprLiteral(Expr):
    def __init__(self, value: Any) -> None:
        self.value = value

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_literal_expr(self)

class ExprLogical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_logical_expr(self)

class ExprUnary(Expr):
    def __init__(self, operator: Token, right: Expr) -> None:
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_unary_expr(self)

class ExprVariable(Expr):
    def __init__(self, name: Token) -> None:
        self.name = name

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_variable_expr(self)

