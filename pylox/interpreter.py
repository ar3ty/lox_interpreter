from expr import *
from stmt import *
from typing import Any
from tokentype import *
from environment import Environment, RuntimeException
from lox_callable import *

class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self) -> None:
        self.errors: list = []
        self.globals = Environment()
        self.environment = self.globals
        self.globals.define("clock", Clock())


    def interpret(self, stmts: list[Stmt]):
        try:
            for stmt in stmts:
                self.execute(stmt)
            return None, self.errors
        except RuntimeException:
            return None, self.errors
        
    def stringify(self, value: Any) -> str:
        if value is None: return "nil"
        if isinstance(value, float):
            text = str(value)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(value)

    def visit_binary_expr(self, expr: ExprBinary) -> Any:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        match expr.operator.type:
            case TokenType.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                raise self.error(expr.operator, "Operand must be two numbers or two strings.")
    
            case TokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return float(left) * float(right)
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)

        return None
    
    def visit_call_expr(self, expr: ExprCall) -> Any:
        callee = self.evaluate(expr.callee)
        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))
        if not isinstance(callee, LoxCallable):
            raise self.error(expr.paren, "Can only call functions and classes.")
        function = callee
        if len(arguments) != function.arity():
            raise self.error(expr.paren, f"Expected {function.arity()} arguments but got {len(arguments)}.")
        return function.call(self, arguments)

    def visit_grouping_expr(self, expr: ExprGrouping) -> Any:
        return self.evaluate(expr.expression)
    
    def visit_literal_expr(self, expr: ExprLiteral) -> Any:
        return expr.value
    
    def visit_logical_expr(self, expr: ExprLogical) -> Any:
        left = self.evaluate(expr.left)
        if expr.operator.type == TokenType.OR:
            if self.is_truthy(left): return left
        else:
            if not self.is_truthy(left): return left
        return self.evaluate(expr.right)
    
    def visit_unary_expr(self, expr: ExprUnary) -> str:
        right = self.evaluate(expr.right)
        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -float(right)
            case TokenType.BANG:
                return not self.is_truthy()
               
        return None
    
    def visit_variable_expr(self, expr: ExprVariable) -> Any:
        return self.environment.get(expr.name)

    def check_number_operand(self, operator: Token, obj: Any):
        if isinstance(obj, float): return
        raise self.error(operator, "Operand must be a number.")
    
    def check_number_operands(self, operator: Token, left: Any, right: Any):
        if isinstance(left, float) and isinstance(right, float): return
        raise self.error(operator, "Operands must be numbers.")

    def is_truthy(self, obj: Any) -> bool:
        if obj == None: return False
        if isinstance(obj, bool): return obj
        return True

    def is_equal(self, a: Any, b: Any) -> bool:
        if a is None and b is None: return True
        if a is None or b is None: return False
        if isinstance(a, float) and isinstance(b, float):
            return a == b
    
    def evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)
    
    def execute(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def execute_block(self, statements: list[Stmt], environment: Environment) -> None:
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visit_block_stmt(self, stmt: StmtBlock):
        self.execute_block(stmt.statements, Environment(self.environment))
        return None
    
    def error(self, token: Token, message:str) -> RuntimeException:
        error = RuntimeException(token, message)
        self.errors.append(error)
        return error
    
    def visit_expression_stmt(self, stmt: StmtExpression) -> None:
        self.evaluate(stmt.expression)
        return None
    
    def visit_function_stmt(self, stmt: StmtFunction) -> None:
        function = LoxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)
        return None
    
    def visit_if_stmt(self, stmt: StmtIf):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)
        return None
    
    def visit_print_stmt(self, stmt: StmtPrint) -> None:
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None
    
    def visit_return_stmt(self, stmt: StmtReturn) -> None:
        value = None
        if stmt.value != None: value = self.evaluate(stmt.value)
        raise Return(value)
    
    def visit_var_stmt(self, stmt: StmtVar):
        value = None
        if stmt.initializer != None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return None
    
    def visit_while_stmt(self, stmt: StmtWhile):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None

    def visit_assign_expr(self, expr: ExprAssign):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value
