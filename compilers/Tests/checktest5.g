/* checktest5.g - Unsupported Operators

   The statements in this file should all generate type errors.
   To test, run:

       bash % python3 -m gone.checker Tests/checktest5.g

*/

print 2 + 3.5;    // ERROR      
print 2.0 + 3;    // ERROR

print 'h' + 'w';  // ERROR
print 'h' - 'w';
print 'h' * 'w';
print 'h' / 'w';
print -'h';
print +'h';

/* This is a particularly tricky case.  How do you want to report
   errors that propagate through a large expression?   Every operation
   needs to produce some kind of type for later stages of checking to
   work. However, once an error is reported, they tend to cascade.
   So, does this expression produce a single type error (1+2.0) or
   does it produce 5 type errors (one for each operator)?
*/

print 1 + 2.0 + 3 + 4 + 5 + 6;


