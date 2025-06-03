from tokentype import TokenType, Token


class ScanError:
    def __init__(self, line: int, message: str):
        self.line = line
        self.message = message

    def report(self, where='') -> str:
        return f"Error in {where} [line {self.line}]: {self.message}\n"
    

class Scanner:
    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE
    }

    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: list[Token] = []
        self.errors: list[ScanError] = []
        self.line = 1
        self.start = 0
        self.current = 0

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens, self.errors
    
    def scan_token(self) -> None:
        c = self.advance()
        match c:
            case '(':
                self.add_token(TokenType.LEFT_PAREN)
            case ')':
                self.add_token(TokenType.RIGHT_PAREN)
            case '{':
                self.add_token(TokenType.LEFT_BRACE)
            case '}':
                self.add_token(TokenType.RIGHT_BRACE)
            case ',':
                self.add_token(TokenType.COMMA)
            case '.':
                self.add_token(TokenType.DOT)
            case '-':
                self.add_token(TokenType.MINUS)
            case '+':
                self.add_token(TokenType.PLUS)
            case ';':
                self.add_token(TokenType.SEMICOLON)
            case '*':
                self.add_token(TokenType.STAR)
            case '!':
                typ = TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG
                self.add_token(typ)
            case '=':
                typ = TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL
                self.add_token(typ)
            case '<':
                typ = TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS
                self.add_token(typ)
            case '>':
                typ = TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER
                self.add_token(typ)
            case '/':
                if self.match('/'):
                    while (self.peek() != '\n' and not self.is_at_end()):
                        self.advance()
                elif self.match('*'):
                    self.block_comment()
                else:
                    self.add_token(TokenType.SLASH)
            case ' ' | '\r' | '\t':
                pass
            case '\n':
                self.line += 1

            case '"':
                self.string()
        
            case _:
                if c.isdigit():
                    self.number()
                elif c.isalpha():
                    self.identifier()
                else:
                    self.error("Unexpected character.")
    
    def identifier(self) -> None:
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        text = self.source[self.start:self.current]
        typ = self.keywords.get(text)
        if typ == None:
            typ = TokenType.IDENTIFIER
        self.add_token(typ)
    
    def number(self) -> None:
        while self.peek().isdigit():
            self.advance()
        if (self.peek() == '.' and self.peek_next().isdigit()):
            self.advance()
            while self.peek().isdigit():
                self.advance()
        number = self.source[self.start:self.current]
        self.add_token(TokenType.NUMBER, float(number))

    def string(self) -> None:
        while (self.peek() != '"' and not self.is_at_end()):
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            self.error("Unterminated string.")
            return
        self.advance()

        value : str = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def block_comment(self) -> None:
        depth = 1
        while depth > 0 and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            if self.peek() == '*' and self.peek_next() == "/":
                depth -= 1
                self.advance()
                self.advance()
            elif self.peek() == '/' and self.peek_next() == "*":
                depth += 1
                self.advance()
                self.advance()
            else:
                self.advance()
        if self.is_at_end():
            self.error("Unterminated block comment.")
            return

    def match(self, char: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != char:
            return False
        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return '\0'
        return self.source[self.current]
    
    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c
    
    def add_token(self, typ: TokenType, literal: object = None) -> None:
        text = self.source[self.start:self.current]
        self.tokens.append(Token(typ, text, literal, self.line))

    def error(self, message: str) -> None:
        self.errors.append(ScanError(self.line, message))

