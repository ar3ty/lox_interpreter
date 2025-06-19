import unittest

from scanner import Scanner
from parser import *
from expr import *
from astprinter import *

class TestParser(unittest.TestCase):
    def test_manual_tokens(self):
        tokens = []
        tokens.append(Token(TokenType.LEFT_PAREN, "(", None, 1))
        tokens.append(Token(TokenType.NUMBER, "5", 5.0, 1))
        tokens.append(Token(TokenType.MINUS, "-", None, 1))
        tokens.append(Token(TokenType.NUMBER, "3", 3.0, 1))
        tokens.append(Token(TokenType.RIGHT_PAREN, ")", None, 1))
        tokens.append(Token(TokenType.STAR, "*", None, 1))
        tokens.append(Token(TokenType.MINUS, "-", None, 1))
        tokens.append(Token(TokenType.NUMBER, "2", 2.0, 1))
        tokens.append(Token(TokenType.EQUAL_EQUAL, "==", None, 1))
        tokens.append(Token(TokenType.NUMBER, "4", 4.0, 1))
        tokens.append(Token(TokenType.SEMICOLON, ";", None, 1))
        tokens.append(Token(TokenType.EOF, "", None, 1))
        parser = Parser(tokens)
        statements, errors = parser.parse()
        expression = Binary(
            Binary(
                Grouping(Binary(
                    Literal(5.0),
                    Token(TokenType.MINUS, "-", None, 1),
                    Literal(3.0)
                )),
                Token(TokenType.STAR, "*", None, 1),
                Unary(
                    Token(TokenType.MINUS, "-", None, 1),
                    Literal(2.0)
                )
            ),
            Token(TokenType.EQUAL_EQUAL, "==", None, 1),
            Literal(4.0)
            )
        printer = AstPrinter()
        ast1 = printer.print(expression)
        ast2 = printer.print(statements[0].expression)
        self.assertEqual(ast1, ast2)
        self.assertEqual(errors, [])

    def test_auto_tokens(self):
        source = "(5-3)* -2 == 4;"
        scanner = Scanner(source)
        tokens, errors = scanner.scan_tokens()
        parser = Parser(tokens)
        pr_stmts, errors = parser.parse()
        expression = Binary(
            Binary(
                Grouping(Binary(
                    Literal(5.0),
                    Token(TokenType.MINUS, "-", None, 1),
                    Literal(3.0)
                )),
                Token(TokenType.STAR, "*", None, 1),
                Unary(
                    Token(TokenType.MINUS, "-", None, 1),
                    Literal(2.0)
                )
            ),
            Token(TokenType.EQUAL_EQUAL, "==", None, 1),
            Literal(4.0)
            )
        printer = AstPrinter()
        ast1 = printer.print(expression)
        ast2 = printer.print(pr_stmts[0].expression)
        self.assertEqual(ast1, ast2)
        self.assertEqual(errors, [])

    def test_no_expression(self):
        source = "-"
        scanner = Scanner(source)
        tokens, errors = scanner.scan_tokens()
        parser = Parser(tokens)
        pr_expr, errors = parser.parse()
        self.assertEqual(pr_expr, None)
        self.assertIn(errors[0].message, "Expect expression.")

    def test_no_right_paren(self):
        source = "(3-4"
        scanner = Scanner(source)
        tokens, errors = scanner.scan_tokens()
        parser = Parser(tokens)
        pr_expr, errors = parser.parse()
        self.assertEqual(pr_expr, None)
        self.assertIn(errors[0].message, "Expect ')' after expression.")