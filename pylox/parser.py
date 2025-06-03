from tokentype import *
from expr import *

class ParseError(RuntimeError):
    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.token = token

class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current = 0

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

    def match(self, *types: TokenType) -> bool:
        for typ in types:
            if self.check(typ):
                self.advance()
                return True
        return False
    
    def consume(self, typ: TokenType, message: str) -> Token:
        if self.check(typ):
            return self.advance()
        raise self.error(self.peek(), message)
    
    def error(self, token: Token, message:str) -> ParseError:
        return ParseError(token, message)

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
