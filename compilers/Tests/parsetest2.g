/* parsetest2.g

   Expression parsing including binary operations, unary operations, and grouping.
   To do this, you need to add new grammar rules such as the following:

    @_('expression PLUS expression',
       'expression TIMES expression')
    def expression(self, p):
        return BinOp(p[1], p[0], p.expression1)

    @_('MINUS expression')
    def expression(self, p):
        return UnaryOp(p[0], p.expression)

    @_('LPAREN expression RPAREN')
    def expression(self, p):
        return p.expression

    You'll also need to introduce AST nodes for BinOp and UnaryOp.
*/

/* All binary operators */

print 1 + 2;
print 1 - 2;
print 1 * 2;
print 1 / 2;

/* Unary operators */
print -1;
print +1;

/* Expression grouping */
print 2*(3+4);
