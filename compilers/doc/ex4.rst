Exercise 4 - Code Generation
----------------------------

In earlier exercises, you looked at how Python represents abstract
syntax trees and wrote some code to walk through the trees.  In this
exercise, we look at how to generate low-level code from an AST.

Python Machine Code
~~~~~~~~~~~~~~~~~~~

When you write Python functions, they get compiled down to a low-level
interpreter machine code.   You can view the code using the ``dis`` module.
Try it::

    >>> def foo():				    
            return a + 2*b - 3*c			    
    						    
    >>> import dis  				    
    >>> dis.dis(foo)				    
      2           0 LOAD_GLOBAL              0 (a)	    
                  3 LOAD_CONST               1 (2)	    
                  6 LOAD_GLOBAL              1 (b)	    
                  9 BINARY_MULTIPLY     		    
                 10 BINARY_ADD          		    
                 11 LOAD_CONST               2 (3)	    
                 14 LOAD_GLOBAL              2 (c)	    
                 17 BINARY_MULTIPLY     		    
                 18 BINARY_SUBTRACT     		    
                 19 RETURN_VALUE        		    
    >>>

Python's machine code is based on a simple stack machine. To carry out operations, operands
are first pushed onto a stack.  Different operations then consume entries on the stack
and replace the top entry with the result.  Here is an example::

     >>> # Evaluate a = 1 + 2*3 - 4*5  using a stack machine
     >>> stack = []
     >>> stack.append(1)
     >>> stack.append(2)
     >>> stack.append(3)
     >>> stack
     [1, 2, 3]
     >>> stack[-2:] = [stack[-2] * stack[-1]]
     >>> stack
     [1, 6]
     >>> stack[-2:] = [stack[-2] + stack[-1]]
     >>> stack
     [7]
     >>> stack.append(4)
     >>> stack.append(5)
     >>> stack
     [7, 4, 5]
     >>> stack[-2:] = [stack[-2] * stack[-1]]
     >>> stack
     [7, 20]
     >>> stack[-2:] = [stack[-2] - stack[-1]]
     >>> stack
     [-13]
     >>> a = stack.pop()
     >>> a
     -13
     >>>

Turning an AST into machine code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To turn an AST into machine code, you walk the AST and turn each AST node
into a sequence of low-level machine instructions.  One way to represent
instructions is as tuples of the form (opcode, ...).

First, let's get the AST for expression in the Python function you just defined::

    >>> import ast
    >>> top = ast.parse("a + 2*b - 3*c")
    >>> print(ast.dump(top))
    Module(body=[Expr(value=BinOp(left=BinOp(left=Name(id='a',ctx=Load()), 
                 op=Add(), right=BinOp(left=Num(n=2), op=Mult(),
                 right=Name(id='b', ctx=Load()))), op=Sub(),
                 right=BinOp(left=Num(n=3), op=Mult(), right=Name(id='c',
                 ctx=Load()))))])
    >>> 

Let's generate code.  Define the following class::

    import ast					   
    class CodeGenerator(ast.NodeVisitor):		   
        def __init__(self):				   
            self.code = []				   
    						   
        def visit_BinOp(self,node):			   
            self.visit(node.left)			   
            self.visit(node.right)			   
            opname = node.op.__class__.__name__	   
            inst = ("BINARY_"+opname.upper(),)	   
            self.code.append(inst)			   
            					   
        def visit_Name(self,node):			   
            if isinstance(node.ctx, ast.Load):	   
                inst = ('LOAD_GLOBAL',node.id)		   
            else:					   
                inst = ('Unimplemented',)		   
            self.code.append(inst)			   
    						   
        def visit_Num(self,node):			   
            inst = ('LOAD_CONST',node.n)		   
            self.code.append(inst)                     

Now, let's use it to generate low-level machine instructions::

     >>> top = ast.parse("a + 2*b - 3*c")
     >>> gen = CodeGenerator()
     >>> gen.visit(top)
     >>> gen.code
     [('LOAD_GLOBAL', 'a'), ('LOAD_CONST', 2), ('LOAD_GLOBAL', 'b'), ('BINARY_MULT',), ('BINARY_ADD',),
      ('LOAD_CONST', 3), ('LOAD_GLOBAL', 'c'), ('BINARY_MULT',), ('BINARY_SUB',)]
     >>> for inst in gen.code:
             print(inst)

     ('LOAD_GLOBAL', 'a')
     ('LOAD_CONST', 2)
     ('LOAD_GLOBAL', 'b')
     ('BINARY_MULT',)
     ('BINARY_ADD',)
     ('LOAD_CONST', 3)
     ('LOAD_GLOBAL', 'c')
     ('BINARY_MULT',)
     ('BINARY_SUB',)
     >>>

Observe: Your generated code from the AST is virtually identical to that
produced by the disassembly of the earlier function.   To fully generate
code, you'd need to flesh out the ``CodeGenerator`` class so that it 
covers all possible AST nodes, but the overall idea is the same.

Discussion
~~~~~~~~~~

Code generation is often not much more than what we have done here.
Essentially you're going to traverse the AST and create a sequence of
low-level instructions for carrying out operations.



