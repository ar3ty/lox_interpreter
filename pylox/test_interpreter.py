import unittest, io, sys
import unittest.mock

from scanner import Scanner
from parser import *
from interpreter import *

class TestInterpreter(unittest.TestCase):
    def test_interpret(self):
        statement = Print(Binary(
        Unary(Token(TokenType.MINUS, '-', None, 1),
              Literal(123.0)),
        Token(TokenType.STAR, '*', None, 1),
        Grouping(Literal(45.67))
        ))
        output_buffer = io.StringIO()
        with unittest.mock.patch('sys.stdout', new=output_buffer):
            interpreter = Interpreter()
            _, errors = interpreter.interpret([statement])
        output = output_buffer.getvalue().strip()
        self.assertEqual(output, "-5617.41")
        self.assertEqual(errors, [])

    def test_full_interpret(self):
        source = "print 4 + 15 / 3;"
        scanner = Scanner(source)
        tokens, scan_errors = scanner.scan_tokens()
        self.assertEqual(scan_errors, [])
        parser = Parser(tokens)
        statements, parse_errors = parser.parse()     
        self.assertEqual(parse_errors, [])
        output_buffer = io.StringIO()
        with unittest.mock.patch('sys.stdout', new=output_buffer):   
            interpreter = Interpreter()
            _, errors = interpreter.interpret(statements)
        output = output_buffer.getvalue().strip()
        self.assertEqual(output, "9")
        self.assertEqual(errors, [])

    