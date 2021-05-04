class SemanticTypes:
    PROGRAM = "program"
    VARIABLE = "variable"

    VARS_DECLARATION = "vars_declaration"
    FUNCTION_DECLARATION = "function_declaration"
    IF_ELSE_DECLARATION = "if_else_declaration"
    REPEAT_DECLARATION = "repeat_declaration"
    RETURN_DECLARATION = "return_declaration"

    BINARY_EXPRESSION_LAZY = "binary_expression_lazy"
    UNARY_EXPRESSION_LAZY = "unary_expression_lazy"
    LITERAL_VARIABLE_LAZY = "literal_variable_lazy"
    FUNCTION_CALL_LAZY = "function_call_lazy"

    BINARY_EXPRESSION = "binary_expression"
    UNARY_EXPRESSION = "unary_expression"

    FUNCTION_CALL = "function_call"
    ASSIGNMENT = "assignment"
    PARAMETER = "parameter"
    LITERAL = "literal"
    POINTER = "pointer"

    WRITE = "write"
    READ = "read"

    LITERAL_CHARACTERS = "literal_characters"
    LITERAL_VARIABLE = "literal_variable"
    LITERAL_INTEGER = "literal_integer"
    LITERAL_FLOAT = "literal_float"


class AssignmentTypes:
    INITIALIZE = "initialize"
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"


class OperationTypes:
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    GRANTER = "granter"
    LESS = "less"
    GRANTER_EQUAL = "granter_equal"
    LESS_EQUAL = "less_equal"
    EQUAL = "equal"
    DIFFERENT = "different"


class TypeTypes:
    FLOAT = "float"
    INTEGER = "integer"
    TEXT = "text"
    VOID = "void"


# Specialized Types 

class Program:
    t = SemanticTypes.PROGRAM

    def __init__(self, declarations):
        self.declarations = declarations


class Variable:
    t = SemanticTypes.VARIABLE

    def __init__(self, typing, name, indexes, initialized):
        self.typing = typing
        self.name = name
        self.indexes = indexes
        self.initialized = initialized

    def get_type(self):
        def map_index(i):
            return f"[{'' if i.t == SemanticTypes.POINTER else i.value}]"

        return self.typing + "".join(map(map_index, self.indexes))

    def check_indexes(self):
        def check_index(index):
            if index.t == SemanticTypes.POINTER:
                return True
            if index.t == SemanticTypes.LITERAL_INTEGER:
                return index.value > 0
            return False

        return all(map(check_index, self.indexes))

    def get_index(self, i):
        index = self.indexes[i]
        if index.t == SemanticTypes.POINTER:
            return index.length
        if index.t == SemanticTypes.LITERAL_INTEGER:
            return index.value


class VarsDeclaration:
    t = SemanticTypes.VARS_DECLARATION

    def __init__(self, variables):
        self.variables = variables


class FunctionDeclaration:
    t = SemanticTypes.FUNCTION_DECLARATION

    def __init__(self, return_type, name, parameters, body):
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.body = body


class AssignmentDeclaration:
    t = SemanticTypes.ASSIGNMENT

    def __init__(self, variable, assignment, expression):
        self.variable = variable
        self.assignment = assignment
        self.expression = expression


class Write:
    t = SemanticTypes.WRITE

    def __init__(self, expression):
        self.expression = expression


class Read:
    t = SemanticTypes.READ

    def __init__(self, expression):
        self.expression = expression


class Pointer:
    t = SemanticTypes.POINTER

    def __init__(self):
        self.initialized = False
        self.length = 0


# Lazy Expressions

class FunctionCallLazy:
    t = SemanticTypes.FUNCTION_CALL_LAZY

    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters
    
    def set_typing(self, typing):
        return FunctionCall(typing, self.name, self.parameters)


class BinaryExpressionLazy:
    t = SemanticTypes.BINARY_EXPRESSION_LAZY

    def __init__(self, operation, first, second):
        self.operation = operation
        self.first = first
        self.second = second


class UnaryExpressionLazy:
    t = SemanticTypes.UNARY_EXPRESSION_LAZY

    def __init__(self, operation, variable):
        self.operation = operation
        self.variable = variable


class LiteralVariableLazy:
    t = SemanticTypes.LITERAL_VARIABLE_LAZY

    def __init__(self, name, indexes):
        self.name = name
        self.indexes = indexes
    
    def set_typing(self, typing):
        return LiteralVariable(typing, self.name, self.indexes)


# Expressions

class FunctionCall:
    t = SemanticTypes.FUNCTION_CALL

    def __init__(self, typing, name, parameters):
        self.typing = typing
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

    def __init__(self, operation, first, second, typing):
        self.operation = operation
        self.first = first
        self.second = second
        self.typing = typing


class UnaryExpression:
    t = SemanticTypes.UNARY_EXPRESSION

    def __init__(self, operation, variable, typing):
        self.operation = operation
        self.variable = variable
        self.typing = typing


class LiteralVariable:
    t = SemanticTypes.LITERAL_VARIABLE

    def __init__(self, typing, name, indexes):
        self.typing = typing
        self.name = name
        self.indexes = indexes


class LiteralInteger:
    t = SemanticTypes.LITERAL_INTEGER

    def __init__(self, value):
        self.value = value
        self.typing = TypeTypes.INTEGER


class LiteralFloat:
    t = SemanticTypes.LITERAL_FLOAT

    def __init__(self, value):
        self.value = value
        self.typing = TypeTypes.FLOAT


class LiteralCharacters:
    t = SemanticTypes.LITERAL_CHARACTERS

    def __init__(self, value):
        self.value = value
        self.typing = TypeTypes.TEXT

