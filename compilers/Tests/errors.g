/* errors.g

   A sample program with a wide variety of semantic errors that must be catch by
   your compiler.

*/

/* Type errors on operators */

print 2 + 2.5;               // Type error : int + float
print 2 + '4';               // Type error : int + char

/* Checks for unsupported operations on strings */

print 'H' - 'W';     // Type error: Unsupported operator - for type char
print 'H' * 'W';
print 'H' / 'W';
print +'W';
print -'H';

/* Assignment to an undefined variable */
b = 2;

/* Assignment to a constant */
const c = 4;
c = 5;

/* Assignment type error */
var d int;
d = 4;       // Good
d = 4.5;     // Bad

/* Bad type names */
var e foo;
var f d;

/* Variable declaration type error */
var g int = 2.5;

/* Propagation of types in expressions */
var h int;
var i float;
var j int = h * i;

/* Undefined variable in an expression */
print 2 + x;

/* Bad location */
print 2 + int;

/* Duplicate definition */

var d float;
var int int;

