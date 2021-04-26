from tpp.Tree import Tree
from tpp.SemanticTree import *


S = SemanticTypes
A = AssignmentTypes
O = OperationTypes
T = TypeTypes


class SemanticContext:
    def __init__(self, scope, parent=None):
        self.scope = scope

        self.functions = {}
        self.variables = {}

        self.parent = parent

    def declare_variable(self, decl):
        self.variables[decl.name] = decl

    def declare_function(self, decl):
        self.functions[decl.name] = decl

    def variable_initialized(self, name):
        # Mark the variable as initialized in the closest context
        var = self.get_variable(name)
        if var:
            var.initialized = True

    def variable_is_declared_local(self, name):
        # Check if the variable was declared in the current context
        return bool(self.variables.get(name))

    def variable_is_declared(self, name):
        # Check if the variable was declared in the closest context
        return bool(self.get_variable(name))

    def variable_is_initialized(self, name):
        # Check if the variable was initialized in the closest context
        var = self.get_variable(name)
        return var and var.initialized

    def is_global(self):
        return self.parent is None

    def get_function_name(self):
        if self.parent is None:
            return None
        if self.parent.parent is None:
            return self.scope
        return self.parent.get_function_name()

    def get_variable(self, name):
        if self.variable_is_declared_local(name):
            return self.variables[name]
        elif self.parent is not None:
            return self.parent.get_variable(name)
        else:
            return None


class SemanticErrors:
    AST_MALFORMED = "AST_MALFORMED"
    MAIN_NOT_FOUND = "MAIN_NOT_FOUND"
    CALL_UNDECLARED_FUNCTION = "CALL_UNDECLARED_FUNCTION"

    ASSIGN_VARIABLE_UNDECLARED = "ASSIGN_VARIABLE_UNDECLARED"
    USING_VARIABLE_UNDECLARED = "USING_VARIABLE_UNDECLARED"
    USING_VARIABLE_UNINITILIZED = "USING_VARIABLE_UNINITILIZED"
    MULTIPLE_VARIABLE_DECLARATION = "MULTIPLE_VARIABLE_DECLARATION"

    NEGATIVE_VECTOR_SIZE = "NEGATIVE_VECTOR_SIZE"

    WRONG_NUMBER_OF_PARAMETERS = "WRONG_NUMBER_OF_PARAMETERS"
    TYPE_ERROR_ON_FUNCTION_CALL = "TYPE_ERROR_ON_FUNCTION_CALL"
    MULTIPLE_FUNCTION_DECLARATION = "MULTIPLE_FUNCTION_DECLARATION"
    RETURN_VALUE_ON_VOID_FUNCTION = "RETURN_VALUE_ON_VOID_FUNCTION"
    RETURN_NONE_ON_TYPED_FUNCTION = "RETURN_NONE_ON_TYPED_FUNCTION"

    NO_INITIALIZE_STATIC_ARRAY = "NO_INITIALIZE_STATIC_ARRAY"
    INVALID_ACESS_INDEX = "INVALID_ACESS_INDEX"
    INVALID_INITIALIZATION_INDEX = "INVALID_INITIALIZATION_INDEX"


SE = SemanticErrors


