# simplelex.py

from sly import Lexer

class SimpleLexer(Lexer):
    # Token names
    tokens = { 'NUMBER', 'ID', 'PLUS', 'TIMES', 'LPAREN', 'RPAREN', 'ASSIGN',
               'LT', 'LE', 'GT', 'GE', 'EQ', 'NE', 'IF', 'ELSE', 'WHILE' }

    # Ignored characters
    ignore = ' \t'

    # Token regexs
    NUMBER = r'\d+'

    PLUS =r'\+'
    TIMES = r'\*'
    LPAREN = r'\('
    RPAREN = r'\)'
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    EQ = r'=='
    NE = r'!='
    ASSIGN = r'='   

    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
        keywords = { 'if', 'else', 'while' }
        if t.value in keywords:
            t.type = t.value.upper()
        return t

    @_(r'\n+')
    def ignore_newline(self,  t):
        self.lineno += t.value.count('\n')

    def error(self, value):
        print('Bad character %r' % value[0])
        self.index += 1

# Example
if __name__ == '__main__':
    text = '''
           if a < b 
           else a <= b
           while a > b
           a >= b
           a == b
           a != b
    '''
    lexer = SimpleLexer()
    for tok in lexer.tokenize(text):
        print(tok)

    
    
