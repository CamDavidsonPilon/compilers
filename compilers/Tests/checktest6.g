/* checktest6.g - Types and declarations

   Constant and variable declarations need to have types
   attached.  Modify your checker to attach types to:

       const a = 1;  
       var x int;

   For a constant, the type comes from the expression on the right.
   For a variable, the type comes from the type name given. You'll
   need to use the name to perform a lookup of the corresponding
   Type object.

   Once you have that working, modify the checker to properly handle
   variable lookup and assignment:

      print a + 2;    // Make sure type of "a" is propagated
      x = 3 + 4;      // Make sure type of "x" matches right hand side

*/

const a = 1;
var x int;

x = a + 2;        // OK
x = 3.5;          // Error

var y int = 3.5;  // Error
var z spam;       // Error. Unknown type name 'spam'
