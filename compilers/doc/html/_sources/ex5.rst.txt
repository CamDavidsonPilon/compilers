Exercise 5 - Introducing LLVM
-----------------------------

LLVM is a compiler writing framework that addresses many of the
problems with emitting low-level machine code.  However, it can also
be daunting to jump into.  If you're using developer tools such as
XCode on the Mac, you're using LLVM.  The clang C/C++ compiler is
written on top of LLVM.  It is also used to implement various Just In
Time (JIT) compilation tools.

In this exercise, we're going to introduce the basics of creating LLVM
code.  To do this, we're going to use the ``llvmlite`` package
developed by Continuum Analytics.  This is available in the Anaconda
Python distribution so if you're using that, you should already have
it. 

LLVM Preliminaries
~~~~~~~~~~~~~~~~~~

Your first task is to make sure Anaconda Python and the clang C/C++
compiler have been installed on your machine. Please review the README
file for the compilers project regarding installation notes.

Hello World
~~~~~~~~~~~

The first step in using LLVM is to make a LLVM module which contains
all of the code you will be generating.  Create a file
``hellollvm.py`` and put this code into it::

    # hellollvm.py
    from llvmlite.ir import Module

    mod = Module('hello')
    print(mod)

Run the program and you should get some output like this::

    bash % python3 hellollvm.py
    ; ModuleID = "hello"
    target triple = "unknown-unknown-unknown"
    target datalayout = ""

    bash %

The output you're using is LLVM low-level code--a kind of architecture
independent assembly language. At this point, it's not too
interesting.  However, let's declare a function to put in the module.
Change the program to the following to declare a function with the C
prototype ``int hello()``::

    # hellollvm.py

    from llvmlite.ir import (
        Module, Function, FunctionType, IntType
        )

    mod = Module('hello')
    hello_func = Function(mod, FunctionType(IntType(32), []), name='hello')
    print(mod)

Running the program, you should now get the following::

    bash % python3 hellollvm.py
    ; ModuleID = "hello"
    target triple = "unknown-unknown-unknown"
    target datalayout = ""

    declare i32 @"hello"() 

    bash %

Again, it's not too interesting at this point.  However, you can see
how a function declaration was placed in the module output. The LLVM
statement ``declare i32 @"hello"()`` is declaring a function that
returns a 32-bit integer and takes no arguments.

Let's add some code to the function.  To do this, you first need to
create a basic block. A basic block is a container that holds
low-level instructions.  Add the following to the program::

    # hellollvm.py
    
    from llvmlite.ir import (
        Module, Function, FunctionType, IntType
        )

    mod = Module('hello')
    hello_func = Function(mod, FunctionType(IntType(32), []), name='hello')
    block = hello_func.append_basic_block('entry')
    print(mod)

When you run the program, you should now get this output::

    ; ModuleID = "hello"
    target triple = "unknown-unknown-unknown"
    target datalayout = ""

    define i32 @"hello"() 
    {
    entry:
    }

Notice how the function declaration has changed into an actual
function definition and a code label ``entry:`` has been inserted.

Finally, let's add an instruction to the block.  To do this, you need
to create a ``IRBuilder`` object.  A builder is a class that makes it
easy to add instructions to a block.  Modify the program to make the
function return a constant value 37::

    # hellollvm.py
    
    from llvmlite.ir import (
        Module, Function, FunctionType, IntType, 
        Constant, IRBuilder
        )

    mod = Module('hello')
    hello_func = Function(mod, FunctionType(IntType(32), []), name='hello')
    block = hello_func.append_basic_block('entry')
    builder = IRBuilder(block)
    builder.ret(Constant(IntType(32), 37))
    print(mod)

Running the program should now produce this::

    ; ModuleID = "hello"
    target triple = "unknown-unknown-unknown"
    target datalayout = ""
    
    define i32 @"hello"() 
    {
    entry:
      ret i32 37
    }

There you are---a complete LLVM function that does nothing but return
a value.  Now, a question arises: How do you go about getting it to run?

Compilation to a Standalone Executable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to run your LLVM generated code, one approach is to feed it
to a LLVM-based compiler such as ``clang``.  Save your generated
code to a file ``hello.ll``::

   bash % python3 hellollvm.py > hello.ll
   bash % 

Now, write a short C program to bootstrap::

    /* main.c */
    #include <stdio.h>

    extern int hello(); 

    int main() {
        printf("hello() returned %i\n", hello());
    }

Compile this program together with ``hello.ll`` to make an executable::

    bash % clang main.c hello.ll
    bash % ./a.out
    hello() returned 37
    bash %

This basic technique for invoking your code and creating stand-alone programs
will be useful for testing and development.  You also get the advantage of 
being able to use C library functions such as ``printf()``.  Without this,
you'd have to figure out how to perform I/O directly using low-level LLVM
instructions--which would not be fun.

