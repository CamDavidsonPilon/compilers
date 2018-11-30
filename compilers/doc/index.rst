.. Write a Compiler documentation master file, created by
   sphinx-quickstart on Fri Sep 23 12:10:12 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Write a Compiler
================

David Beazley (http://www.dabeaz.com), Copyright (C) 2012-2018

This directory contains files related to the "Write a Compiler"
course.  Essential details are provided below.

Course Setup
------------

The recommended setup for this project is Python 3.6 with the following added
packages:

    - llvmlite    (http://llvmlite.readthedocs.org)
    - SLY         (https://github.com/dabeaz/sly)
    - clang C/C++ compiler

To simplify the installation, it is recommended that you use the Anaconda Python
distribution as it includes all of the needed tools.

Course Slides
-------------

Course lecture slides as found in the file ``CompilerSlides.pdf``.
Please consult as needed during the class.

Exercises
---------

There are eight course exercises.  Each exercise serves as an
introduction to a corresponding project section.  Do you
work with the exercises in the ``Exercises`` directory.
Solution code for exercises can be found in ``Exercises/Solutions``.


.. toctree::
   ex1
   ex2
   ex3
   ex4
   ex5
   ex6
   ex7
   ex8
   :maxdepth: 1

Projects
--------

You will be implementing a compiler for a simple language called
Gone.

.. toctree::
  Overview
  Gone
  :maxdepth: 1

The project is divided into 8 parts. Make sure you do the 
corresponding exercise for each part first.

.. toctree::
   Project1
   Project2
   Project3
   Project4
   Project5
   Project6
   Project7
   Project8
   Project9
   :maxdepth: 1

The project for this course is substantial--eventually consisting of
several thousand lines of Python code.  The ``gone`` directory is
where you will be doing your work.  Presently, this directory contains
a few ``.py`` files that contain a skeleton of the compiler and
further instructions.

A reference implementation of the compiler is found in the ``goner``
directory.  This is a very basic implementation without a lot of bells
and whistles.  However, if you get stuck, it's okay to look at it for
a hint.  To get the most out of the project, you are strongly
encourage to work on your own implementation of the project rather
than copying solution code.  You'll want to think about other issues
such as testing as well.

Due to the complexity of the project, it is strongly suggested that
you do all of your work under version control (git, Mercurial,
subversion, etc.).  After each project, you should check in code
changes and tag your work.  This will be very useful should you need
to revert code later in the project.

Testing
-------

The ``Tests/`` directory contains a series of test inputs and other
files for testing various stages of the compiler.  Instructions about
specific tests will be given in each project section.

The ``Programs/`` directory contains full programs that you can try
once you have the complete compiler working.  You will likely only be
able to run these programs when you get to the very end of the project.

One challenge is to think about debugging and unit testing as you go along.
The compiler has a lot of moving parts and testing is non-trivial.
