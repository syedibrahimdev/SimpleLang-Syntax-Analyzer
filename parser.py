class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, token_type):
        token = self.current()
        if token and token.type == token_type:
            self.pos += 1
        else:
            line = token.line if token else 'EOF'
            found = f'{token.type} ({token.value})' if token else 'EOF'
            raise SyntaxError(f"Expected {token_type} at line {line}, found {found}")

    def parse(self):
        while self.current():
            self.statement()

    def statement(self):
        token = self.current()
        if not token:
            return
        if token.value in ('int', 'bool', 'string'):
            self.variable_declaration()
        elif token.value == 'if':
            self.if_statement()
        elif token.value == 'for':
            self.for_loop()
        elif token.type == 'ID':
            self.assignment()
        else:
            raise SyntaxError(f"Unexpected token '{token.value}' at line {token.line}")

    def variable_declaration(self):
        self.eat('ID')  # type
        self.eat('ID')  # variable name
        token = self.current()
        if token and token.type == 'ASSIGN':
            self.eat('ASSIGN')
            self.expression()
        self.eat('END')

    def assignment(self):
        self.eat('ID')
        self.eat('ASSIGN')
        self.expression()
        self.eat('END')

    def if_statement(self):
        self.eat('ID')  # 'if'
        self.eat('LPAREN')
        self.expression()
        self.eat('RPAREN')
        self.eat('LBRACE')
        while True:
            token = self.current()
            if not token or token.type == 'RBRACE':
                break
            self.statement()
        self.eat('RBRACE')

    def for_loop(self):
        self.eat('ID')  # 'for'
        self.eat('LPAREN')

        self.variable_declaration()  # already eats ;
        self.expression()
        self.eat('END')              # this eats the second ;

        # Manual assignment parsing without extra `;`
        self.eat('ID')
        self.eat('ASSIGN')
        self.expression()
        self.eat('RPAREN')  # directly close the header

        self.eat('LBRACE')
        while True:
            token = self.current()
            if not token or token.type == 'RBRACE':
                break
            self.statement()
        self.eat('RBRACE')

    def expression(self):
        self.simple_expression()
        token = self.current()
        if token and token.type == 'COMPARE':
            self.eat('COMPARE')
            self.simple_expression()

    def simple_expression(self):
        self.term()
        while True:
            token = self.current()
            if token and token.type == 'OP':
                self.eat('OP')
                self.term()
            else:
                break

    def term(self):
        token = self.current()
        if not token:
            raise SyntaxError("Unexpected end of input while parsing term")
        if token.type in ('NUMBER', 'ID'):
            self.eat(token.type)
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            self.expression()
            self.eat('RPAREN')
        else:
            raise SyntaxError(f"Invalid term at line {token.line}")
