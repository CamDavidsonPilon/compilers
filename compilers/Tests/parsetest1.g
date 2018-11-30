/* parsetest1.g

   Modify the grammer so that it can deal with multiple print statements.
   To do this, you need to figure out some way to collect multiple statements.
   This can be done using a list if you're a bit clever.  At first, this is
   going to seem a bit brain-bending.

   Make a pair of grammar rules like this:

   @_('statement')
   def statements(self, p):               # A single statement
       return [ p.statement ]             # The initial list

   @_('statements statement')
   def statements(self, p):               # Multiple statements
       p.statements.append(p.statement)   # Add a statement to previous statements
       return p.statements

  Then make a grammar rule that collects all of the possible statements
  in one place.

  @_('print_statement',
     # add more statements later
    )
  def statement(self, p):
      return p[0]
*/

print 42;
print 3.14159;
print 'a';
