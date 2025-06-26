from typing import Any, Protocol, runtime_checkable
from stmt import *
from environment import Environment, RuntimeException
import time

class Return(RuntimeException):
    def __init__(self, value):
        super().__init__(None, None)
        self.value = value

@runtime_checkable
class LoxCallable(Protocol):
    def call(self, interpreter, arguments: list[Any]) -> Any: ...
    def arity(self) -> int: ...
    def __str__(self) -> str: ...

class Clock(LoxCallable):
    def call(self, interpreter, arguments: list[Any]) -> float:
        return time.time()
    
    def arity(self):
        return 0
    
    def __str__(self) -> str:
        return "native clock function"
    
class LoxFunction(LoxCallable):
    def __init__(self, declaration: StmtFunction):
        self.declaration = declaration

    def call(self, interpreter, arguments: list[Any]):
        environment = Environment(interpreter.globals)
        for i in range(len(self.declaration.parameters)):
            environment.define(self.declaration.parameters[i].lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_value:
            return return_value.value
        return None
    
    def arity(self) -> int:
        return len(self.declaration.parameters)
    
    def __str__(self) -> str:
        return f"function {self.declaration.name.lexeme}"