class SemanticError:
    ERROR_MAP = {
        "AST_MALFORMED": "Erro fatal: Algum problema ocorreu e seu programa não pode ser construído.",
        "MAIN_NOT_FOUND": "Função principal não encontrada.",
        "TYPE_ERROR_ON_FUNCTION_CALL": "Chamada de função com tipos incompatíveis.",
        "ASSIGN_VARIABLE_UNDECLARED": "Tentativa de atribuição em uma variável não declarada.",
        "USING_VARIABLE_UNDECLARED": "Tentativa de utilização de uma variável não declarada.",
        "USING_VARIABLE_UNINITILIZED": "Tentativa de utilização de uma variável não inicializada.",
        "MULTIPLE_VARIABLE_DECLARATION": "Multiplas declarações de uma variável no mesmo escopo.",
        "CALL_UNDECLARED_FUNCTION": "Tentativa de invocar uma função não declarada.",
        "WRONG_NUMBER_OF_PARAMETERS": "Quantidade incorreta de parametros.",
        "NEGATIVE_VECTOR_SIZE": "Tamanho de vetor não deve ser negativo ou nulo (0).",
        "RETURN_VALUE_ON_VOID_FUNCTION": "Existem valores sendo retornados de uma função sem retorno.",
        "RETURN_NONE_ON_TYPED_FUNCTION": "Nenhum valor esta sendo retornado de uma função tipada.",
        "NO_INITIALIZE_STATIC_ARRAY": "Vetores estáticos não deve receber atribuições.",
        "INVALID_ACESS_INDEX": "Tentativa de acessar um índice inválido.",
        "INVALID_INITIALIZATION_INDEX": "Tentativa de inicialização de ponteiro invalida.",
    }

    def __init__(self, name, ctx, info={}):
        self.name = name
        self.ctx = ctx
        self.info = info

    def get_message(self):
        return self.ERROR_MAP[self.name]


