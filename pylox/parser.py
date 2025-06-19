from tokentype import *
from expr import *
from stmt import *

class ParseError(Exception):
    def __init__(self, token: Token, message: str) -> None:
        self.message = message
        self.token = token

    def report(self, where='') -> str:
        if where == '':
            if self.token.type == TokenType.EOF:
                where = "at end"
            else:
                where = f"at '{self.token.lexeme}'"
        return f"Parse error {where} [line {self.token.line}]: {self.message}\n"

class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = tokens
        self.errors: list[ParseError] = []
        self.current = 0

    def parse(self):
        statements = []
        try:
            while not self.is_at_end():
                statements.append(self.statement())
            return statements, []
        except ParseError:
            return None, self.errors
        """
        try:
            return self.expression(), []
        except ParseError:
            return None, self.errors
        """
        
    def statement(self) -> Stmt:
        if self.match(TokenType.PRINT): return self.print_statement()
        return self.expr_statement()
    
    def print_statement(self) -> Stmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)
    
    def expr_statement(self) -> Stmt:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Expression(expr)

    def expression(self) -> Expr:
        return self.equality()
    
    def equality(self) -> Expr:
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr
    
    def comparison(self) -> Expr:
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr
    
    def term(self) -> Expr:
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr
    
    def factor(self) -> Expr:
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr
    
    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            expr = Unary(operator, right)
            return expr
        return self.primary()
    
    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            expr = Literal("false")
            return expr
        if self.match(TokenType.TRUE):
            expr = Literal("true")
            return expr
        if self.match(TokenType.NIL):
            expr = Literal("null")
            return expr
        if self.match(TokenType.NUMBER, TokenType.STRING):
            expr = Literal(self.previous().literal)
            return expr
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            expr = Grouping(expr)
            return expr
        if self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            self.error(self.previous(), "Miising left-hand operand.")
            self.equality()
            return None
        if self.match(TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL, TokenType.LESS, TokenType.GREATER):
            self.error(self.previous(), "Miising left-hand operand.")
            self.comparison()
            return None
        if self.match(TokenType.PLUS):
            self.error(self.previous(), "Miising left-hand operand.")
            self.term()
            return None
        if self.match(TokenType.STAR, TokenType.SLASH):
            self.error(self.previous(), "Miising left-hand operand.")
            self.factor()
            return None
        self.error(self.peek(), "Expect expression.")

    def match(self, *types: TokenType) -> bool:
        for typ in types:
            if self.check(typ):
                self.advance()
                return True
        return False
    
    def consume(self, typ: TokenType, message: str) -> Token:
        if self.check(typ):
            return self.advance()
        self.error(self.peek(), message)
    
    def error(self, token: Token, message:str) -> ParseError:
        error = ParseError(token, message)
        self.errors.append(error)
        raise error

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            match self.peek().type:
                case TokenType.CLASS:
                    return
                case TokenType.FUN:
                    return
                case TokenType.VAR:
                    return
                case TokenType.FOR:
                    return
                case TokenType.IF:
                    return
                case TokenType.WHILE:
                    return
                case TokenType.PRINT:
                    return
                case TokenType.RETURN:
                    return
            self.advance() 

    def check(self, typ: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == typ
    
    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
            return self.previous()
        
    def is_at_end(self) -> Token:
        return self.peek().type == TokenType.EOF
        
    def peek(self) -> Token:
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current - 1]
