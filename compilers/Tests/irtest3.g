/* irtest3.g - Constant declarations */

const x = 2;
const pi = 3.14159;
const a = 'a';

print x;
print pi;
print a;

/* This should produce the following:

('MOVI', 2, 'R1')
('VARI', 'x')
('STOREI', 'R1', 'x')
('MOVF', 3.14159, 'R2')
('VARF', 'pi')
('STOREF', 'R2', 'pi')
('MOVB', 97, 'R3')
('VARB', 'a')
('STOREB', 'R3', 'a')
('LOADI', 'x', 'R4')
('PRINTI', 'R4')
('LOADF', 'pi', 'R5')
('PRINTF', 'R5')
('LOADB', 'a', 'R6')
('PRINTB', 'R6')

Note: Constants are declared as ordinary variables.  You don't worry
about immutability at this stage because that was already validated in
the type checker.

To make this part of the project work, you'll need to pay careful
attention to location nodes and reading of locations in expressions.

*/
