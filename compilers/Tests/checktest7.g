/* checktest7.g - Odd and ends

   This file contains an assortment of miscellaneous errors you might detect.
   These mostly concern further interaction between builtin type names
   and everything else.
*/

print float;      // ERROR. float is not a valid expression
y = 3;
int = 3;          // ERROR. int is not a valid location
var int float;    // ERROR. int previously declared (as a type)

var a int = 3 + 4.5;   // How many errors get reported for this?
                       // There is a type error in the expression, but
                       // does that type error also show up in the variable
                       // assignment?

