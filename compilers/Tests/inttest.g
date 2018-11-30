/* inttest.g

   Test all of the basic expressions on integers.
*/

/* Integer operations */

const a = 1;          // Integer constant
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
print(b);
(b++;)
print(b);

