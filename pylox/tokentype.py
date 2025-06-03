from enum import Enum
from typing import Any

class TokenType(Enum):
   LEFT_PAREN = "LEFT_PAREN"
   RIGHT_PAREN = "RIGHT_PAREN"
   LEFT_BRACE = "LEFT_BRACE"
   RIGHT_BRACE = "RIGHT_BRACE"
   COMMA = "COMMA"
   DOT = "DOT"
   MINUS = "MINUS"
   PLUS = "PLUS"
   SEMICOLON = "SEMICOLON"
   SLASH = "SLASH"
   STAR = "STAR"

   BANG = "BANG"
   BANG_EQUAL = "BANG_EQUAL"
   EQUAL = "EQUAL"
   EQUAL_EQUAL = "EQUAL_EQUAL"
   GREATER = "GREATER"
   GREATER_EQUAL = "GREATER_EQUAL"
   LESS = "LESS"
   LESS_EQUAL = "LESS_EQUAL"

   IDENTIFIER = "IDENTIFIER"
   STRING = "STRING"
   NUMBER = "NUMBER"

   AND = "AND"
   CLASS = "CLASS"
   ELSE = "ELSE"
   FALSE = "FALSE"
   FUN = "FUN"
   FOR = "FOR"
   IF = "IF"
   NIL = "NIL"
   OR = "OR" 
   PRINT = "PRINT"
   RETURN = "RETURN"
   SUPER = "SUPER"
   THIS = "THIS"
   TRUE = "TRUE"
   VAR = "VAR"
   WHILE = "WHILE"

   EOF = "EOF"

class Token:
    def __init__(self, typ: TokenType, lexeme: str, literal: Any, line: int) -> None:
        self.type = typ
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self) -> str:
        return f"Type: {self.type}, lexeme {self.lexeme}, literal {self.literal}"
    
    def __eq__(self, other):
        if isinstance(other, Token):
            return self.type == other.type and self.lexeme == other.lexeme and self.literal == other.literal
        return False