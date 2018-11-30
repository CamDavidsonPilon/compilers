/* lextest4.g

   All tokens
 */

/* Simple Tokens */
+ - * / = ; ( )

/* Keywords */
const var print

/* Identifiers */
a z  A Z _a _z _A _Z a123 A123 a123z A123Z

/* Tricky identifiers */
printer variable constant

/* Integers */
1234

/* Bonus Integers - Uncomment */
0x1234 0b1101011 0o123

/* Floats */
1.23 123. .123 0. .0

/* Bonus Floats - Uncomment */
1.23e1 1.23e+1 1.23e-1 123e1 1.23E1 1.23E+1

/* Characters */
'a' '\n' '\x3f' '\'' '\\'

