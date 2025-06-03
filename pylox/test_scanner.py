import unittest

from scanner import *

class TestScanner(unittest.TestCase):
    def test_single_token(self):
        t1 = [Token(TokenType.IF, "if", None, 1)]
        t1.append(Token(TokenType.EOF, "", None, 1))
        scanner = Scanner("if")
        sc_tokens, errors = scanner.scan_tokens()
        self.assertEqual(t1, sc_tokens)
        self.assertEqual(errors, [])

    def test_expression(self):
        tokens = []
        tokens.append(Token(TokenType.IF, "if", None, 1))
        tokens.append(Token(TokenType.LEFT_PAREN, "(", None, 1))
        tokens.append(Token(TokenType.IDENTIFIER, "cond", None, 1))
        tokens.append(Token(TokenType.RIGHT_PAREN, ")", None, 1))
        tokens.append(Token(TokenType.EOF, "", None, 1))
        scanner = Scanner("if (cond)")
        sc_tokens, errors = scanner.scan_tokens()
        self.assertEqual(tokens, sc_tokens)
        self.assertEqual(errors, [])

    def test_string(self):
        tokens = []
        tokens.append(Token(TokenType.IDENTIFIER, "s", None, 1))
        tokens.append(Token(TokenType.EQUAL, "=", None, 1))
        tokens.append(Token(TokenType.STRING, '"string"', "string", 1))
        tokens.append(Token(TokenType.EOF, "", None, 1))
        scanner = Scanner("s = \"string\"")
        sc_tokens, errors = scanner.scan_tokens()
        self.assertEqual(tokens, sc_tokens)
        self.assertEqual(errors, [])

    def test_comment(self):
        expected = [
            Token(TokenType.PRINT, "print", None, 2),
            Token(TokenType.STRING, '"Hello"', "Hello", 2),
            Token(TokenType.SEMICOLON, ";", None, 2),
            Token(TokenType.EOF, "", None, 2),
        ]
        scanner = Scanner("// Comment line\n print \"Hello\";")
        tokens, errors = scanner.scan_tokens()
        self.assertEqual(expected, tokens)
        self.assertEqual([], errors)

    def test_block_comment(self):
        expected = [
            Token(TokenType.PRINT, "print", None, 3),
            Token(TokenType.STRING, '"Hello"', "Hello", 3),
            Token(TokenType.SEMICOLON, ";", None, 3),
            Token(TokenType.EOF, "", None, 3),
        ]
        scanner = Scanner("/* Comment\n spanning\n lines */ print \"Hello\";")
        tokens, errors = scanner.scan_tokens()
        self.assertEqual(expected, tokens)
        self.assertEqual([], errors)

    def test_nested_block_comments(self):
        expected = [
            Token(TokenType.PRINT, "print", None, 3),
            Token(TokenType.STRING, '"Hello"', "Hello", 3),
            Token(TokenType.SEMICOLON, ";", None, 3),
            Token(TokenType.EOF, "", None, 3),
        ]
        scanner = Scanner("/* Comment\n /* spanning */\n lines */ print \"Hello\";")
        tokens, errors = scanner.scan_tokens()
        self.assertEqual(expected, tokens)
        self.assertEqual([], errors)

    def test_unterminated_nested_block_comments(self):
        expected = [
            Token(TokenType.PRINT, "print", None, 3),
            Token(TokenType.STRING, '"Hello"', "Hello", 3),
            Token(TokenType.SEMICOLON, ";", None, 3),
            Token(TokenType.EOF, "", None, 3),
        ]
        scanner = Scanner("/* Comment\n /* spanning \n lines */ print \"Hello\";")
        tokens, errors = scanner.scan_tokens()
        self.assertIn("Unterminated block comment.", errors[0].message)
        self.assertEqual(1, len(errors))

    def test_unterminatred_block_comment(self):
        scanner = Scanner("/* Not closed")
        tokens, errors = scanner.scan_tokens()
        self.assertIn("Unterminated block comment.", errors[0].message)
        self.assertEqual(1, len(errors))


    