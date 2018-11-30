/* irtest2.g - Unary Operations */

print -(1+2);
print +(3+4);
print -(5.0+6.0);
print +(7.0+8.0);

/*
This one is a bit tricky.  The underlying virtual machine doesn't have any
concept of a unary operation.  So, to implement -x, you'll need to use 0-x.
For the + operators, nothing much happens.

The following output should be produced:

('MOVI', 1, 'R1')
('MOVI', 2, 'R2')
('ADDI', 'R1', 'R2', 'R3')
('MOVI', 0, 'R4')
('SUBI', 'R4', 'R3', 'R5')
('PRINTI', 'R5')
('MOVI', 3, 'R6')
('MOVI', 4, 'R7')
('ADDI', 'R6', 'R7', 'R8')
('PRINTI', 'R8')
('MOVF', 5.0, 'R9')
('MOVF', 6.0, 'R10')
('ADDF', 'R9', 'R10', 'R11')
('MOVF', 0.0, 'R12')
('SUBF', 'R12', 'R11', 'R13')
('PRINTF', 'R13')
('MOVF', 7.0, 'R14')
('MOVF', 8.0, 'R15')
('ADDF', 'R14', 'R15', 'R16')
('PRINTF', 'R16')

*/
