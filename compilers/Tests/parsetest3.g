/* parsetest3.g

   Add support for var and const declarations.   Do this, you'll
   need to add AST nodes for each declaration type.  For example:

    class ConstDeclaration(Statement):
        '''
        const name = value ;
        '''
        name  : str
        value : Expression

    class VarDeclaration(Statement):
        '''
        var name datatype [ = value ];
        '''
        name     : str
        datatype : DataType
        value    : (Expression, type(None))    # Optional

   Variable declarations are tricky because they introduce the concept
   of a datatype and they also have an optional value.  To handle the
   optional value, you'll need to allow an expression or None as shown above.
   To handle datatypes, you'll want to introduce a few more AST nodes:

    class DataType(AST):
        pass

    class SimpleType(DataType):
        name : str

*/

const pi = 3.14159;
const pi = 3.14158;
print 3;

var x int;
var y int = 23*45;


