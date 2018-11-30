# simpleast.py


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
