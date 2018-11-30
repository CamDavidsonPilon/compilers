/* irtest0.g - Simple literals */

print 2;
print 3.5;
print 'a';

/* This should produce the following output:

('MOVI', 3, 'R1')
('PRINTI', 'R1')
('MOVF', 3.5, 'R2')
('PRINTF', 'R2')
('MOVB', 97, 'R3')
('PRINTB', 'R3')
*/
