import sys, locale
from scanner import *
    
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
    errors = run(text, path)
    if errors:
        sys.exit(65)

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
        
had_error = False

def run(code: str, where:str = '') -> list[ScanError]:
    scanner = Scanner(code)
    tokens, errors = scanner.scan_tokens()

    if errors:
        for error in errors:
            sys.stderr.write(error.report(where))
        sys.stderr.flush()
        return errors

    for token in tokens:
        print(token)


if __name__ == "__main__":
    main(sys.argv)