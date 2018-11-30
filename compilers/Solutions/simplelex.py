# simplelex.pysimplelex.py


from sly import Lexer

class SimpleLexer(Lexer):
    # Token names
    tokens = { NUMBER, ID, LPAREN, RPAREN, TIMES, PLUS, LT, LE, GT, GE, EQ, NE, ASSIGN, IF, ELSE, WHILE, OCTAL }

    # Ignored characters
    ignore = ' \t'

    # Token regexs
    NUMBER = r'\d+'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE

    LPAREN = r'\('
    RPAREN = r'\)'
    TIMES  = r'\*'
    PLUS   = r'\+'
    LE     = r'<='
    GE     = r'>='
    LT     = r'<'
    GT     = r'>'
    EQ     = r'=='
    NE     = r'!='
    ASSIGN = r'='


    def NUMBER(self, t):
        if t.value[0] == '0':
            t.type='OCTAL'
        print("saw a number", t)
        return t

    @_(r'\n+')
    def ignore_newline(self,  t):
        self.lineno += t.value.count('\n')


    def error(self, t):
        print('Bad character %r' % t.value[0])
        self.index += 1

# Example
if __name__ == '__main__':
    text = '''
           a < b
           a <= b
           a > b
           a >= b
           a == b
           a != b
           052
           if a < b

    '''
    lexer = SimpleLexer()
    for tok in lexer.tokenize(text):
        print(tok)