A Function with Arguments
~~~~~~~~~~~~~~~~~~~~~~~~~

Let's make a more interesting function.  This function takes two
arguments ``x`` and ``y`` and computes the value ``x**2 + y**2``.  To
do this, we're going to follow similar steps as above. First, declare
the function, add a basic block, and make a new builder.  Once the
builder is obtained, we'll create some instructions to compute and
return the result. Add the following code to your ``hellollvm.py``
program::

    # hellollvm.py
    ...

    # A user-defined function
    from llvmlite.ir import DoubleType

    ty_double = DoubleType()
    dsquared_func = Function(mod, 
                             FunctionType(ty_double, [ty_double, ty_double]), 
                             name='dsquared')
    block = dsquared_func.append_basic_block('entry')
    builder = IRBuilder(block)

    # Get the function args
    x, y = dsquared_func.args

    # Compute temporary values for x*x and y*y
    xsquared = builder.fmul(x, x)
    ysquared = builder.fmul(y, y)

    # Sum the values and return the result
    d2 = builder.fadd(xsquared, ysquared)
    builder.ret(d2)

    # Output the final module
    print(mod)

One thing to notice is that you use the builder to carry out the steps
needed to perform the calculation that you're trying to perform. Python
variables such as ``x``, ``xsquared``, and ``d2`` are being used to
hold intermediate results.

If you run this program, you should output similar to the following::

    ; ModuleID = "hello"
    ...

    define double @"dsquared"(double %".1", double %".2") 
    {
    entry:
      %".4" = fmul double %".1", %".1"
      %".5" = fmul double %".2", %".2"
      %".6" = fadd double %".4", %".5"
      ret double %".6"
    }

To test it, modify the C bootstrap code as follows::

    /* main.c */
    #include <stdio.h>
    
    extern int hello();
    extern double dsquared(double, double);
    
    int main() {
      printf("Hello returned: %i\n", hello());
      printf("dsquared(3, 4) = %f\n", dsquared(3.0, 4.0));
    }

Compile as follows::
  
    bash % python3 hellollvm.py > hello.ll
    bash % clang main.c hello.ll
    bash % ./a.out
    Hello returned: 37
    dsquared(3, 4) = 25.000000
    bash %

Calling an external function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Even though you're emitting low-level assembly code, there's no need
to completely reinvent the wheel from scratch.  Suppose you wanted to
call a function already defined in a C library?  Here is how you
declare a reference to the ``sqrt()`` function in the C math library::

    # hellollvm.py
    ...

    sqrt_func = Function(mod, 
                         FunctionType(ty_double, [ty_double]), 
                         name='sqrt')

Now, define a distance function that evaluates ``sqrt(dsquared(x,y))``::

    # hellollvm.py
    ...

    distance_func = Function(mod, 
                             FunctionType(ty_double, [ty_double, ty_double]), 
                             name='distance')
    block = distance_func.append_basic_block('entry')
    builder = IRBuilder(block)
    x, y = distance_func.args
    d2 = builder.call(dsquared_func, [x, y])
    d = builder.call(sqrt_func, [d2])
    builder.ret(d)

If you run ``hellollvm.py``, you should get output that looks like this::

    ; ModuleID = "hello"
    ...

    declare double @"sqrt"(double %".1") 
    
    define double @"distance"(double %".1", double %".2") 
    {
    entry:
      %".4" = call double (double, double)* @"dsquared"(double %".1", double %".2")
      %".5" = call double (double)* @"sqrt"(double %".4")
      ret double %".5"
    }

Modify the ``main.c`` program for testing::

    /* main.c */
    #include <stdio.h>

    extern int hello();
    extern double dsquared(double, double);
    extern double distance(double, double);

    int main() {
      printf("Hello returned: %i\n", hello());
      printf("dsquared(3, 4) = %f\n", dsquared(3.0, 4.0));
      printf("distance(3, 4) = %f\n", distance(3.0, 4.0));
    }

Compile and run::

   bash % python3 hellollvm.py > hello.ll
   bash % clang main.c hello.ll -lm
   bash % ./a.out
   Hello returned: 37
   dsquared(3, 4) = 25.000000
   distance(3, 4) = 5.000000
   bash %

You should be getting exactly the output above.  If not, stop and
figure out what's wrong.

As an aside, you're not limited to calling just existing C
libraries. You can make your own custom C runtime functions and call
them from your LLVM generated code using the same technique.  You'll
be doing this in the project.

Variables and State
~~~~~~~~~~~~~~~~~~~

You might want to define a variable that keeps its state.  Let's make
a global variable ``x``::

    # hellollvm.py
    ...
    from llvmlite.ir import GlobalVariable
    x_var = GlobalVariable(mod, ty_double, 'x')
    x_var.initializer = Constant(ty_double, 0.0)

