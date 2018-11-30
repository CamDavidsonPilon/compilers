/* testrel_float.g

   Some tests of relations involving floating point numbers with no errors.  
   This code should check and run.
 */

var a float = 2.0;
var b float = 3.0;

print a < b;
print a <= b;
print a > b;
print a >= b;
print a == b;
print a != b;
print a < b && a > b;
print a < b || a > b;
print !(a<b);

print true;
print false;

print !(a<b) || false;

print 2.0 < 3.0 || 3.0 > 4.0 || 10.0 < 1.0;
