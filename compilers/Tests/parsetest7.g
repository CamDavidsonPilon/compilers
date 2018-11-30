/* parsetest7.g

   This file aims to test all of the valid datatypes and operators
   for the first part of the project.
*/

/* Integer operations */
var x int = 0;
var y int = 0;
var a int = 0;
x ++ ;
x -= y + 1;
(x, y = 1, 2+5;)
(a = 1;)
x = y = 1;
x = 1; y= 2;


var b int = 2;        // Integer variable declaration (with value)
var c int;            // Integer declaration (no value)

c = a + b + 3;        // Assignment to an integer
print c;              // Integer printing.  Outputs 6

print a + b;          // Outputs 3
print a - b;          // Outputs -1
print b * c;          // Outputs 12
print c / b;          // Outputs 3
print +a;             // Outputs 1
print -a;             // Outputs -1

// Test of associativity
print a + b * c;       // Outputs 13

/* Floating point operations */

const fa = 1.0;        // Float constant
var fb float = 2.0;    // Float variable declaration (with value)
var fc float;          // Variable declaration (no value)

fc = fa + fb + 3.0;    // Assignment to an float
print fc;              // Float printing.  Outputs 6.0

print fa + fb;         // Outputs 3.0
print fa - fb;         // Outputs -1.0
print fb * fc;         // Outputs 12.0
print fc / fb;         // Outputs 3.0
print +fa;             // Outputs 1.0
print -fa;             // Outputs -1.0

/* Character literals */

const ca = 'a';
var cb char;

print ca;           // Outputs 'a'
cb = 'b';
y = x + 2;
