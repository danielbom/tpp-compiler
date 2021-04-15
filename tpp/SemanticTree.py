class SemanticTypes:
    PROGRAM = "program"
    VARIABLE = "variable"

    VARS_DECLARATION = "vars_declaration"
    FUNCTION_DECLARATION = "function_declaration"
    IF_ELSE_DECLARATION = "if_else_declaration"
    REPEAT_DECLARATION = "repeat_declaration"
    RETURN_DECLARATION = "return_declaration"

    BINARY_EXPRESSION = "binary_expression"
    UNARY_EXPRESSION = "unary_expression"

    FUNCTION_CALL = "function_call"
    ASSIGNMENT = "assignment"
    PARAMETER = "parameter"
    LITERAL = "literal"

    WRITE = "write"
    READ = "read"


class AssignmentTypes:
    INITIALIZE = 'initialize'
    ADD = 'add'
    SUBTRACT = 'subtract'
    MULTIPLY = 'multiply'
    DIVIDE = 'divide'


class Program:
    t = SemanticTypes.PROGRAM

    def __init__(self, declarations):
        self.declarations = declarations


class Variable:
    t = SemanticTypes.VARIABLE

    def __init__(self, typing, name):
        self.typing = typing
        self.name = name
        self.initialized = False


class VarsDeclaration:
    t = SemanticTypes.VARS_DECLARATION

    def __init__(self, variables):
        self.variables = variables


class AssignmentDeclaration:
    t = SemanticTypes.ASSIGNMENT

    def __init__(self, variable, assignment, expression):
        self.variable = variable
        self.assignment = assignment
        self.expression = expression


class FunctionDeclaration:
    t = SemanticTypes.FUNCTION_DECLARATION

    def __init__(self, return_type, name, parameters, body):
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.body = body


class FunctionParameter:
    t = SemanticTypes.PARAMETER

    def __init__(self, typing, name):
        self.typing = typing
        self.name = name


class FunctionCall:
    t = SemanticTypes.FUNCTION_CALL

    def __init__(self, name, parameters):
        self.name = name 
        self.parameters = parameters


class IfElseDeclaration:
    t = SemanticTypes.IF_ELSE_DECLARATION

    def __init__(self, if_expression, if_body, else_body):
        self.if_expression = if_expression
        self.if_body = if_body
        self.else_body = else_body


class RepeatDeclaration:
    t = SemanticTypes.REPEAT_DECLARATION

    def __init__(self, body, expression):
        self.body = body
        self.expression = expression


class ReturnDeclaration:
    t = SemanticTypes.RETURN_DECLARATION

    def __init__(self, expression):
        self.expression = expression


class BinaryExpression:
    t = SemanticTypes.BINARY_EXPRESSION

    def __init__(self, operation, first, second):
        self.operation = operation
        self.first = first
        self.second = second


class UnaryExpression:
    t = SemanticTypes.UNARY_EXPRESSION

    def __init__(self, operation, variable):
        self.operation = operation
        self.variable = variable


class Literal:
    t = SemanticTypes.LITERAL

    def __init__(self, identifier, value, indexes = []):
        self.identifier = identifier
        self.value = value
        self.indexes = indexes

class Write:
    t = SemanticTypes.WRITE

    def __init__(self, expression):
        self.expression = expression

class Read:
    t = SemanticTypes.READ

    def __init__(self, expression):
        self.expression = expression
