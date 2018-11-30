/* irtest1.g - Binary Operations */

print (3 + 4*5 - 6) / 7;
print (3.0 + 4.0*5.0 - 6.0) / 7.0;

/* This should produce the following output:

('MOVI', 3, 'R1')
('MOVI', 4, 'R2')
('MOVI', 5, 'R3')
('MULI', 'R2', 'R3', 'R4')
('ADDI', 'R1', 'R4', 'R5')
('MOVI', 6, 'R6')
('SUBI', 'R5', 'R6', 'R7')
('MOVI', 7, 'R8')
('DIVI', 'R7', 'R8', 'R9')
('PRINTI', 'R9')
('MOVF', 3.0, 'R10')
('MOVF', 4.0, 'R11')
('MOVF', 5.0, 'R12')
('MULF', 'R11', 'R12', 'R13')
('ADDF', 'R10', 'R13', 'R14')
('MOVF', 6.0, 'R15')
('SUBF', 'R14', 'R15', 'R16')
('MOVF', 7.0, 'R17')
('DIVF', 'R16', 'R17', 'R18')
('PRINTF', 'R18')

*/
