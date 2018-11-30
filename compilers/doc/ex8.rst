Exercise 8 - Functions and Stack Frames
---------------------------------------

Programming languages let you defined user-defined functions.
For example::

    def square(x):
        return x*x

In this exercise, we refresh a few basics.

Scoping Rules
~~~~~~~~~~~~~

Variables defined inside a function are local to that
function.  For example, if you define::

    def foo():
        a = 2
        b = 3

Then the variables ``a`` and ``b`` are local to that 
function.  If there are global variables with the same name,
there are no conflicts.  Moreover, calling the function
won't overwrite the global values::

    >>> a = 10
    >>> b = 20
    >>> foo()
    >>> a
    10
    >>> b

On the other hand, functions can access the value of globals.
For example::

    >>> def bar():
            print(x)

    >>> x = 42
    >>> bar()
    42
    >>>

In general, all code in Python executes in two scopes--a local scope
which is the enclosing function and a global scope which is the
containing module.    This two-scoping rule is at the very heart of
the interpreter itself.  You can control it explicitly if you use the
``exec`` function.

    >>> gvars = {'x': 10}    # Global scope
    >>> lvars = {'n': 5}     # Local scope
    >>> exec("for i in range(n): print(i+x)", gvars, lvars)
    10
    11
    12
    13
    14
    >>> 

Under the covers, Python generates different instructions for local/global
manipulation of variables.  For example::

    >>> def foo(a):							   
            global b						   
            a = 2*a							   
            b = 2*b							   
    								   
    >>> dis.dis(foo)						   
      3           0 LOAD_CONST               1 (2) 			   
                  3 LOAD_FAST                0 (a)           # Local   
                  6 BINARY_MULTIPLY      				   
                  7 STORE_FAST               0 (a)           # Local   
    								   
      4          10 LOAD_CONST               1 (2) 			   
                 13 LOAD_GLOBAL              0 (b)           # Global  
                 16 BINARY_MULTIPLY      				   
                 17 STORE_GLOBAL             0 (b)           # Global  
                 20 LOAD_CONST               0 (None) 		   
                 23 RETURN_VALUE         				   
    >>>                                                                

In this code, local variables are accessed using ``LOAD_FAST`` and
``STORE_FAST`` instructions whereas global variables are accessed
using ``LOAD_GLOBAL`` and ``STORE_GLOBAL``.   When you define a function,
Python compiles it and is able to determine the scope of each variable
in advance (all variables assigned in a function are local unless
explicitly overridden with the ``global`` declaration).

Activation Frames
~~~~~~~~~~~~~~~~~

Every time you call a function, a new stack frame (or activation
frame) gets created.  The stack frame is a storage area for all of the
local variables defined inside the function.  For example, suppose you
had this code::

    def foo(x):
        y = 10
        z = 20
 
    def bar(a,b):
       c = 30
       foo(a)

    def spam(a):
       bar(0,a)

    x = 100
    spam(x)

Under the covers the execution stack looks like this::

     |----------------|
     |__main__:       |
     |   x = 100      |
     |----------------|
     |spam:           |
     |   a = 100      |
     |----------------|
     |bar:            |
     |   a = 0        |
     |   b = 100      |
     |   c = 30       |
     |----------------|
     |foo:            |
     |   x = 0        |
     |   y = 10       |
     |   z = 20       |
     |----------------|

You can directly see Python's stack structure whenever an exception occurs::

     >>> spam(100)
     Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 2, in spam
      File "<stdin>", line 2, in bar
      File "<stdin>", line 2, in foo
     RuntimeError: An error occurred

A little known fact about Python is that you can manually get a hook
for walking up and down the call stack if you call
``sys._getframe()``.  Try it::

    >>> import sys
    >>> def printstack():
            frame = sys._getframe()      # Get current stack frame
            while frame:
                    print("[%s]" % frame.f_code.co_name)
                    print("   Locals: %s" % list(frame.f_locals))
                    frame = frame.f_back  # Go to next frame
       
    >>> def foo():
            a = 10
            b = 20
            printstack()

    >>> foo()
    [printstack]
       Locals: ['frame']
    [foo]
       Locals: ['a', 'b']
    [<module>]
       Locals: ['__builtins__', 'printstack', '__package__', 'sys', '__name__', 'foo', '__doc__']
    >>>

    >>> def bar():
            x = 1
            y = 2
            foo()
    >>> bar()
    [printstack]
       Locals: ['frame']
    [foo]
       Locals: ['a', 'b']
    [bar]
       Locals: ['y', 'x']
    [<module>]
      Locals: ['bar', '__builtins__', 'printstack', '__package__', 'sys', '__name__', 'foo', '__doc__']

    >>>

For portability, you probably wouldn't want to write too much Python
code that relied on this.  However, sometimes programmers will get into
various "frame hacking" tricks that make use of it.

One important aspect of stack frames is that a function gets a unique 
stack frame each time it is called.  This is especially important
for recursive functions.  For example, try this::

    >>> def recursive(n):
            if n > 0:
                 recursive(n-1)
            else:
                 printstack()

    >>> recursive(10)
    [printstack]													
       Locals: ['frame']												
    [recursive]													
       Locals: ['n']												
    [recursive]													
       Locals: ['n']												
    [recursive]													
       Locals: ['n']												
    [recursive]													
       Locals: ['n']												
    [recursive]													
       Locals: ['n']												
    [recursive]													
       Locals: ['n']												
    [recursive]													
       Locals: ['n']												
    [recursive]													
       Locals: ['n']												
    [recursive]													
       Locals: ['n']												
    [recursive]													
       Locals: ['n']												
    [recursive]													
       Locals: ['n']												
    [<module>]													
       Locals: ['bar', 'recursive','__builtins__', 'printstack', '__package__', 'sys', '__name__', 'foo', '__doc__']
    >>>

Global and Local Variables in LLVM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In past work, variables in LLVM were declared as global variables.  For example::

     x_var = GlobalVariable(mod, IntType(32), name='x')
     x_var.initializer = Constant(IntType(32), 0)

For functions, you will need to start making local variables.  This is easily 
accomplished using the ``alloca`` method of builder objects::

     y_var = builder.alloca(IntType(32), name='y')
     builder.store(Constant(IntType(32), 0), y_var)

The ``alloca`` allocates a variable on the stack frame of an LLVM function.
As long as your code contines to use ``load`` and ``store`` operations to 
access variables, you shouldn't have to change much in your code.





