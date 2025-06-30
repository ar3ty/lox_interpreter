from expr import *
from stmt import *
from environment import RuntimeException
from enum import Enum

class FunctionType(Enum):
   NONE = "NONE"
   FUNCTION = "FUNCTION"

class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpeter) -> None:
        self.interperter = interpeter
        self.scopes = []
        self.errors = []
        self.current_function = FunctionType.NONE

    def visit_block_stmt(self, stmt: StmtBlock) -> None:
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()
        return None
    
    def visit_expression_stmt(self, stmt: StmtExpression) -> None:
        self.resolve_single(stmt.expression)
        return None
    
    def visit_function_stmt(self, stmt: StmtFunction) -> None:
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, FunctionType.FUNCTION)
        return None
    
    def visit_print_stmt(self, stmt: StmtPrint) -> None:
        self.resolve_single(stmt.expression)
        return None
    
    def visit_return_stmt(self, stmt) -> None:
        if self.current_function == FunctionType.NONE:
            self.error(stmt.keyword, "Can't return from top-level code.")
        if stmt.value != None:
            self.resolve_single(stmt.value)
        return None

    def visit_if_stmt(self, stmt: StmtIf) -> None:
        self.resolve_single(stmt.condition)
        self.resolve_single(stmt.then_branch)
        if stmt.else_branch != None: self.resolve_single(stmt.else_branch)
        return None
    
    def visit_var_stmt(self, stmt: StmtVar) -> None:
        self.declare(stmt.name)
        if stmt.initializer != None:
            self.resolve_single(stmt.initializer)
        self.define(stmt.name)
        return None
    
    def visit_while_stmt(self, stmt: StmtWhile) -> None:
        self.resolve_single(stmt.condition)
        self.resolve(stmt.body)
        return None
    
    def visit_assign_expr(self, expr: ExprAssign) -> None:
        self.resolve_single(expr.value)
        self.resolve_local(expr, expr.name)
        return None
    
    def visit_binary_expr(self, expr: ExprBinary) -> None:
        self.resolve_single(expr.left)
        self.resolve_single(expr.right)
        return None
    
    def visit_call_expr(self, expr: ExprCall) -> None:
        self.resolve_single(expr.callee)
        for arg in expr.arguments:
            self.resolve_single(arg)
        return None
    
    def visit_grouping_expr(self, expr: ExprGrouping) -> None:
        self.resolve_single(expr.expression)
        return None
    
    def visit_literal_expr(self, expr: ExprLiteral) -> None:
        return None
    
    def visit_logical_expr(self, expr: ExprLogical) -> None:
        self.resolve_single(expr.left)
        self.resolve_single(expr.right)
        return None
    
    def visit_unary_expr(self, expr: ExprUnary) -> None:
        self.resolve_single(expr.right)
        return None
    
    def visit_variable_expr(self, expr: ExprVariable) -> None:
        if (len(self.scopes) != 0 and self.scopes[-1][expr.name.lexeme] == False):
            self.error(expr.name, "Can't read local variable in its own initializer.")
        self.resolve_local(expr, expr.name)
        return None
    
    def resolve(self, statements: list[Stmt]):
        for stmt in statements:
            self.resolve_single(stmt)
        return self.errors

    def resolve_single(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def resolve_function(self, fun: StmtFunction, typ: FunctionType) -> None:
        enclosing_function = self.current_function
        self.current_function = typ
        self.begin_scope()
        for param in fun.parameters:
            self.declare(param)
            self.define(param)
        self.resolve(fun.body)
        self.end_scope()
        self.current_function = enclosing_function

    def begin_scope(self) -> None:
        self.scopes.append({})

    def end_scope(self) -> None:
        self.scopes.pop()

    def declare(self, name: Token) -> None:
        if len(self.scopes) == 0: return
        scope = self.scopes[-1]
        if name.lexeme in scope:
            self.error(name,  "Already a variable with this name in this scope.")
        scope[name.lexeme] = False

    def define(self, name: Token) -> None:
        if len(self.scopes) == 0: return
        self.scopes[-1][name.lexeme] = True

    def resolve_local(self, expr: Expr, name: Token) -> None:
        for i in range(len(self.scopes)- 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interperter.resolve(expr, len(self.scopes) - 1 - i)
                return

    def error(self, token: Token, message: str) -> RuntimeException:
        error = RuntimeException(token, message)
        self.errors.append(error)
        return error
