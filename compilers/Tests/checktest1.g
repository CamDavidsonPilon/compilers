/* checktest1.g - Redefinition

   Check for redefinition of previously defined symbols. To do this,
   modify your code to first check for a previously defined entry
   in the symbol table for inserting a new one.
*/

const a = 2;        // OK
var x int;          // OK

var a float;        // ERROR. a previously defined
const x = 3;        // ERROR. x previously defined


var z bool = true;
z = false;

print false && true;
print false == true;
print 1 == true;
print 1 > 2;
print 1 >= 2;
print 1 != 2;
print 1 != 2.0;


