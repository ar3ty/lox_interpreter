import unittest

from tokentype import TokenType
from astprinter import *

class TestAstPrinter(unittest.TestCase):
    def test_print(self):
        expression = ExprBinary(
        ExprUnary(Token(TokenType.MINUS, '-', None, 1),
              ExprLiteral(123)),
        Token(TokenType.STAR, '*', None, 1),
        ExprGrouping(ExprLiteral(45.67))
        )
        printer = AstPrinter()
        repr = printer.print(expression)
        self.assertEqual(repr, "(* (- 123) (group 45.67))")

    def test_rpnprint(self):
        expression = ExprBinary(
            ExprUnary(Token(TokenType.MINUS, '-', None, 1),
                ExprLiteral(123)),
            Token(TokenType.STAR, '*', None, 1),
            ExprGrouping(ExprLiteral(45.67))
        )
        printer = RpnPrinter()
        repr = printer.print(expression)
        self.assertEqual(repr, "123 - 45.67 *")