import re

class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def __repr__(self):
        return f'Token(type={self.type}, value={self.value}, line={self.line})'

def tokenize(code):
    token_specification = [
        ('NUMBER',   r'\d+'),
        ('COMPARE',  r'==|!=|<=|>=|<|>'),  # Must be FIRST among symbols
        ('ASSIGN',   r'='),
        ('END',      r';'),
        ('ID',       r'[A-Za-z_]\w*'),
        ('OP',       r'&&|\|\||\+|\-|\*|\/'),
        ('LPAREN',   r'\('),
        ('RPAREN',   r'\)'),
        ('LBRACE',   r'\{'),
        ('RBRACE',   r'\}'),
        ('COMMA',    r','),
        ('NEWLINE',  r'\n'),
        ('SKIP',     r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]

    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
    tokens = []
    line_num = 1
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NEWLINE':
            line_num += 1
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character {value!r} on line {line_num}')
        else:
            tokens.append(Token(kind, value, line_num))
    return tokens
