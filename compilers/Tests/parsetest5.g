/* parsetest5.g

   Add precedence specifiers.   Consider the two statements:

      print 2 * 3 + 4;
      print 2 + 3 * 4;

   These two statements should group operations differently. For
   example, with added parens to emphasize:

      print (2 * 3) + 4;
      print 2 + (3 * 4);

   Run your parser on this file and carefully study the output.
   Figure out what's wrong with it.
*/

print 2 * 3 + 4;
print 2 + 3 * 4;

/* Fix the precedence by filling in the following precedence table
   in the parser.

   precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
   )

   Note: Making this change should make shift/reduce errors go away.
 */
