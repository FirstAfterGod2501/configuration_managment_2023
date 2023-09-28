from sly import Lexer, Parser
import json

class MyLexer(Lexer):
    tokens = {NAME, NUMBER, STRING}
    ignore = " \t'\n"

    literals = {'(', ')'}

    # Регулярные выражения для определения лексем
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'
    NUMBER = r'\-?\d+'

    @_(r';.*')
    def ignore_comment(self, t):
        pass

    def error(self, t):
        self.index +=1


class MyParser(Parser):
    tokens = MyLexer.tokens

    @_('expr')
    def start(self, p):
        return p.expr

    @_('value')
    def expr(self, p):
        return p.value

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('expr expr')
    def expr(self, p):
        return [p.expr0, p.expr1]

    @_('NAME')
    def value(self, p):
        return p.NAME

    @_('NUMBER')
    def value(self, p):
        return int(p.NUMBER)

    @_('STRING')
    def value(self, p):
        return p.STRING[1:-1]

    def error(self, p):
        print("Ошибка синтаксического разбора")


def to_json(obj):
    if isinstance(obj, list):
        return [to_json(item) for item in obj]
    elif isinstance(obj, dict):
        return {to_json(key): to_json(value) for key, value in obj.items()}
    elif isinstance(obj, tuple) and hasattr(obj, '_fields'):
        return {field: to_json(getattr(obj, field)) for field in obj._fields}
    else:
        return obj


text = """
    (envinstall
        (dotnet "sudo apt install dotnet")
        (gcc "sudo apt install gcc")
    )
    (database
        (host "localhost")
        (port 5432)
        (name "mydb")
    )
    (service
        (compileOptions "-O3 -std=c++20")
        (compiler "gcc")
        (add 
            (
                (source "main.cpp")
                (source "Task.h")
                (source "Task.cpp")
                (source "TaskBackend.h)
                (source "TaskBackend.cpp)
            )
        )
    )
"""

lexer = MyLexer()
parser = MyParser()

tokens = lexer.tokenize(text)
result = parser.parse(tokens)

json_result = to_json(result)
json_str = json.dumps(json_result, indent=4)
print(json_str)