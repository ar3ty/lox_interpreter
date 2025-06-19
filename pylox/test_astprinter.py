import unittest

from tokentype import TokenType
from astprinter import *

class TestAstPrinter(unittest.TestCase):
    def test_print(self):
        expression = Binary(
        Unary(Token(TokenType.MINUS, '-', None, 1),
              Literal(123)),
        Token(TokenType.STAR, '*', None, 1),
        Grouping(Literal(45.67))
        )
        printer = AstPrinter()
        repr = printer.print(expression)
        self.assertEqual(repr, "(* (- 123) (group 45.67))")

    def test_rpnprint(self):
        expression = Binary(
            Unary(Token(TokenType.MINUS, '-', None, 1),
                Literal(123)),
            Token(TokenType.STAR, '*', None, 1),
            Grouping(Literal(45.67))
        )
        printer = RpnPrinter()
        repr = printer.print(expression)
        self.assertEqual(repr, "123 - 45.67 *")