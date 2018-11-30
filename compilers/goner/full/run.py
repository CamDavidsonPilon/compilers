# gone/run.py
#
# Project 5:
# ----------
# Runs a Gone program in a LLVM JIT.   This requires that the
# Gone runtime support library (gonert.c) be compiled into a shared
# object and placed in the same directory as this file.
#
# Note:  This project will require minor modification in Project 8

import os
import os.path
import ctypes
import llvmlite.binding as llvm

_path = os.path.dirname(__file__)

def run(llvm_ir):
    # Load the runtime
    if os.name != 'nt':
        ctypes._dlopen(os.path.join(_path, 'gonert.so'), ctypes.RTLD_GLOBAL)
    else:
        ctypes._dlopen(os.path.join(_path, 'gonert.dll'), ctypes.RTLD_GLOBAL)

    # Initialize LLVM
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()

    engine = llvm.create_mcjit_compiler(mod, target_machine)

    # Execute the main() function
    #
    # !!! Note: Requires modification in Project 8 (see below)

    init_ptr = engine.get_function_address('__init')
    init_func = ctypes.CFUNCTYPE(None)(init_ptr)
    init_func()

    main_ptr = engine.get_function_address('_gone_main')
    main_func = ctypes.CFUNCTYPE(None)(main_ptr)
    main_func()

    # Project 8:  Modify the above code to execute the Gone __init()
    # function that initializes global variables.  Then add code below
    # that executes the Gone main() function.

def main():
    from .errors import errors_reported
    from .llvmgen import compile_llvm
    import sys

    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 -m gone.run filename\n")
        raise SystemExit(1)

    source = open(sys.argv[1]).read()
    llvm_code = compile_llvm(source)
    if not errors_reported():
        run(llvm_code)

if __name__ == '__main__':
    main()
