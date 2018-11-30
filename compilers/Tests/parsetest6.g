/* parsetest6.g

   Add line number tracking.   One thing that will become important later is
   adding line numbers to AST nodes so that you can issue error messages. 
   In your parser.py file, modify the main program so that the debugging output
   shows line numbers:

   def main():
       ...
       # Output the resulting parse tree structure
       for depth, node in flatten(ast):
           print('%s: %s%s' % (getattr(node, 'lineno', None), ' '*(4*depth), node))

   When you run your program, it show line numbers as 'None'.  You haven't assigned any.
   Add line numbers to your program by using the lineno attribute in the parser.
   Here's an example for the print statement:

   @_('PRINT expression SEMI')
   def print_statement(self, p):
       return PrintStatement(p.expression, lineno=p.lineno)

*/

print 1 +
      2 *
      3;

var x int;
const pi = 3.14159;
x = 2 + 4;
