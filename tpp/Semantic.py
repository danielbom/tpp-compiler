from tpp.Tree import Tree
from tpp.SemanticTree import *


T = SemanticTypes
A = AssignmentTypes


class SemanticContext:
    def __init__(self, parent=None):
        self.functions = {}
        self.variables = {}
        self.sequence = []

        self.parent = parent
        self.children = []

        if parent:
            parent.children.append(self)

    def variable_initialized(self, name):
        # Mark the variable as initialized in the closest context
        if bool(ctx.variables.get(name)):
            ctx.variables[name].initialized = True
        else:
            self.parent.variable_initialized(name)

    def variable_is_declarated(self, name):
        # Check if the variable was declared in the closest context
        if bool(ctx.variables.get(name)):
            return True
        else:
            return self.parent and self.parent.variable_is_declarated(name)

    def variable_is_initialized(self, name):
        # Check if the variable was initialized in the closest context
        if bool(ctx.variables.get(name)):
            return ctx.variables[name].initialized
        else:
            return self.parent and self.parent.variable_is_initialized(name)


class SemanticError:
    def __init__(self, name, info=None):
        self.name = name
        self.info = info


class SemanticChecker:
    def __init__(self, ast):
        self.ast = ast
        self.errors = []
        self.program_ctx = SemanticContext()
    
    def function_is_declarated(self, name):
        return bool(self.program_ctx.functions.get(name))

    def check_expression(self, expression):
        pass

    def check_body(self, body):
        '''
        [ ]: se_declaracao
        [ ]: repita_declaracao
        [ ]: atribuicao_declaracao
        [ ]: retorna_declaracao
        [ ]: escreva_declaracao
        [ ]: leia_declaracao
        [ ]: chamada_de_funcao_declaracao
        [ ]: criacao_de_variaveis_declaracao
        '''
        pass

    def check_function(self, decl, ctx):
        pass

    def check_assignment(self, decl, ctx):
        name = decl.variable

        if not ctx.variable_is_declarated(name):
            # check variable declaration
            self.errors.append(SemanticError("USING_VARIABLE_UNDECLARATED", {
                "variable": name,
                "declaration": decl
            }))

        elif decl.assignment == A.INITIALIZE:
            # collect variable initialization
            ctx.variable_initialized(name)

            'TODO: check typing'

        elif not ctx.variable_is_initialized(name):
            # check variable initialization
            self.errors.append(SemanticError("USING_VARIABLE_UNINITILIZED", {
                "variable": name,
                "declaration": decl
            }))

    def check_program(self):
        '''
        On program, check and collect:
            [X] FUNCTION_DECLARATION (check, collect, programa)
            [X] VARS_DECLARATION (collect)
            [X] ASSIGNMENT (check, collect)
        '''
        ctx = self.program_ctx

        for decl in self.ast.declarations:
            if decl.t == T.FUNCTION_DECLARATION:
                # collect function declaration
                ctx.functions[decl.name] = decl

            elif decl.t == T.VARS_DECLARATION:
                for v in decl.variables:
                    # collect variable declaration
                    ctx.variables[v.name] = v
                    ctx.sequence.append(decl)

            elif decl.t == T.ASSIGNMENT:
                self.check_assignment(decl, ctx)
                ctx.sequence.append(decl)
        
        # All functions and variables was collected before 
        # checking the function declaration
        for decl in ctx.functions.values():
            self.check_function(decl, ctx)

        MAIN_NAME = "programa"
        if not self.function_is_declarated(MAIN_NAME):
            # check declaration of the main function
            self.errors.append(SemanticError("MAIN_NOT_FOUND"))
        else:
            ctx.sequence.append(ctx.functions[MAIN_NAME])

    def check(self):
        if self.ast and self.ast.t == T.PROGRAM:
            self.check_program()
        else:
            self.errors.append(SemanticError("AST_MALFORMED"))
        return self


