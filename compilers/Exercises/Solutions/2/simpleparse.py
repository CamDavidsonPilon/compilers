# simpleparse.py

from sly import Parser

from simplelex import SimpleLexer

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
        return p

    @_('expr PLUS term')
    def expr(self, p):
        return p

    @_('term')
    def expr(self, p):
        return p

    @_('term TIMES factor')
    def term(self, p):
        return p

    @_('factor')
    def term(self, p):
        return p

    @_('LPAREN expr RPAREN')
    def factor(self, p):
        return p

    @_('NUMBER')
    def factor(self, p):
        return p

    @_('ID')
    def factor(self, p):
        return p


if __name__ == '__main__':
    text = 'a = 2 + 3 * (4 + 5)'
    lexer = SimpleLexer()
    parser = SimpleParser()
    result = parser.parse(lexer.tokenize(text))
    print(result)

