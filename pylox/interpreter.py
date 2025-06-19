from expr import *
from stmt import *
from typing import Any
from tokentype import *

class RuntimeException(Exception):
    def __init__(self, token: Token, message: str) -> None:
        self.message = message
        self.token = token

    def report(self, where='') -> str:
        if where == '':
            if self.token.type == TokenType.EOF:
                where = "at end"
            else:
                where = f"at '{self.token.lexeme}'"
        return f"Runtime error {where} [line {self.token.line}]: {self.message}\n"

class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self) -> None:
        self.errors: list[RuntimeException] = []

    def interpret(self, stmts: list[Stmt]):
        try:
            for stmt in stmts:
                self.execute(stmt)
            return None, []
        except RuntimeException:
            return None, self.errors
        """
        try:
            value = self.evaluate(expr)
            text = self.stringify(value)
            return text, self.errors
        except RuntimeException:
            return None, self.errors
        """
        
    def stringify(self, value: Any) -> str:
        if value is None: return "nil"
        if isinstance(value, float):
            text = str(value)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(value)

    def visit_binary_expr(self, expr: Binary) -> Any:
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
                self.error(expr.operator, "Operand must be two numbers or two strings.")
    
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
    
    def visit_grouping_expr(self, expr: Grouping) -> Any:
        return self.evaluate(expr.expression)
    
    def visit_literal_expr(self, expr: Literal) -> Any:
        return expr.value
    
    def visit_unary_expr(self, expr: Unary) -> str:
        right = self.evaluate(expr.right)
        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -float(right)
            case TokenType.BANG:
                return not self.is_truthy()
               
        return None
    
    def check_number_operand(self, operator: Token, obj: Any):
        if isinstance(obj, float): return
        self.error(operator, "Operand must be a number.")
    
    def check_number_operands(self, operator: Token, left: Any, right: Any):
        if isinstance(left, float) and isinstance(right, float): return
        self.error(operator, "Operands must be numbers.")

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
    
    def error(self, token: Token, message:str) -> RuntimeException:
        error = RuntimeException(token, message)
        self.errors.append(error)
        raise error
    
    def visit_expression_stmt(self, stmt: Expression) -> None:
        self.evaluate(stmt.expression)
        return None
    
    def visit_print_stmt(self, stmt: Print) -> None:
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None