def simplify_tree(root):
    IGNORE_NODES = [
        "DOIS_PONTOS",
        "VIRGULA",
        "ESCREVA",
        "LEIA",
        "SE",
        "ENTAO",
        "SENAO",
        "REPITA",
        "ATE",
        "RETORNA",
        "PARENTESES_ESQ",
        "PARENTESES_DIR",
        "COLCHETE_ESQ",
        "COLCHETE_DIR",
        "FIM",
    ]
    GO_AHEAD = ['declaracao', 'numero']
    NO_IGNORE_NODES = ['numero']
    VOID_TYPE = Tree('tipo', [Tree('VAZIO', value='vazio')])

    def ignore_nodes(nodes):
        return (c for c in nodes if c.identifier not in IGNORE_NODES)

    def simplify_expression(node: Tree):
        cs = node.children
        n = len(cs)

        if node.identifier in GO_AHEAD:
            return simplify_expression(cs[0])
        if node.identifier.endswith('primario'):
            return simplify_expression(cs[0])
        if node.identifier == 'expressao_matematica':
            return simplify_expression(cs[0])
        if node.identifier == 'literal':
            return simplify_expression(cs[1] if n == 3 else cs[0]) 
        if node.identifier == 'expressao_unaria':
            if cs[1].identifier == 'literal':
                op, literal = cs
                maybe_number = literal.children[0]
                if maybe_number.identifier == 'numero':
                    number = maybe_number.children[0]
                    value = op.value + number.value
                    any_number = Tree(number.identifier, value=value)
                    return any_number
            return Tree(node.identifier, [cs[0], simplify_expression(cs[1])])

        if n == 1:
            return simplify_expression(cs[0])
        if n == 2:
            first, second = cs

            if second.identifier == 'conjuncao_ou_disjuncao':
                second = second.children[0]

            op, second = second.children
            first = simplify_expression(first)
            second = simplify_expression(second)

            return Tree('expression', [first, op, second])

        return node

    def rec(node: Tree):
        if node.identifier in GO_AHEAD:
            return rec(node.children[0])

        if node.identifier == 'expressao':
            return simplify_expression(node.children[0])

        cs = node.children
        cs = ignore_nodes(cs)
        cs = list(map(rec, cs))

        if node.identifier == 'funcao_declaracao' and len(cs) == 2:
            cs = [VOID_TYPE] + cs

        return Tree(node.identifier, cs, node.value)

    return rec(root)


def semantic_preprocessor(root):
    assignment_map = {
        'ATRIBUICAO': A.INITIALIZE,
        'ADICAO_ATRIBUICAO': A.ADD,
        'SUBTRACAO_ATRIBUICAO': A.SUBTRACT,
        'MULTIPLICACAO_ATRIBUICAO': A.MULTIPLY,
        'DIVISAO_ATRIBUICAO': A.DIVIDE
    }
    root = simplify_tree(root)

    def rec(node: Tree):
        error = "Unnimplemented"
        if node.identifier == 'programa':
            # Extract values
            program_list = node.children[0]

            # Transform values
            declarations = [rec(c) for c in program_list.children]

            # Construct declaration
            return Program(declarations)
        if node.identifier == 'funcao_declaracao':
            # Extract values
            return_type, header, body = node.children
            name, parameters = header.children

            # Transform values
            return_type = return_type.children[0].value
            name = name.value
            parameters = ((p.children[0].value, p.children[1].value)
                          for p in parameters.children)
            parameters = [FunctionParameter(*p) for p in parameters]
            body = [rec(c) for c in body.children]

            # Construct declaration
            return FunctionDeclaration(return_type, name,
                                        parameters, body)
        if node.identifier == 'criacao_de_variaveis_declaracao':
            # Extract values
            typing, variables = node.children

            # Transform values
            typing = typing.children[0].value
            variables = (v.children[0].value for v in variables.children)
            variables = [Variable(typing, v) for v in variables]

            # Construct declaration
            return VarsDeclaration(variables)
        if node.identifier == 'atribuicao_declaracao':
            # Extract values
            variable, assignment, expression = node.children

            # Transform values
            variable = variable.children[0].value
            assignment = assignment_map[assignment.identifier]
            expression = rec(expression)

            # Construct declaration
            return AssignmentDeclaration(variable, assignment, expression)
        if node.identifier == 'se_declaracao':
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
        if node.identifier == 'repita_declaracao':
            # Extract values
            body, expression = node.children

            # Transform values
            body = [rec(c) for c in body.children]
            expression = rec(expression)

            # Construct declaration
            return RepeatDeclaration(body, expression)
        if node.identifier == 'retorna_declaracao':
            # Extract values
            expression = node.children[0]

            # Transform values
            expression = rec(expression)

            # Construct declaration
            return ReturnDeclaration(expression)
        if node.identifier == 'expressao_unaria':
            # Extract values
            operation, expression = node.children

            # Transform values
            operation = operation.identifier.lower()
            expression = rec(expression)

            # Construct declaration
            return UnaryExpression(operation, expression)
        if node.identifier == 'expression':
            first, operation, second = node.children

            operation = operation.identifier.lower()
            first = rec(first)
            second = rec(second)

            return BinaryExpression(operation, first, second)
        if node.identifier == 'NUMERO_CIENTIFICO':
            return Literal('flutuante', float(node.value))
        if node.identifier == 'NUMERO_FLUTUANTE':
            return Literal('flutuante', float(node.value))
        if node.identifier == 'NUMERO_INTEIRO':
            return Literal('inteiro', int(node.value))
        if node.identifier == 'ID':
            return Literal('variable', node.value)

        print()
        print(node, node.children, node.value)
        print()
        raise Exception(error)

    return None if root is None else rec(root)


def semantic_check(root):
    if root is not None:
        root = simplify_tree(root)
        root = semantic_preprocessor(root)
        semantic_checker = SemanticChecker(root)
        return semantic_checker.check()
