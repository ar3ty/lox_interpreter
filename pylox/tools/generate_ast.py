import sys
from pathlib import Path

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: generate_ast <output_directory>")
        sys.exit(64)
    output_dir = sys.argv[1]
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    import_for_expr = ["from typing import Any, Protocol",
                       "from tokentype import Token"]
    import_for_stmt = import_for_expr + ["from expr import Expr"]
    define_ast(output_dir, "Expr", import_for_expr, [
        "Assign   : Token name, Expr value",
        "Binary   : Expr left, Token operator, Expr right",
        "Call     : Expr callee, Token paren, list[Expr] arguments",
        "Get      : Expr object, Token name",
        "Grouping : Expr expression",
        "Literal  : Any value",
        "Logical  : Expr left, Token operator, Expr right",
        "Set      : Expr object, Token name, Expr value",
        "This     : Token keyword",
        "Unary    : Token operator, Expr right",
        "Variable : Token name"
    ])
    define_ast(output_dir, "Stmt", import_for_stmt, [
        "Block      : list[Stmt] statements",
        "Class      : Token name, list['StmtFunction'] methods",
        "Expression : Expr expression",
        "Function   : Token name, list[Token] parameters, list[Stmt] body",
        "If         : Expr condition, Stmt then_branch, Stmt else_branch",
        "Print      : Expr expression",
        "Return     : Token keyword, Expr value",
        "Var        : Token name, Expr initializer",
        "While      : Expr condition, Stmt body"
    ])



def define_ast(output_dir: str, base_name: str, imports: list[str], types: list[str]) -> None:
    path = Path(output_dir) / f"{base_name.lower()}.py"
    with open (path, 'w', encoding='utf-8') as writer:
        # File heading
        for imprt in imports:
            writer.write(f"{imprt}\n")
        writer.write(f"\n")
        define_visitor(writer, base_name, types)
        writer.write(f"class {base_name}:\n")
        writer.write(f"    def accept(self, visitor: {base_name}Visitor) -> Any:\n"+
                     f"        raise NotImplementedError(\"Method accept() must be realized\")\n\n")
        for type_def in types:
            class_name, fields = type_def.split(':', 1)
            define_type(writer, base_name, class_name.strip(), fields)


def define_type(writer, base_name: str, class_name: str, fields: str) -> None:
    # subclass head
    writer.write(f"class {base_name}{class_name.strip()}({base_name}):\n")
    fields = fields.strip().split(", ")
    writer.write(f"    def __init__(self")
    # type announcement
    for field in fields:
        typ, name = field.strip().split()
        writer.write(f", {name}: {typ}")
    writer.write(f") -> None:\n")
    # init filling
    for field in fields:
        typ, name = field.strip().split()
        writer.write(f"        self.{name} = {name}\n")
    writer.write('\n' +
                 f"    def accept(self, visitor: {base_name}Visitor) -> Any:\n" +
                 f"        return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)")
    writer.write(f"\n\n")


def define_visitor(writer, base_name: str, types: list[str]) -> None:
    # Visitor interface generation
    writer.write(f"class {base_name}Visitor(Protocol):\n")
    for type in types:
        name = type.split(':')[0].strip()
        writer.write(
            f"    def visit_{name.lower()}_{base_name.lower()}" +
            f"(self, {base_name.lower()}: \"{base_name}{name}\") -> Any: ...\n"
        )
    writer.write("\n")


if __name__ == "__main__":
    main()