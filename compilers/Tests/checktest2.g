/* checktest2.g - Reading/Writing 

   In this test, you need to add some checks for reading/writing
   of identifiers.   There are two different kinds of declarations:

      const a = 2;     // Constant
      var b int = 3;   // Variable

   Both can be read:

      print a;
      print b;

   However, only one can be assigned:

      a = 3;     // ERROR (constant)
      b = 4;     // OK

   Modify your type-checker to catch this kind of error.  Doing this
   is a bit brain-bending, but one way to do it involves propagating a
   location "usage" downwards in the tree and having it checked when
   locations are consulted.  For example, 

      def visit_Assignment(self, node):
          # Set a usage of the location *BEFORE* visiting it
          node.location.usage = 'write'

          # Visit the location
          self.visit(node.location)

   Now, in the location visitor, you check for usage:

      def visit_SimpleLocation(self, node):
          sym = self.symbols[node.name]       # Look up the symbol
          if node.usage == 'write' and not isinstance(sym, VarDeclaration):
              error(node.lineno, f"Can't assign to {node.name}")

   For consistency, you'll also need to add a usage attribute when 
   reading from a location in expressions:

      def visit_ReadValue(self, node):
          node.location.usage = 'read'
          self.visit(node.location)
*/
   
const a = 2;
a = 4;              // ERROR. a is constant
print(a);           // OK. Reading

var b int;
b = 5;              // OK. Storing a value
print(b);           // OK. Reading
