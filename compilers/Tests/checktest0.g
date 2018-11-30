/* checktest0.g - Symbol tables

   Your first step is to track symbols as created by
   const and var declarations like this:

     const pi = 3.14159;
     var x int;

   In the checker.py file, define a symbol table as a dictionary.

     self.symbols = { }

   Define visit_ConstDeclaration and visit_VarDeclaration methods
   that put declarations into the symbol table. For example:

     def visit_ConstDeclaration(self, node):
         self.symbols[node.name] = node

   Define further visit_* methods that allow you detect undefined
   symbols when read in expressions and assigned.
*/

const pi = 3.14159;
const pi = 2;
var x int;                  // OK
print pi;                   // OK
print x;                    // OK
print y;                    // error. y undefined

x = 45;                     // OK
z = 13;                     // error. z undefined

