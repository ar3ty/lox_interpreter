from typing import Any, Protocol
from tokentype import Token
from expr import Expr

class StmtVisitor(Protocol):
    def visit_block_stmt(self, stmt: "StmtBlock") -> Any: ...
    def visit_expression_stmt(self, stmt: "StmtExpression") -> Any: ...
    def visit_function_stmt(self, stmt: "StmtFunction") -> Any: ...
    def visit_if_stmt(self, stmt: "StmtIf") -> Any: ...
    def visit_print_stmt(self, stmt: "StmtPrint") -> Any: ...
    def visit_return_stmt(self, stmt: "StmtReturn") -> Any: ...
    def visit_var_stmt(self, stmt: "StmtVar") -> Any: ...
    def visit_while_stmt(self, stmt: "StmtWhile") -> Any: ...

class Stmt:
    def accept(self, visitor: StmtVisitor) -> Any:
        raise NotImplementedError("Method accept() must be realized")

class StmtBlock(Stmt):
    def __init__(self, statements: list[Stmt]) -> None:
        self.statements = statements

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_block_stmt(self)

class StmtExpression(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_expression_stmt(self)

class StmtFunction(Stmt):
    def __init__(self, name: Token, parameters: list[Token], body: list[Stmt]) -> None:
        self.name = name
        self.parameters = parameters
        self.body = body

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_function_stmt(self)

class StmtIf(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt) -> None:
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_if_stmt(self)

class StmtPrint(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_print_stmt(self)

class StmtReturn(Stmt):
    def __init__(self, keyword: Token, value: Expr) -> None:
        self.keyword = keyword
        self.value = value

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_return_stmt(self)

class StmtVar(Stmt):
    def __init__(self, name: Token, initializer: Expr) -> None:
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_var_stmt(self)

class StmtWhile(Stmt):
    def __init__(self, condition: Expr, body: Stmt) -> None:
        self.condition = condition
        self.body = body

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_while_stmt(self)

