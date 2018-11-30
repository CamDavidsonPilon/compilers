Exercise 2  - Parsing and Abstract Syntax Trees
-----------------------------------------------

The second step of a compiler is to parse the sequence of tokens
produced by the lexer.  Often, the end result of parsing is a data
structure known as an Abstract Syntax Tree (AST).  For example,
suppose you have this statement::

       a = 2 + 3 * (4 + 5)

An abstract syntax tree might look like this::

              =
            /   \
          "a"    +
               /   \
              2     *
                  /   \
                 3     +
                     /   \
                    4     5

Essentially, the AST describes the syntactic structure of the program.
For example, in this tree, the topmost node is "=" which means that it
is an assignment statement.  The left-hand node is the location of the
assignment ("a") and the right-hand node is the value.  Since the
value is an arithmetic expression, it consists of further nodes
corresponding to different mathematical operators.

A minimal way to represent an AST is through a series of nested tuples
of the the form (operation, child1, child2, ...).  For example, the
above parse tree could be stored like this::

     parse = ('=', 'a', ('+', 2, ('*', 3, ('+', 4, 5))))

This structure is very similar to what are known as S-expressions in
Lisp (See http://en.wikipedia.org/wiki/S-expression).   

Parser Generator Tools
~~~~~~~~~~~~~~~~~~~~~~

In most programming languages, parsers are rarely written entirely by
hand.  Parsing is a well-studied problem in computer science involving
various algorithms and strategies.  Generally what happens is that the
grammar for a language is specified in a high-level form and then fed
to a tool that generates the appropriate parsing code.  The reason
for doing this is that the grammar for a typical programming language might
have hundreds of grammar rules.  If everything is hand-coded, it becomes
incredibly hard to make changes and add new language features. Tools
vastly simplify this.

Even Python works this way.  If you've never looked at this part of
the CPython source, go take a look.  In the CPython source
distribution, the file ``Grammar/Grammar`` contains a specification of
the Python language grammar.  Go look at it.

During the compilation of Python, the grammar is processed by a tool called
``pgen`` to create C source code.  Try it yourself::
 
      bash % cd Python-3.5
      bash % Parser/pgen Grammar/Grammar graminit.h graminit.c
      bash % cat graminit.h
      ... look at the output ...
      bash % cat graminit.c
      ... look at the output ...

Under the covers it all gets turned into cryptic parsing tables. You're
not really supposed to worry about it though (i.e., the generated code
is not meant to be understood by humans).

Just so you know, PEP 306 has information about what's involved in changing the
Python grammar.  See http://www.python.org/dev/peps/pep-0306/.

Writing a Parser with SLY
~~~~~~~~~~~~~~~~~~~~~~~~~

To write our parser, we're going to use SLY.  To do this, you will
need the lexer written for Exercise 1.  Copy the file
``Exercises/1/simplelex.py`` if you need to get working code.  Create
a file ``simpleparser.py`` that looks like this::

    # simpleparse.py

    from sly import Parser
    from simplelex import SimpleLexer

    class SimpleParser(Parser):
        # Specify the tokens set (terminals)

        tokens = SimpleLexer.tokens

        # Grammar:
        #
        # assignment ::=  ID ASSIGN expr 
        #
        # expr       ::= expr PLUS term
        #             |  term
        #
        # term       ::= term TIMES factor
        #             |  factor
        #
        # factor     ::= LPAREN expr RPAREN
        #             |  NUMBER
        #             |  ID

        @_('ID ASSIGN expr')
        def assignment(self, p):
            return p

        @_('expr PLUS term')
        def expr(self, p):
            return p

        @_('term')
        def expr(self, p):
            return p

        @_('term TIMES factor')
        def term(self, p):
            return p

        @_('factor')
        def term(self, p):
            return p

        @_('LPAREN expr RPAREN')
        def factor(self, p):
            return p

        @_('NUMBER')
        def factor(self, p):
            return p

        @_('ID')
        def factor(self, p):
            return p

    if __name__ == '__main__':
        text = 'a = 2 + 3 * (4 + 5)'
        lexer = SimpleLexer()
        parser = SimpleParser()
        result = parser.parse(lexer.tokenize(text))
        print(result)

As first glance, this is likely to make your head shatter.  Weird
decorators.  Duplicate method names?  What on earth is going on?
Essentially what's happening here is a form of pattern matching.  If
you have a grammar rule like this::

    expr ::= expr PLUS term

it gets expressed as a method like this::

    @_('expr PLUS term')
    def expr(self, p):
        return p

The ``@_()`` decorator gives the right-hand-side of the grammar rule
(e.g., ``expr PLUS term``). The name of the method must match the
left-hand-side (e.g., ``expr``).

Running the above code, you may get output similar to this::

    WARNING: Token 'GT' defined, but not used
    WARNING: Token 'ELSE' defined, but not used
    WARNING: Token 'LT' defined, but not used
    WARNING: Token 'NE' defined, but not used
    WARNING: Token 'GE' defined, but not used
    WARNING: Token 'EQ' defined, but not used
    WARNING: Token 'LE' defined, but not used
    WARNING: Token 'IF' defined, but not used
    WARNING: Token 'WHILE' defined, but not used
    WARNING: There are 9 unused tokens
    ('assignment', 'a', '=', ('expr', ('expr', ('term', ('factor', '2'))), '+', 
      ('term', ('term', ('factor', '3')), '*', ('factor', '(', ('expr', ('expr', 
      ('term', ('factor', '4'))), '+', ('term', ('factor', '5'))), ')'))))

The warning messages mean that the tokenizer might produce tokens
that are unrecognized by the parser because they don't appear in
any grammar rules.  The first rule of parsing tools is to pay
attention to the warning messages!   Usually they mean that
there is some kind of potential problem.  For now, we'll ignore the
messages.

The final output of the program is a concrete syntax tree, expressed
as nested tuples. Reading through that is a bit painful, but you 
should see some output that matches the structure of what was parsed.

Building S-Expressions
~~~~~~~~~~~~~~~~~~~~~~

One problem here is that parse trees are often much more complicated
than you'd like.  It might make more sense to try to simplify it.

Try modifying your grammar so that it looks like this::

    # simpleparse.py
    
    from sly import Parser
    from simplelex import SimpleLexer
    
    class SimpleParser(Parser):
   
        tokens = SimpleLexer.tokens

        # Grammar:
        #
        # assignment ::=  ID ASSIGN expr 
        #
        # expr       ::= expr PLUS term
        #             |  term
        #
        # term       ::= term TIMES factor
        #             |  factor
        #
        # factor     ::= LPAREN expr RPAREN
        #             |  NUMBER
        #             |  ID

        @_('ID ASSIGN expr')
        def assignment(self, p):
            return ('=', p.ID, p.expr)

        @_('expr PLUS term')
        def expr(self, p):
            return ('+', p.expr, p.term)

        @_('term')
        def expr(self, p):
            return p.term

        @_('term TIMES factor')
        def term(self, p):
            return ('*', p.term, p.factor)

        @_('factor')
        def term(self, p):
            return p.factor

        @_('LPAREN expr RPAREN')
        def factor(self, p):
            return p.expr

        @_('NUMBER')
        def factor(self, p):
            return p.NUMBER

        @_('ID')
        def factor(self, p):
            return p.ID

    if __name__ == '__main__':
        text = 'a = 2 + 3 * (4 + 5)'
        lexer = SimpleLexer()
        parser = SimpleParser()
        result = parser.parse(lexer.tokenize(text))
        print(result)

The output of this program is a simplified S-expression like this::

    ('=', 'a', ('+', '2', ('*', '3', ('+', '4', '5'))))

Abstract Syntax Trees
~~~~~~~~~~~~~~~~~~~~~

Processing S-expressions is a bit painful in Python so as an
alternative, you might want to take a more object-oriented approach.
For example, to represent an AST, it is common to define classes for
each kind of node like this::

      class AST(object):
            pass 
 
      class Assignment(AST):
            def __init__(self, location, value):
                self.location = location
                self.value = value

      class BinOp(AST):
            def __init__(self, operator, left, right):
                self.operator = operator
                self.left = left
                self.right = right

      class Number(AST):
            def __init__(self, value):
                self.value = value
            
      class Identifier(AST):
            def __init__(self, name):
                self.name = name

Thus, your abstract syntax tree becomes a series of nodes like this::

             Assignment						     
             /        \		
            /          \						       
     Identifier("a")   BinOp("+") 			       
                     /            \				       
                    /              \				       
               Number(2)       BinOp("*")		       
                                  /      \			       
                                 /        \			       
                          Number(3)    BinOp("+")	       
                                          /     \	       
                                         /       \	       
                                   Number(4)    Number(5)      
          

Viewing Python ASTs
~~~~~~~~~~~~~~~~~~~

The ``ast`` module allows you to create and view abstract syntax trees
built by Python itself.  Try a simple experiment::

    >>> text = "a = 2 + 3 * (4 + 5)"
    >>> import ast
    >>> c = ast.parse(text)
    >>> print(ast.dump(c))
    Module(body=[Assign(targets=[Name(id='a', ctx=Store())], 
           value=BinOp(left=Num(n=2), op=Add(), 
           right=BinOp(left=Num(n=3), op=Mult(), 
           right=BinOp(left=Num(n=4), op=Add(), right=Num(n=5)))))])


Carefully study the output and notice that it is very similar to what's
described above.  Try traversing down into the parse tree yourself::

    >>> c.body
    [<_ast.Assign object at 0x1004a3690>]
    >>> c.body[0].targets
    [<_ast.Name object at 0x1004a36d0>]
    >>> c.body[0].targets[0].id
    'a'
    >>> c.body[0].value
    <_ast.BinOp object at 0x1004a3710>
    >>> c.body[0].value.left
    <_ast.Num object at 0x1004a3750>
    >>> c.body[0].value.left.n
    2
    >>> c.body[0].value.right
    <_ast.BinOp object at 0x1004a3790>
    >>> c.body[0].value.right.op
    <_ast.Mult object at 0x10049f790>
    >>> c.body[0].value.right.left
    <_ast.Num object at 0x1004a37d0>
    >>> c.body[0].value.right.right
    <_ast.BinOp object at 0x1004a3810>
    >>> 

Building an AST with SLY
~~~~~~~~~~~~~~~~~~~~~~~~

Make a file ``simpleast.py`` and put the class definitions defined earlier in it.  
Now, change the code in ``simpleparse.py`` so that it looks like this::

    # simpleparse.py

    from sly import Parser
    from simplelex import SimpleLexer
    from simpleast import *

    class SimpleParser(Parser):
        # Specify the tokens set (terminals)

        tokens = SimpleLexer.tokens

        # Grammar:
        #
        # assignment ::=  ID ASSIGN expr 
        #
        # expr       ::= expr PLUS term
        #             |  term
        #
        # term       ::= term TIMES factor
        #             |  factor
        #
        # factor     ::= LPAREN expr RPAREN
        #             |  NUMBER
        #             |  ID

        @_('ID ASSIGN expr')
        def assignment(self, p):
            return Assignment(p.ID, p.expr)

        @_('expr PLUS term')
        def expr(self, p):
	    return BinOp('+', p.expr, p.term)

        @_('term')
        def expr(self, p):
	    return p.term

        @_('term TIMES factor')
        def term(self, p):
            return BinOp('*', p.term, p.factor)

        @_('factor')
        def term(self, p):
            return p.factor

        @_('LPAREN expr RPAREN')
        def factor(self, p):
            return p.expr

        @_('NUMBER')
        def factor(self, p):
            return Number(p.NUMBER)

        @_('ID')
        def factor(self, p):
            return Identifier(p.ID)

    if __name__ == '__main__':
        text = 'a = 2 + 3 * (4 + 5)'
        lexer = SimpleLexer()
        parser = SimpleParser()
        result = parser.parse(lexer.tokenize(text))
        print(result)

In this version, the different methods are programmed to create and/or propagate
an AST node element. For example, if you have a grammar rule like this::
  
     expr : expr PLUS term

that turns into a method::

     @_('expr PLUS term')
     def expr(self, p):
         return BinOp('+', p.expr, p.term)

The ``p`` argument to the ``expr()`` contains the values of
the symbols on the right hand side. Access to ``p.expr`` returns the
left side of the ``+`` operator.  ``p.term`` returns the right side of
the ``+`` operator.

If you run this program, you'll get a result that looks like this::

    <simpleast.Assignment object at 0x100b8b2b0>

That's not the most friendly output. Maybe add a few print statements
to drill down into the data structure::

    print('location:', result.location)
    print('value:', result.value)

Spend a few minutes playing around with the structure.  Try the same
sort of navigation that you did with the Python AST.

One critical note concerns the ordering of rules in the grammar
specification.  SLY always treats the first decorated rule (i.e., the
first method with `@_(...)` as the "top" of the grammar.   Generally
this will be the highest level construct such as the entire program.

You're now ready to move on to Project 2.








