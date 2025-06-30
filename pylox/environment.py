from typing import Any
from tokentype import Token, TokenType

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

class Environment:
    def __init__(self, enclosing: "Environment" = None):
        self.values = {}
        self.enclosing = enclosing

    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise RuntimeException(name, f"Undefined variable '{name.lexeme}'.")
    
    def assign(self, name: Token, value: Any) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return 
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return 
        raise RuntimeException(name, f"Undefined variable '{name.lexeme}'.")

    def define(self, name: str, value: Any) -> None:
        self.values[name] = value

    def ancestor(self, distance: int) -> 'Environment':
        environment = self
        for i in range(distance):
            environment = environment.enclosing
        return environment

    def get_at(self, distance: int, name: str) -> Any:
        return self.ancestor(distance).values[name]
    
    def assign_at(self, distance: int, name: Token, value: Any) -> None:
        self.ancestor(distance).values[name.lexeme] = value