class SemanticChecker:
    def __init__(self, ast):
        self.ast = ast
        self.errors = []
        self.program_ctx = SemanticContext("global")

    # utils
    def function_is_declared(self, name):
        return bool(self.program_ctx.functions.get(name))

    def get_function(self, name):
        return self.program_ctx.functions.get(name)
    
    def get_global_variable(self, name):
        return self.program_ctx.variables.get(name)

    # checkers
    def check_variables_type(self, x: Variable, y):
        xn = len(x.indexes)
        yn = len(x.indexes)

        if xn > 0 and (xn != yn or x.typing != y.typing):
            return False

        for xi, yi in zip(x.indexes, y.indexes):
            if xi.t != yi.t:
                if yi.t != S.POINTER:
                    return False
            else:
                if yi.t == S.LITERAL_INTEGER:
                    if yi.value != xi.value:
                        return False

        return True

    def check_index_access(self, decl: LiteralVariable, ctx):
        name = decl.name
        var = ctx.get_variable(name)

        x = len(var.indexes)
        dim = len(decl.indexes)

        if x < dim:
            raise Exception("Unnimplemented")
        elif x > dim:
            raise Exception("Unnimplemented")
        else:
            # for i in range(x):
            #     vi = var.get_index(i)
            #     di = decl.indexes[i]
            raise Exception("Unnimplemented")

    def check_initialization(self, decl, ctx):
        name = decl.variable.name
        var = ctx.get_variable(name)
        var_dim = len(var.indexes)
        decl_var_dim = len(decl.variable.indexes)

        if var_dim > decl_var_dim:
            maybe_var = decl.expression
            if maybe_var.t == S.LITERAL_VARIABLE:
                var2 = ctx.get_variable(maybe_var.name)
                print(f"{var2=}")
                raise Exception("Unnimplemented")
            else:
                self.errors.append(
                    SemanticError(
                        SE.INVALID_INITIALIZATION_INDEX,
                        ctx,
                        {
                            "variable": name,
                        },
                    )
                )
        elif var_dim < decl_var_dim:
            self.errors.append(
                SemanticError(
                    SE.INVALID_ACESS_INDEX,
                    ctx,
                    {
                        "variable": name,
                        "dimention_check": {
                            "expect": var_dim,
                            "result": decl_var_dim,
                        },
                    },
                )
            )
        else:
            ctx.variable_initialized(name)
            self.check_expression(decl.expression, ctx)

            "TODO: check typing"

    def check_assignment(self, decl, ctx):
        """
        [ ]: Check literal integer less then index length
        [ ]: Check if pointers are initialized
        """
        name = decl.variable.name

        if not ctx.variable_is_declared(name):
            # check variable declaration
            self.errors.append(
                SemanticError(
                    SE.ASSIGN_VARIABLE_UNDECLARED,
                    ctx,
                    {"variable": name, "assign": decl},
                )
            )
        else:
            if decl.assignment == A.INITIALIZE:
                self.check_initialization(decl, ctx)
            elif not ctx.variable_is_initialized(name):
                # check variable initialization
                self.errors.append(
                    SemanticError(
                        SE.USING_VARIABLE_UNINITILIZED,
                        ctx,
                        {"variable": name, "assign": decl},
                    )
                )
            else:
                self.check_expression(decl.expression, ctx)

    def check_expression(self, decl, ctx):
        if decl.t == S.LITERAL_INTEGER:
            pass
        elif decl.t == S.LITERAL_FLOAT:
            pass
        elif decl.t == S.LITERAL_VARIABLE:
            name = decl.name

            if not ctx.variable_is_declared(name):
                # check variable declaration
                self.errors.append(
                    SemanticError(
                        SE.USING_VARIABLE_UNDECLARED,
                        ctx,
                        {"variable": name, "expression": decl},
                    )
                )
            elif not ctx.variable_is_initialized(name):
                # check variable initialization
                self.errors.append(
                    SemanticError(
                        SE.USING_VARIABLE_UNINITILIZED,
                        ctx,
                        {"variable": name, "expression": decl},
                    )
                )
            elif decl.indexes:
                self.check_index_access(decl, ctx)
                return
                if var_dim != decl_var_dim:
                    self.errors.append(
                        SemanticError(
                            SE.INVALID_ACESS_INDEX,
                            ctx,
                            {
                                "variable": name,
                                "dimention_check": {
                                    "expect": var_dim,
                                    "result": decl_var_dim,
                                },
                            },
                        )
                    )
                else:
                    for i, di in enumerate(decl.indexes):
                        if di.t != S.LITERAL_INTEGER:
                            continue
                        vi = var.get_index(i)
                        di = di.value
                        if vi <= di:
                            self.errors.append(
                                SemanticError(
                                    SE.INVALID_ACESS_INDEX,
                                    ctx,
                                    {"index_access": {"expect": vi, "result": di}},
                                )
                            )
        elif decl.t == S.BINARY_EXPRESSION:
            self.check_expression(decl.first, ctx)
            self.check_expression(decl.second, ctx)
        elif decl.t == S.BINARY_EXPRESSION:
            self.check_expression(decl.variable, ctx)
        elif decl.t == S.UNARY_EXPRESSION:
            self.check_expression(decl.variable, ctx)
        elif decl.t == S.FUNCTION_CALL:
            self.check_function_call(decl, ctx)
        else:
            print(decl.__class__.__name__)
            raise Exception("Unnimplemented")

    def check_body(self, scope, body, outer_ctx):
        ctx = SemanticContext(scope, outer_ctx)

        for decl in body:
            self.dispatch_declaration(decl, ctx)

    def check_function(self, func_decl, outer_ctx):
        ctx = SemanticContext(func_decl.name, outer_ctx)

        for p in func_decl.parameters:
            if self.get_function(p.name):
                # variable shadow function declaration
                raise Exception("Unnimplemented")
            else:
                # collect and shadow variable parameters
                ctx.declare_variable(p)

        for decl in func_decl.body:
            self.dispatch_declaration(decl, ctx)

    def check_function_call(self, decl, ctx):
        name = decl.name
        if self.function_is_declared(name):
            func_decl = self.get_function(name)
            expect_len_parameters = len(func_decl.parameters)
            result_len_parameters = len(decl.parameters)

            if expect_len_parameters != result_len_parameters:
                self.errors.append(
                    SemanticError(
                        SE.WRONG_NUMBER_OF_PARAMETERS,
                        ctx,
                        {
                            "function": name,
                            "length_parameters": {
                                "expect": expect_len_parameters,
                                "result": result_len_parameters,
                            },
                        },
                    )
                )

            for p, dp in zip(decl.parameters, func_decl.parameters):
                var = ctx.get_variable(p.name)
                if not self.check_variables_type(var, dp):
                    self.errors.append(
                        SemanticError(
                            SE.TYPE_ERROR_ON_FUNCTION_CALL,
                            ctx,
                            {
                                "variable": p.name,
                                "type_match": {
                                    "expect": dp.get_type(),
                                    "result": var.get_type(),
                                },
                            },
                        )
                    )
                self.check_expression(p, ctx)
        else:
            self.errors.append(
                SemanticError(
                    SE.CALL_UNDECLARED_FUNCTION,
                    ctx,
                    {"function": name},
                )
            )

    def check_declaration_vars(self, decl, ctx):
        for v in decl.variables:
            if ctx.variable_is_declared_local(v.name):
                # check multiple variable declaration
                self.errors.append(
                    SemanticError(
                        SE.MULTIPLE_VARIABLE_DECLARATION,
                        ctx,
                        {"variable": v.name},
                    )
                )
            elif self.get_function(v.name):
                # variable shadow function declaration
                raise Exception("Unnimplemented")
            else:
                for i in v.indexes:
                    if i.t == S.LITERAL_INTEGER and i.value <= 0:
                        self.errors.append(
                            SemanticError(
                                SE.NEGATIVE_VECTOR_SIZE,
                                ctx,
                                {"variable": v.name, "type": v.get_type()},
                            )
                        )
                    elif i.t == S.POINTER:
                        continue

                # collect variable declaration
                ctx.declare_variable(v)

    def check_return(self, decl, ctx):
        func_name = ctx.get_function_name()
        func: FunctionDeclaration = self.get_function(func_name)

        if func.return_type == T.VOID:
            if decl.expression is not None:
                self.errors.append(
                    SemanticError(SE.RETURN_VALUE_ON_VOID_FUNCTION, ctx, {})
                )
        elif decl.expression is None:
            self.errors.append(
                SemanticError(
                    SE.RETURN_NONE_ON_TYPED_FUNCTION, ctx, {"type": func.return_type}
                )
            )
        else:
            self.check_expression(decl.expression, ctx)

    def dispatch_declaration(self, decl, ctx):
        """
        [X]: FUNCTION_DECLARATION (check)
        [X]: IF_ELSE_DECLARATION (check)
        [X]: REPEAT_DECLARATION (check)
        [X]: ASSIGNMENT (check)
        [X]: RETURN_DECLARATION (check)
        [X]: WRITE (check)
        [X]: READ (check)
        [X]: FUNCTION_CALL (check)
        [X]: VARS_DECLARATION (check, collect)
        """
        if decl.t == S.FUNCTION_DECLARATION:
            self.check_function(decl, ctx)
        elif decl.t == S.VARS_DECLARATION:
            self.check_declaration_vars(decl, ctx)
        elif decl.t == S.REPEAT_DECLARATION:
            self.check_expression(decl.expression, ctx)
            self.check_body("repita", decl.body, ctx)
        elif decl.t == S.IF_ELSE_DECLARATION:
            self.check_expression(decl.if_expression, ctx)
            self.check_body("se", decl.if_body, ctx)
            self.check_body("senão", decl.else_body, ctx)
        elif decl.t == S.ASSIGNMENT:
            self.check_assignment(decl, ctx)
        elif decl.t == S.FUNCTION_CALL:
            self.check_function_call(decl, ctx)
        elif decl.t == S.READ:
            self.check_expression(decl.expression, ctx)
        elif decl.t == S.WRITE:
            self.check_expression(decl.expression, ctx)
        elif decl.t == S.RETURN_DECLARATION:
            self.check_return(decl, ctx)
        else:
            print(decl.__class__.__name__)
            raise Exception("Unnimplemented")

    # checker start
    def check_program(self):
        """
        On program, check and collect:
            [X] FUNCTION_DECLARATION (check, collect, programa)
            [X] VARS_DECLARATION (collect)
            [X] ASSIGNMENT (check, collect)
        """
        ctx = self.program_ctx

        # collect all global functions and variables
        for decl in self.ast.declarations:
            if decl.t == S.FUNCTION_DECLARATION:
                name = decl.name

                if self.function_is_declared(name):
                    # check multiple function declaration
                    self.errors.append(
                        SemanticError(
                            "MULTIPLE_FUNCTION_DECLARATION",
                            ctx,
                            {"function": name},
                        )
                    )
                elif self.get_global_variable(name):
                    # function declaration shadow global variable
                    raise Exception("Unnimplemented")
                else:
                    # collect function declaration
                    ctx.declare_function(decl)
            else:
                self.dispatch_declaration(decl, ctx)

        # All functions and variables was collected before
        # checking the function declaration
        for decl in ctx.functions.values():
            self.check_function(decl, ctx)

        MAIN_NAME = "principal"
        if not self.function_is_declared(MAIN_NAME):
            # check declaration of the main function
            self.errors.append(SemanticError(SE.MAIN_NOT_FOUND, ctx))

    def check(self):
        if self.ast and self.ast.t == S.PROGRAM:
            self.check_program()
        else:
            self.errors.append(SemanticError(SE.AST_MALFORMED, ctx))
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
    GO_AHEAD = ["declaracao", "numero", "literal"]
    BINARY_EXPRESSION = [
        "expressao",
        "expressoes_booleanas",
        "negacao",
        "expressoes_booleanas_primario",
        "expressoes_de_igualdade",
        "expressao_de_igualdade_primario",
        "expressoes_de_comparacao",
        "expressao_de_comparacao_primario",
        "expressao_matematica",
        "soma",
        "produto",
    ]
    VOID_TYPE = Tree("tipo", [Tree("VAZIO", value="vazio")])

    def ignore_nodes(nodes):
        return (c for c in nodes if c.identifier not in IGNORE_NODES)

    def rec(node: Tree):
        cs = node.children
        n = len(cs)

        if node.identifier in BINARY_EXPRESSION:
            if n == 1:
                return rec(cs[0])

            if n == 2:
                first, second = cs

                if second.identifier == "conjuncao_ou_disjuncao":
                    second = second.children[0]

                op, second = second.children
                first = rec(first)
                second = rec(second)

                return Tree("expression", [first, op, second])

        if node.identifier == "literal" and n == 3:  # ( expression )
            return rec(cs[1])

        if node.identifier in GO_AHEAD:
            return rec(cs[0])

        if node.identifier == "tipo":
            return node.children[0]

        cs = ignore_nodes(cs)
        cs = list(map(rec, cs))

        if node.identifier == "funcao_declaracao" and len(cs) == 2:
            cs = [VOID_TYPE] + cs

        return node.update_children(cs)

    return rec(root)


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
    root = simplify_tree(root)

    def rec(node: Tree):
        error = "Unnimplemented"
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
            return UnaryExpression(operation, expression)
        if node.identifier == "expression":
            # Extract values
            first, operation, second = node.children

            # Transform values
            operation = operation_map[operation.identifier]
            first = rec(first)
            second = rec(second)

            # Construct declaration
            return BinaryExpression(operation, first, second)

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
            return LiteralVariable(identifier.value, indexes)
        if node.identifier == "chamada_de_funcao_declaracao":
            # Extract values
            name, parameters = node.children

            # Transform values
            name = name.value
            parameters = [rec(p.children[0]) for p in parameters.children]

            # Construct declaration
            return FunctionCall(name, parameters)

        if node.identifier == "NUMERO_CIENTIFICO":
            return LiteralFloat(float(node.value))
        if node.identifier == "NUMERO_FLUTUANTE":
            return LiteralFloat(float(node.value))
        if node.identifier == "NUMERO_INTEIRO":
            return LiteralInteger(int(node.value))
        if node.identifier == "ID":
            return LiteralVariable(node.value)

        print()
        print(node.str_tree())
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
