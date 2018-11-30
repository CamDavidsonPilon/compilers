/* checktest4.g - Operators

   Add type-propagation to binary and unary operators.  To do this, you
   will need to add visit_BinOp() and visit_UnaryOp() methods to your checker.
   For example:

       def visit_BinOp(self, node):
           self.visit(node.left)
           self.visit(node.right)
           # Verify that the operator works with the left/right types
           ...
           # Set the resulting type
           node.type = ... result_type ...

   To test, run using the following:

       bash % python3 -m gone.checker Tests/checktest4.g --show-types

   Verify that types are being attached to the various expression nodes.
   There should be no errors reported in this file.
*/

/* These should all check correctly. Verify that proper types are attached */

print 2 + 3;
print 2 - 3 * 5;
print 2 * 3;
print 2 / 3;
print +2;
print -2;

print 2.0 + 3.0;
print 2.0 - 3.0;
print 2.0 * 3.0;
print 2.0 / 3.0;
print +2.0;
print -2.0;

print 'h';