Now, let's write a function that increments the variable and 
prints its new value.  To do this, you use ``load`` and ``store``
instructions to manipulate the variable state::

    # hellollvm.py
    ...

    from llvmlite.ir import VoidType

    incr_func = Function(mod, 
                         FunctionType(VoidType(), []), 
                         name='incr')
    block = incr_func.append_basic_block('entry')
    builder = IRBuilder(block)
    tmp1 = builder.load(x_var)
    tmp2 = builder.fadd(tmp1, Constant(ty_double, 1.0))
    builder.store(tmp2, x_var)
    builder.ret_void()

Modify the ``main.c`` file as follows::

    /* main.c */
    #include <stdio.h>

    extern int hello();
    extern double dsquared(double, double);
    extern double distance(double, double);
    extern double x;
    extern void incr();

    int main() {
      printf("Hello returned: %i\n", hello());
      printf("dsquared(3, 4) = %f\n", dsquared(3.0, 4.0));
      printf("distance(3, 4) = %f\n", distance(3.0, 4.0));
      printf("x is %f\n", x);
      incr();
      printf("x is now %f\n", x);
    }

Compile and run the program again::

   bash % python3 hellollvm.py > hello.ll
   bash % clang main.c hello.ll -lm
   bash % ./a.out
   Hello returned: 37
   dsquared(3, 4) = 25.000000
   distance(3, 4) = 5.000000
   x is 0.000000
   x is now 1.000000
   bash %

Just in Time Compilation
~~~~~~~~~~~~~~~~~~~~~~~~

In our example, we are creating LLVM instructions, writing them to a
file, and using the ``clang`` compiler to produce an executable. 
This is not the only approach.  If you desired, you could compile
directly in Python and access the instructions via a library such as
``ctypes``.   This part is a bit tricky, but add the following code to
``hellollvm.py``::

    # hellollvm.py 
    ...

    import llvmlite.binding as llvm

    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    compiled_mod = llvm.parse_assembly(str(mod))
    engine = llvm.create_mcjit_compiler(compiled_mod, target_machine)

    # Look up the function pointer (a Python int)
    func_ptr = engine.get_function_address("distance")

    # Turn into a Python callable using ctypes
    from ctypes import CFUNCTYPE, c_int, c_double
    distance = CFUNCTYPE(c_double, c_double, c_double)(func_ptr)

    res = distance(3, 4)
    print('distance =', res)

If you run this, you should see the program run the code, and
produce output such as this::

    bash % python3 hellollvm.py
    distance = 5.0
    bash %

This version is a bit different than normal compilation in that the code
runs inside an active Python interpreter process. The performance should be
the same, it's just that you're launching the code via ctypes.  In the
earlier examples, you were creating standalone executables with no
Python dependency at all.

A LLVM Mini-Reference
~~~~~~~~~~~~~~~~~~~~~

This section aims to provide a mini-reference for using LLVM in the
next part of the project.   It summarizes some of the critical bits.

For creating LLVM code, use the following import::

    from llvmlite.ir import (
          Module, Function, FunctionType, IRBuilder, 
	  IntType, DoubleType, Constant
	  )

All LLVM code is placed in a module.  You create one like this::

    mod = Module("modname")

You declare functions like this::

    func = Function(mod, 
                    FunctionType(rettype, [argtypes]),
                    name="funcname")

The following basic datatypes are used heavily in declarations::
 
    IntType(32)             # A 32-bit integer
    DoubleType()            # A double-precision float

To define constants corresponding to the above types, do this::
  
    c = Constant(IntType(32), value)
    d = Constant(DoubleType(), value)

To start adding code to a function, you must add a basic block
and create a builder.  For example::

    block = func.append_basic_block('entry')
    builder = IRBuilder(block)

Builder objects have a variety of useful methods for adding
instructions.  These include::

    # Returning values
    builder.ret(value)            
    builder.ret_void()            
 
    # Integer math
    builder.add(left, right)
    builder.sub(left, right)
    builder.mul(left, right)
    builder.sdiv(left, right)    

    # Floating math
    builder.fadd(left, right)
    builder.fsub(left, right)
    builder.fmul(left, right)
    builder.fdiv(left, right)

    # Function call
    builder.call(func, args)

When using the builder, it is important to emphasize that you must
save the results of the above operations and use them in subsequent
calls.  For example::

    t1 = builder.fmul(a, b)
    t2 = builder.fmul(c, d)
    t3 = builder.fadd(t1, t2)
    ...

To declare a global variable do something like this::

    name_var = GlobalVariable(module, IntType(32), name='varname')
    name_var.initializer = Constant(IntType(32), 0)

To access a global variable, use load and store instructions::

    tmp = builder.load(name_var)
    builder.store(tmp, name_var)



    
    
