import unittest, io, sys
import unittest.mock

from scanner import Scanner
from parser import *
from interpreter import *

class TestInterpreter(unittest.TestCase):
    def test_interpret(self):
        statement = StmtPrint(ExprBinary(
        ExprUnary(Token(TokenType.MINUS, '-', None, 1),
              ExprLiteral(123.0)),
        Token(TokenType.STAR, '*', None, 1),
        ExprGrouping(ExprLiteral(45.67))
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

    def test_while_cond(self):
        source = """var a = 10;
while (a > 0) {
    if (a > 2) {
        print a;
    } else {
        print "a <= 2";
    }
    a = a - 1;
}"""
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
        expected = """10
9
8
7
6
5
4
3
a <= 2
a <= 2"""
        self.assertEqual(output, expected)
        self.assertEqual(errors, [])

    def test_function(self):
        source = """fun fib(n) {
  if (n <= 1) return n;
  return fib(n - 2) + fib(n - 1);
}

for (var i = 0; i < 20; i = i + 1) {
  print fib(i);
}"""
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
        expected = """0
1
1
2
3
5
8
13
21
34
55
89
144
233
377
610
987
1597
2584
4181"""
        self.assertEqual(output, expected)
        self.assertEqual(errors, [])
    
    def test_for_cycle(self):
        source = """var a = 0;
var temp;

for (var b = 1; a < 100; b = temp + b) {
  print a;
  temp = a;
  a = b;
}"""
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
        expected = """0
1
1
2
3
5
8
13
21
34
55
89"""
        self.assertEqual(output, expected)
        self.assertEqual(errors, [])

    