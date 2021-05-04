from tpp.Semantic.Checker import *
from tpp.Semantic.simplify_tree import *


def semantic_preprocessor(root):
    type_map = {
        "flutuante": T.FLOAT,
        "inteiro": T.INTEGER,
        "texto": T.TEXT,
        "vazio": T.VOID,
    }
    assignment_map = {
        "ATRIBUICAO": A.INITIALIZE,
        "ADICAO_ATRIBUICAO": A.ADD,
        "SUBTRACAO_ATRIBUICAO": A.SUBTRACT,
        "MULTIPLICACAO_ATRIBUICAO": A.MULTIPLY,
        "DIVISAO_ATRIBUICAO": A.DIVIDE,
    }
    operation_map = {
        "ADICAO": O.ADD,
        "SUBTRACAO": O.SUBTRACT,
        "MULTIPLICACAO": O.MULTIPLY,
        "DIVISAO": O.DIVIDE,
        "MAIOR": O.GRANTER,
        "MENOR": O.LESS,
        "MAIORIGUAL": O.GRANTER_EQUAL,
        "MAIORIGUAL": O.LESS_EQUAL,
        "IGUAL": O.EQUAL,
        "DIFERENTE": O.DIFFERENT,
    }

    def rec(node: Tree):
        if node.identifier == "programa":
            # Extract values
            program_list = node.children[0]

            # Transform values
            declarations = [rec(c) for c in program_list.children]

            # Construct declaration
            return Program(declarations)

        if node.identifier == "funcao_declaracao":
            # Extract values
            return_type, header, body = node.children
            name, parameters = header.children

            # Transform values
            return_type = type_map[return_type.value]
            name = name.value

            # parameters: [Tree] -> Gen<[Tree]> -> Gen<(string, LiteralVariable)> -> [Variable]
            parameters = [] if len(parameters.children) == 1 else parameters.children
            parameters = (p.children for p in parameters)
            parameters = ((type_map[cs[0].value], rec(cs[1])) for cs in parameters)
            parameters = [Variable(t, v.name, v.indexes, True) for t, v in parameters]
            body = [rec(c) for c in body.children]

            # Construct declaration
            return FunctionDeclaration(return_type, name, parameters, body)
        if node.identifier == "criacao_de_variaveis_declaracao":
            # Extract values
            typing, variables = node.children

            # Transform values
            typing = type_map[typing.value]

            # variables: Gen<[Tree]> -> Gen<(string, [Tree])> -> [Variable]
            variables = (v.children for v in variables.children)
            variables = ((cs[0].value, list(map(rec, cs[1:]))) for cs in variables)
            variables = [
                Variable(typing, name, indexes, bool(indexes))
                for name, indexes in variables
            ]

            # Construct declaration
            return VarsDeclaration(variables)
        if node.identifier == "atribuicao_declaracao":
            # Extract values
            variable, assignment, expression = node.children

            # Transform values
            variable = rec(variable)
            assignment = assignment_map[assignment.identifier]
            expression = rec(expression)

            # Construct declaration
            return AssignmentDeclaration(variable, assignment, expression)
        if node.identifier == "se_declaracao":
            # Extract values
            if len(node.children) == 3:
                if_expression, if_body, else_body = node.children
                else_body = else_body.children
            else:
                if_expression, if_body = node.children
                else_body = []

            # Transform values
            if_expression = rec(if_expression)
            if_body = [rec(c) for c in if_body.children]
            else_body = [rec(c) for c in else_body]

            # Construct declaration
            return IfElseDeclaration(if_expression, if_body, else_body)
        if node.identifier == "repita_declaracao":
            # Extract values
            body, expression = node.children

            # Transform values
            body = [rec(c) for c in body.children]
            expression = rec(expression)

            # Construct declaration
            return RepeatDeclaration(body, expression)
        if node.identifier == "retorna_declaracao":
            if node.children:
                # Extract values
                expression = node.children[0]

                # Transform values
                expression = rec(expression)
            else:
                expression = None

            # Construct declaration
            return ReturnDeclaration(expression)

        if node.identifier == "escreva":
            return Write(rec(node.children[0]))
        if node.identifier == "leia":
            return Read(rec(node.children[0]))

        if node.identifier == "expressao_unaria":
            # Extract values
            operation, expression = node.children

            # Transform values
            operation = operation_map[operation.identifier]
            expression = rec(expression)
            if expression.t in [S.LITERAL_INTEGER, S.LITERAL_FLOAT]:
                expression.value = -expression.value
                return expression

            # Construct declaration
            return UnaryExpressionLazy(operation, expression)
        if node.identifier == "expression":
            # Extract values
            first, operation, second = node.children

            # Transform values
            operation = operation_map[operation.identifier]
            first = rec(first)
            second = rec(second)

            # Construct declaration
            return BinaryExpressionLazy(operation, first, second)

        if node.identifier == "ponteiro":
            return Pointer()
        if node.identifier == "vetor":
            return rec(node.children[0])
        if node.identifier == "var":
            # Extract values
            identifier, *indexes = node.children

            # Transform values
            indexes = [rec(c) for c in indexes]

            # Construct declaration
            return LiteralVariableLazy(identifier.value, indexes)
        if node.identifier == "chamada_de_funcao_declaracao":
            # Extract values
            name, parameters = node.children

            # Transform values
            name = name.value
            parameters = [rec(p.children[0]) for p in parameters.children if p.children]

            # Construct declaration
            return FunctionCallLazy(name, parameters)

        if node.identifier == "NUMERO_CIENTIFICO":
            return LiteralFloat(float(node.value))
        if node.identifier == "NUMERO_FLUTUANTE":
            return LiteralFloat(float(node.value))
        if node.identifier == "NUMERO_INTEIRO":
            return LiteralInteger(int(node.value))
        if node.identifier == "ID":
            return LiteralVariableLazy(node.value, [])
        if node.identifier == "CARACTERES":
            return LiteralCharacters(node.value)

        print()
        print(node.str_tree())
        print()
        print(node, node.children, node.value)
        print()
        raise Exception("Unimplemented")

    return None if root is None else rec(root)


def semantic_check(root):
    if root is not None:
        root = simplify_tree(root)
        root = semantic_preprocessor(root)
        return SemanticChecker().check(root)
