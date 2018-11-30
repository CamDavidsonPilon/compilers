# simpleparse.py

from sly import Parser

from simplelex import SimpleLexer
from simpleast import *

class SimpleParser(Parser):

    tokens = SimpleLexer.tokens

    # Grammar:
    #
    # assignment ::=  ID ASSIGN expr 
    #
    # expr       ::= expr PLUS term
    #             |  term
    #
    # term       ::= term TIMES factor
    #             |  factor
    #
    # factor     ::= LPAREN expr RPAREN
    #             |  NUMBER
    #             |  ID

    @_('ID ASSIGN expr')
    def assignment(self, p):
        return ('=', p.ID, p.expr)

    @_('expr PLUS term')
    def expr(self, p):
        return ('+', p.expr, p.term)

    @_('term')
    def expr(self, p):
        return p.term

    @_('term TIMES factor')
    def term(self, p):
        return ('*', p.term, p.factor)

    @_('factor')
    def term(self, p):
        return p.factor

    @_('LPAREN expr RPAREN')
    def factor(self, p):
        return p.expr

    @_('NUMBER')
    def factor(self, p):
        return p.NUMBER

    @_('ID')
    def factor(self, p):
        return p.ID

if __name__ == '__main__':
    text = 'a = 2 + 3 * (4 + 5)'
    lexer = SimpleLexer()
    parser = SimpleParser()
    result = parser.parse(lexer.tokenize(text))
    print(result)
