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
    def __init__(self, declaration: StmtFunction, closure: Environment, is_initializer: bool):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def bind(self, instance: 'LoxInstance') -> 'LoxFunction':
        enviroment = Environment(self.closure)
        enviroment.define("this", instance)
        return LoxFunction(self.declaration, enviroment, self.is_initializer)

    def call(self, interpreter, arguments: list[Any]):
        environment = Environment(self.closure)
        for i in range(len(self.declaration.parameters)):
            environment.define(self.declaration.parameters[i].lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_value:
            if self.is_initializer: return self.closure.get_at(0, "this")
            return return_value.value
        if self.is_initializer: return self.closure.get_at(0, "this")
        return None
    
    def arity(self) -> int:
        return len(self.declaration.parameters)
    
    def __str__(self) -> str:
        return f"function {self.declaration.name.lexeme}"
    
class LoxClass(LoxCallable):
    def __init__(self, name: str, methods: dict):
        self.name = name
        self.methods = methods

    def find_method(self, name: str) -> LoxFunction:
        if name in self.methods:
            return self.methods[name]
        return None

    def call(self, interpreter, arguments: list[Any]):
        instance = LoxInstance(self)
        initializer = self.find_method("init")
        if initializer != None:
            initializer.bind(instance).call(interpreter, arguments)
        return instance
    
    def arity(self) -> int:
        initializer = self.find_method("init")
        if initializer == None: return 0
        return initializer.arity()

    def __str__(self) -> str:
        return self.name
    
class LoxInstance:
    def __init__(self, klass: LoxClass):
        self.klass = klass
        self.fields = {}

    def __str__(self) -> str:
        return self.klass.name + " instance"
    
    def get(self, name: Token):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]
        method = self.klass.find_method(name.lexeme)
        if method != None: return method.bind(self)
        raise RuntimeException(name, f"Undefined property '{name.lexeme}'.")
    
    def set(self, name: Token, value: Any) -> None:
        self.fields[name.lexeme] = value
