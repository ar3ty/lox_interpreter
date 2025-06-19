import sys, locale
from scanner import Scanner
from astprinter import AstPrinter
from parser import Parser
from interpreter import Interpreter
    
def main(argv: list) -> None:
    if len(argv) > 2:
        print("Usage: python3 pylox [script]")
        sys.exit(64)
    elif len(argv) == 2:
        run_file(argv[1])
    else:
        run_prompt()
        
def run_file(path: str) -> None:
    with open(path, 'rb') as f:
        bytes = f.read()
    text = bytes.decode(locale.getpreferredencoding())
    error = run(text)
    if error:
        sys.exit(error)

def run_prompt() -> None:
    try:
        while True:
            try:
                line = input("> ")
                run(line)
            except EOFError:
                break
    except KeyboardInterrupt:
        print("Stoped due to the user interruption")

def run(code: str):
    scanner = Scanner(code)
    tokens, scan_errors = scanner.scan_tokens()

    if scan_errors:
        for error in scan_errors:
            sys.stderr.write(error.report())
        sys.stderr.flush()
        return 65
    print(tokens)

    parser = Parser(tokens)
    statements, parse_errors = parser.parse()

    if parse_errors:
        for error in parse_errors:
            sys.stderr.write(error.report())
        sys.stderr.flush()
        return 65
    
    
    interpreter = Interpreter()
    text, runtime_errors = interpreter.interpret(statements)
    print(runtime_errors)

    if runtime_errors:
        for error in runtime_errors:
            sys.stderr.write(error.report())
        sys.stderr.flush()
        return 70
    
    print(text)
    return None
    

if __name__ == "__main__":
    main(sys.argv)