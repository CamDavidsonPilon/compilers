/* irtest4.g - Variable declarations and assignment */
/*
var x int = 42;
var y int;
y = x + 10;

var pi float = 3.14159;
var z float;
z = 2.0 * pi;

var a char = 'a';
var b char;
b = a;
print b;

var c bool = true;
var d bool = false;

print c && d;
print c || d;
print true;
print 1;
print 2;
*/

print true;
print !true;
print -1;


/* The expected output is

('MOVI', 42, 'R1')
('VARI', 'x')
('STOREI', 'R1', 'x')
('VARI', 'y')
('LOADI', 'x', 'R2')
('MOVI', 10, 'R3')
('ADDI', 'R2', 'R3', 'R4')
('STOREI', 'R4', 'y')
('MOVF', 3.14159, 'R5')
('VARF', 'pi')
('STOREF', 'R5', 'pi')
('VARF', 'z')
('MOVF', 2.0, 'R6')
('LOADF', 'pi', 'R7')
('MULF', 'R6', 'R7', 'R8')
('STOREF', 'R8', 'z')
('MOVB', 97, 'R9')
('VARB', 'a')
('STOREB', 'R9', 'a')
('VARB', 'b')
('LOADB', 'a', 'R10')
('STOREB', 'R10', 'b')
*/

