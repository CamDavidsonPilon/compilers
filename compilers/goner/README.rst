This directory contains a very basic reference implementation of Gone
through the end of Project 5. It implements all phases of the project
and can run simple programs.  Look at it for implementation hints and
other details.

This implementation does NOT include all possible Gone features.
It is also not implemented in the most elegant way.

The compiler includes various stages that can execute independently.

Tokenizing:
-----------
python3 -m goner.tokenize filename.g  

Parsing
-------
python3 -m goner.parser filename.g

Type Checking
-------------
python3 -m goner.checker filename.g

Intermediate code generation
----------------------------
python3 -m goner.ircode filename.g

LLVM Code generation
--------------------
python3 -m goner.llvmgen filename.g

IR Code Interpreter
-------------------
python3 -m goner.interp filename.g

LLVM Just in Time Compilation
-----------------------------
python3 -m goner.run filename.g

Stand-alone Compilation
-----------------------
python3 -m goner.compile filename.g
