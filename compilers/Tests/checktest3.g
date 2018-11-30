/* checktest3.g - Introducing types

   All data in Gone has an associated type.  You need to start building
   the type system.  Go to the file Gone/typesys.py and look at the
   instructions there.   When you come back, start work on attaching
   types to objects.

   Your first task: attach types to simple literals.   Run this
   test using:

        bash % python3 -m gone.checker Tests/checktest3.g --show-types
*/

var x int = 0;
var z tuple(int);
z = (-3, x);
print z((x));
var y int = z((x));

print x + y;
