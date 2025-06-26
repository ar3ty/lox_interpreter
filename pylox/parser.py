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
                statements.append(self.declaration())
            return statements, self.errors
        except ParseError:
            return None, self.errors
        """
        try:
            return self.expression(), []
        except ParseError:
            return None, self.errors
        """
        
    def statement(self) -> Stmt:
        if self.match(TokenType.FOR): return self.for_statement()
        if self.match(TokenType.IF): return self.if_statement()
        if self.match(TokenType.PRINT): return self.print_statement()
        if self.match(TokenType.RETURN): return self.return_statement()
        if self.match(TokenType.WHILE): return self.while_statement()
        if self.match(TokenType.LEFT_BRACE): return StmtBlock(self.block())
        return self.expr_statement()
    
    def for_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.match(TokenType.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expr_statement()
        condition = None
        if not self.check(TokenType.SEMICOLON): condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")
        increment = None
        if not self.check(TokenType.RIGHT_PAREN): increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")
        body = self.statement()

        if increment != None:
            body = StmtBlock([body, StmtExpression(increment)])

        if condition == None: condition = ExprLiteral(True)
        body = StmtWhile(condition, body)

        if initializer != None:
            body = StmtBlock([initializer, body])

        return body
    
    def if_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE): else_branch = self.statement()
        return StmtIf(condition, then_branch, else_branch)
    
    def print_statement(self) -> Stmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return StmtPrint(value)
    
    def return_statement(self) -> Stmt:
        keyword = self.previous()
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")

    def var_declaration(self) -> Stmt:
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return StmtVar(name, initializer)
    
    def while_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()
        return StmtWhile(condition, body)

    
    def expr_statement(self) -> Stmt:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return StmtExpression(expr)
    
    def function(self, kind: str) -> Stmt:
        name = self.consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
        self.consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))
            while self.match(TokenType.COMMA):
                if len(parameters) >= 255:
                    self.error(self.peek(), "Can't have more than 255 parameters.")
                parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")

        self.consume(TokenType.LEFT_BRACE, "Expect { before " + "{kind} body.")
        body = self.block()
        return StmtFunction(name, parameters, body)

    
    def block(self) -> list[Stmt]:
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def assignment(self) -> Expr:
        expr = self.or_expression()
        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, ExprVariable):
                name = expr.name
                return ExprAssign(name, value)
            raise self.error(equals, "Invalid assignment target.")
        return expr
    
    def or_expression(self) -> Expr:
        expr = self.and_expression()
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.and_expression()
            expr = ExprLogical(expr, operator, right)
        return expr
    
    def and_expression(self) -> Expr:
        expr = self.equality()
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.equality()
            expr = ExprLogical(expr, operator, right)
        return expr

    def expression(self) -> Expr:
        return self.assignment()
    
    def declaration(self) -> Stmt:
        try:
            if self.match(TokenType.FUN): return self.function("function")
            if self.match(TokenType.VAR): return self.var_declaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None
    
    def equality(self) -> Expr:
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = ExprBinary(expr, operator, right)
        return expr
    
    def comparison(self) -> Expr:
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = ExprBinary(expr, operator, right)
        return expr
    
    def term(self) -> Expr:
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = ExprBinary(expr, operator, right)
        return expr
    
    def factor(self) -> Expr:
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = ExprBinary(expr, operator, right)
        return expr
    
    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            expr = ExprUnary(operator, right)
            return expr
        return self.call()
    
    def finish_call(self, callee: Expr) -> Expr:
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                if len(arguments) >= 255:
                    self.error(self.peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())
        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
        return ExprCall(callee, paren, arguments)
    
    def call(self) -> Expr:
        expr = self.primary()
        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            else:
                break
        return expr
    
    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            expr = ExprLiteral("false")
            return expr
        if self.match(TokenType.TRUE):
            expr = ExprLiteral("true")
            return expr
        if self.match(TokenType.NIL):
            expr = ExprLiteral("null")
            return expr
        if self.match(TokenType.NUMBER, TokenType.STRING):
            expr = ExprLiteral(self.previous().literal)
            return expr
        if self.match(TokenType.IDENTIFIER):
            expr = ExprVariable(self.previous())
            return expr
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            expr = ExprGrouping(expr)
            return expr
        raise self.error(self.peek(), "Expect expression.")

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
    
    def error(self, token: Token, message: str):
        error = ParseError(token, message)
        self.errors.append(error)
        return error

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
