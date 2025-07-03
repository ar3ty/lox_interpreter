from expr import *
from stmt import *
from environment import RuntimeException
from enum import Enum

class FunctionType(Enum):
   NONE = "NONE"
   FUNCTION = "FUNCTION"
   INITIALIZER = "INITIALIZER"
   METHOD = "METHOD"

class ClassType(Enum):
   NONE = "NONE"
   CLASS = "CLASS"

class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpeter) -> None:
        self.interperter = interpeter
        self.scopes = []
        self.errors = []
        self.current_function = FunctionType.NONE
        self.current_class = ClassType.NONE

    def visit_block_stmt(self, stmt: StmtBlock) -> None:
        self.begin_scope()
        self.resolve_list(stmt.statements)
        self.end_scope()
        return None
    
    def visit_class_stmt(self, stmt: StmtClass) -> None:
        enclosing_class = self.current_class
        self.current_class = ClassType.CLASS
        self.declare(stmt.name)
        self.define(stmt.name)
        self.begin_scope()
        self.scopes[-1]["this"] = True
        for method in stmt.methods:
            declaration = FunctionType.METHOD
            if method.name.lexeme == "init":
                declaration = FunctionType.INITIALIZER
            self.resolve_function(method, declaration)
        self.end_scope()
        self.current_class = enclosing_class
        return None
    
    def visit_expression_stmt(self, stmt: StmtExpression) -> None:
        self.resolve_expr(stmt.expression)
        return None
    
    def visit_function_stmt(self, stmt: StmtFunction) -> None:
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, FunctionType.FUNCTION)
        return None
    
    def visit_print_stmt(self, stmt: StmtPrint) -> None:
        self.resolve_expr(stmt.expression)
        return None
    
    def visit_return_stmt(self, stmt: StmtReturn) -> None:
        if self.current_function == FunctionType.NONE:
            self.error(stmt.keyword, "Can't return from top-level code.")
        if stmt.value != None:
            if self.current_function == FunctionType.INITIALIZER:
                self.error(stmt.keyword, "Can't return a value from an initializer.")
            self.resolve_expr(stmt.value)
        return None

    def visit_if_stmt(self, stmt: StmtIf) -> None:
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.then_branch)
        if stmt.else_branch != None: self.resolve_stmt(stmt.else_branch)
        return None
    
    def visit_var_stmt(self, stmt: StmtVar) -> None:
        self.declare(stmt.name)
        if stmt.initializer != None:
            self.resolve_expr(stmt.initializer)
        self.define(stmt.name)
        return None
    
    def visit_while_stmt(self, stmt: StmtWhile) -> None:
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.body)
        return None
    
    def visit_assign_expr(self, expr: ExprAssign) -> None:
        self.resolve_expr(expr.value)
        self.resolve_local(expr, expr.name)
        return None
    
    def visit_binary_expr(self, expr: ExprBinary) -> None:
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)
        return None
    
    def visit_call_expr(self, expr: ExprCall) -> None:
        self.resolve_expr(expr.callee)
        for arg in expr.arguments:
            self.resolve_expr(arg)
        return None
    
    def visit_get_expr(self, expr: ExprGet):
        self.resolve_expr(expr.object)
        return None
    
    def visit_grouping_expr(self, expr: ExprGrouping) -> None:
        self.resolve_expr(expr.expression)
        return None
    
    def visit_literal_expr(self, expr: ExprLiteral) -> None:
        return None
    
    def visit_logical_expr(self, expr: ExprLogical) -> None:
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)
        return None
    
    def visit_set_expr(self, expr: ExprSet):
        self.resolve_expr(expr.value)
        self.resolve_expr(expr.object)
        return None
    
    def visit_this_expr(self, expr: ExprThis):
        if self.current_class == ClassType.NONE:
            self.error(expr.keyword, "Can't use 'this' outside of a class.")
            return None
        self.resolve_local(expr, expr.keyword)
        return None

    def visit_unary_expr(self, expr: ExprUnary) -> None:
        self.resolve_expr(expr.right)
        return None
    
    def visit_variable_expr(self, expr: ExprVariable) -> None:
        if (len(self.scopes) != 0 and 
        expr.name.lexeme in self.scopes[-1] and
        self.scopes[-1][expr.name.lexeme] == False):
            self.error(expr.name, "Can't read local variable in its own initializer.")
        self.resolve_local(expr, expr.name)
        return None
    
    def resolve_list(self, statements: list[Stmt]):
        for stmt in statements:
            self.resolve_stmt(stmt)
        return self.errors

    def resolve_stmt(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def resolve_expr(self, expr: Expr) -> None:
        expr.accept(self)

    def resolve_function(self, fun: StmtFunction, typ: FunctionType) -> None:
        enclosing_function = self.current_function
        self.current_function = typ
        self.begin_scope()
        for param in fun.parameters:
            self.declare(param)
            self.define(param)
        self.resolve_list(fun.body)
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
