/* parsetest4.g

   You need to add support for the concepts of reading and assigning values.
   First, there is the more general concept of a "location".  For example:

       print 1 + <location> ;
       <location> = 1 + 2 ;

   In our language, a "location" is a simple variable name.  For example:

       var x int = 1;
       print 1 + x;
       x = 1 + 2;

   At a more advanced stage, a location could be something else such as an
   array location:

       print 1 + x[0];
       x[0] = 1 + 2;

   To do this part, you need to define AST nodes for locations:

       class Location(AST):
           pass

       class SimpleLocation(Location):
           name : str

   You then need to modify your grammar to allow locations to be used
   in expressions and in assignment statements.   This might require
   more AST nodes to be defined.
*/

var x int = 1;
print 1 + x;
x = 1 + 2;

var z bool;
var y bool = false;
const v = true;

print (false && true) || !false;

print (false && true);
