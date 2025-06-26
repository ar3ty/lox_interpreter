from expr import *

class AstPrinter(ExprVisitor):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)
    
    def visit_binary_expr(self, expr: ExprBinary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
    
    def visit_grouping_expr(self, expr: ExprGrouping) -> str:
        return self.parenthesize("group", expr.expression)
    
    def visit_literal_expr(self, expr: ExprLiteral) -> str:
        if (expr.value == None):
            return "nil"
        return str(expr.value)
    
    def visit_unary_expr(self, expr: ExprUnary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)
    
    def parenthesize(self, name: str, *exprs: Expr) -> str:
        parts = [f"({name}"]
        for expr in exprs:
            parts.append(' ')
            parts.append(expr.accept(self))
        parts.append(')')
        return ''.join(parts)
    
class RpnPrinter(ExprVisitor):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)
    
    def visit_binary_expr(self, expr: ExprBinary) -> str:
        left = expr.left.accept(self)
        right = expr.right.accept(self)
        return f"{left} {right} {expr.operator.lexeme}"
    
    def visit_grouping_expr(self, expr: ExprGrouping) -> str:
        return expr.expression.accept(self)
    
    def visit_literal_expr(self, expr: ExprLiteral) -> str:
        if (expr.value == None):
            return "nil"
        return str(expr.value)
    
    def visit_unary_expr(self, expr: ExprUnary) -> str:
        right = expr.right.accept(self)
        return f"{right} {expr.operator.lexeme}"