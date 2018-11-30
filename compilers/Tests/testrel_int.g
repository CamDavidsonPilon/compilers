/* testrel_int.g

   Some tests of integer relations with no errors.  This code should check and run.
 */

var a int = 2;
var b int = 3;

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

print 2 < 3 || 3 > 4 || 10 < 1;

var c bool = true;
var d bool = false;

print c && d;
print c || d;
print !(c);

