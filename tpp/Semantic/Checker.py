from tpp.Semantic.Context import *
from tpp.Semantic.Tree import *
from tpp.Semantic.Errors import *
from tpp.Semantic.Warnings import *


S = SemanticTypes
A = AssignmentTypes
O = OperationTypes
T = TypeTypes

SE = SemanticErrors
SW = SemanticWarnings


class SemanticChecker:
    def __init__(self):
        self.ast = None
        self.errors = []
        self.warnings = []
        self.program_ctx = SemanticContext("global")

    # utils
    def iterate_over_body(self, body):
        for decl in body:
            if decl.t == S.IF_ELSE_DECLARATION:
                yield from self.iterate_over_body(decl.if_body)
                yield from self.iterate_over_body(decl.else_body)
            elif decl.t == S.REPEAT_DECLARATION:
                yield from self.iterate_over_body(decl.body)
            else:
                yield decl

    def function_is_declared(self, name):
        return bool(self.program_ctx.functions.get(name))

    def get_function(self, name):
        return self.program_ctx.functions.get(name)

    def get_global_variable(self, name):
        return self.program_ctx.variables.get(name)

    # checkers
    def check_function_main_exists(self):
        ctx = self.program_ctx

        MAIN_NAME = "principal"
        if not self.function_is_declared(MAIN_NAME):
            # check declaration of the main function
            self.errors.append(SemanticError(SE.MAIN_NOT_FOUND, ctx))
        else:
            main = self.get_function(MAIN_NAME)

            calls = self.iterate_over_body(main.body)
            calls = (d for d in calls if d.t == S.FUNCTION_CALL)

            if any(d.name == MAIN_NAME for d in calls):
                self.warnings.append(SemanticWarning(SW.MAIN_CALL_ITSELF, ctx))

    def check_variable_usage(self, ctx):
        for v in ctx.variables.values():
            if not v.initialized:
                self.warnings.append(
                    SemanticWarning(
                        SW.VARIABLE_NEVER_INITIALIZED, ctx, {"variable": v.name}
                    )
                )
            elif not v.used:
                self.warnings.append(
                    SemanticWarning(SW.VARIABLE_NEVER_USED, ctx, {"variable": v.name})
                )

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
            raise Exception("Unimplemented")
        elif x > dim:
            raise Exception("Unimplemented")
        elif x == 0:
            pass
        else:
            for i in range(x):
                vi = var.get_index(i)
                di = decl.indexes[i]
                print(f"{vi=}")
                print(f"{di=}")
            # raise Exception("Unimplemented")

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
                raise Exception("Unimplemented")
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
                    SE.INVALID_ACCESS_INDEX,
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
            e = decl.expression

            if var.typing != e.typing:
                self.warnings.append(
                    SemanticWarning(
                        SW.IMPLICIT_CAST,
                        ctx,
                        {
                            "variable": name,
                            "type_match": {"expect": var.typing, "result": e.typing},
                        },
                    )
                )

    def check_assignment(self, decl, ctx):
        """
        [X]: Check literal integer less then index length
        [ ]: Check if pointers are initialized
        """
        decl.variable = self.check_expression(decl.variable, ctx)
        decl.expression = self.check_and_mark_expression(decl.expression, ctx)
        name = decl.variable.name

        if ctx.variable_is_declared(name):
            if decl.assignment == A.INITIALIZE:
                self.check_initialization(decl, ctx)
            elif not ctx.variable_is_initialized(name):
                # check variable initialization
                self.errors.append(
                    SemanticError(
                        SE.USING_VARIABLE_UNINITIALIZED,
                        ctx,
                        {"variable": name, "assign": decl},
                    )
                )
        else:
            # check variable declaration
            self.errors.append(
                SemanticError(
                    SE.ASSIGN_VARIABLE_UNDECLARED,
                    ctx,
                    {"variable": name, "assign": decl},
                )
            )

    def apply_operation(self, operation, first, second):
        if operation == O.ADD:
            return first.value + second.value
        if operation == O.SUBTRACT:
            return first.value - second.value
        if operation == O.MULTIPLY:
            return first.value * second.value
        if operation == O.DIVIDE:
            if first.t == S.LITERAL_INTEGER:
                if second.t == S.LITERAL_INTEGER:
                    return first.value // second.value
            return first.value / second.value

        raise Exception("Unimplemented")

    def simplify_literal(self, op, first, second):
        lit = None
        if op in [O.ADD, O.SUBTRACT, O.MULTIPLY, O.DIVIDE]:
            if first.t == S.LITERAL_INTEGER:
                if second.t == S.LITERAL_INTEGER:
                    lit = LiteralInteger
                if second.t == S.LITERAL_FLOAT:
                    lit = LiteralFloat
            if first.t == S.LITERAL_FLOAT:
                if second.t == S.LITERAL_FLOAT:
                    lit = LiteralFloat
                if second.t == S.LITERAL_INTEGER:
                    lit = LiteralFloat

        return lit(self.apply_operation(op, first.value, second.value)) if lit else None

    def extract_typing(self, first, second):
        t1 = first.typing
        t2 = second.typing

        if t1 is None or t2 is None:
            return None

        if t1 == T.INTEGER:
            if t2 == T.INTEGER:
                return T.INTEGER
            if t2 == T.FLOAT:
                return T.FLOAT

        if t1 == T.FLOAT:
            if t2 == T.INTEGER:
                return T.FLOAT
            if t2 == T.FLOAT:
                return T.FLOAT

        raise Exception("Unimplemented")

    def _check_expression(self, decl, ctx, mark_used):
        if decl.t == S.LITERAL_VARIABLE_LAZY:
            # Get current variable declaration
            var = ctx.get_variable(decl.name)

            if var is None:
                self.errors.append(
                    SemanticError(
                        SE.USING_VARIABLE_UNDECLARED, ctx, {"variable": decl.name}
                    )
                )

                return decl.set_typing(None)

            if mark_used:
                var.used = True

            # Update variable typing
            lit = decl.set_typing(var.typing)

            # Update variable declaration on context
            return lit
        elif decl.t == S.BINARY_EXPRESSION_LAZY:
            first = self._check_expression(decl.first, ctx, mark_used)
            second = self._check_expression(decl.second, ctx, mark_used)

            maybe_decl = self.simplify_literal(decl.operation, first, second)
            if maybe_decl:
                return maybe_decl

            typing = self.extract_typing(first, second)

            return BinaryExpression(decl.operation, first, second, typing)
        elif decl.t == S.UNARY_EXPRESSION_LAZY:
            variable = self._check_expression(decl.variable, ctx, mark_used)

            # TODO: Check if variable is numeric

            return UnaryExpression(decl.operation, variable, variable.typing)
        elif decl.t == S.FUNCTION_CALL_LAZY:
            func = self.get_function(decl.name)
            return decl.set_typing(None if func is None else func.return_type)

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
                        SE.USING_VARIABLE_UNINITIALIZED,
                        ctx,
                        {"variable": name, "expression": decl},
                    )
                )
            elif decl.indexes:
                self.check_index_access(decl, ctx)

            return decl
        elif decl.t == S.FUNCTION_CALL:
            return self.check_function_call(decl, ctx)
        elif decl.t == S.LITERAL_INTEGER:
            pass
        elif decl.t == S.LITERAL_FLOAT:
            pass
        elif decl.t == S.BINARY_EXPRESSION:
            pass
        elif decl.t == S.UNARY_EXPRESSION:
            pass
        else:
            print(decl.__dict__)
            print(decl.__class__.__name__)
            raise Exception("Unimplemented")

        return decl

    def check_expression(self, decl, ctx):
        return self._check_expression(decl, ctx, False)

    def check_and_mark_expression(self, decl, ctx):
        return self._check_expression(decl, ctx, True)

    def check_body(self, scope, body, outer_ctx):
        ctx = SemanticContext(scope, outer_ctx)

        for decl in body:
            self.dispatch_declaration(decl, ctx)

        self.check_variable_usage(ctx)

    def check_and_declare_variable(self, var, ctx):
        if ctx.variable_is_declared_local(var.name):
            # check multiple variable declaration
            self.errors.append(
                SemanticError(
                    SE.MULTIPLE_VARIABLE_DECLARATION,
                    ctx,
                    {"variable": var.name},
                )
            )
        elif self.function_is_declared(var.name):
            # check shadow function declaration
            self.error.append(
                SemanticError(
                    SE.SYMBOL_ALREADY_EXISTS,
                    ctx,
                    {"variable": var.name},
                )
            )
        else:
            for i in var.indexes:
                if i.t == S.LITERAL_INTEGER and i.value <= 0:
                    self.errors.append(
                        SemanticError(
                            SE.NEGATIVE_VECTOR_SIZE,
                            ctx,
                            {"variable": var.name, "type": var.get_type()},
                        )
                    )
                elif i.t == S.LITERAL_FLOAT:
                    self.errors.append(
                        SemanticError(
                            SE.INVALID_INDEX_VALUE,
                            ctx,
                            {"variable": var.name, "type": var.get_type()},
                        )
                    )
                elif i.t == S.POINTER:
                    continue

            # collect variable declaration
            ctx.declare_variable(var)

    def check_function(self, func, outer_ctx):
        ctx = SemanticContext(func.name, outer_ctx)

        for p in func.parameters:
            self.check_and_declare_variable(p, ctx)

        body = [self.dispatch_declaration(decl, ctx) for decl in func.body]

        self.check_variable_usage(ctx)

        calls = self.iterate_over_body(func.body)
        calls = [d for d in calls if d.t == S.RETURN_DECLARATION]

        if func.return_type == T.VOID:
            if calls:
                self.errors.append(
                    SemanticError(
                        SE.RETURN_VALUE_ON_VOID_FUNCTION, ctx, {"function": func.name}
                    )
                )
        else:
            if not calls:
                self.errors.append(
                    SemanticError(
                        SE.RETURN_NONE_ON_TYPED_FUNCTION,
                        ctx,
                        {"type": func.return_type},
                    )
                )

        return FunctionDeclaration(func.return_type, func.name, func.parameters, body)

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

            # Check and transform parameters
            parameters = [self.check_expression(p, ctx) for p in decl.parameters]

            for p, dp in zip(parameters, func_decl.parameters):
                if dp.typing != p.typing:
                    self.warnings.append(
                        SemanticWarning(
                            SW.IMPLICIT_FLOAT,
                            ctx,
                            {
                                "variable": dp.name,
                                "type_match": {
                                    "expect": dp.typing,
                                    "result": p.typing,
                                },
                            },
                        )
                    )

                if p.t == S.FUNCTION_CALL:
                    # Safe get declared function
                    if self.function_is_declared(p.name):
                        func = self.get_function(p.name)

                        if func.return_type != dp.typing:
                            self.warnings.append(
                                SemanticWarning(
                                    SW.IMPLICIT_FLOAT,
                                    ctx,
                                    {
                                        "variable": dp.name,
                                        "type_match": {
                                            "expect": dp.typing,
                                            "result": func.return_type,
                                        },
                                    },
                                )
                            )

            return FunctionCall(name, parameters, decl.typing)
        else:
            self.errors.append(
                SemanticError(
                    SE.CALL_UNDECLARED_FUNCTION,
                    ctx,
                    {"function": name},
                )
            )

    def check_return(self, decl, ctx):
        func_name = ctx.get_function_name()
        func: FunctionDeclaration = self.get_function(func_name)

        if func.return_type == T.VOID:
            if decl.expression is not None:
                self.errors.append(
                    SemanticError(
                        SE.RETURN_VALUE_ON_VOID_FUNCTION, ctx, {"function": func_name}
                    )
                )
        elif decl.expression is None:
            self.errors.append(
                SemanticError(
                    SE.RETURN_NONE_ON_TYPED_FUNCTION, ctx, {"type": func.return_type}
                )
            )
        else:
            expression = self.check_and_mark_expression(decl.expression, ctx)
            return ReturnDeclaration(expression)

        return decl

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
            return self.check_function(decl, ctx)
        elif decl.t == S.VARS_DECLARATION:
            for v in decl.variables:
                self.check_and_declare_variable(v, ctx)
            return decl
        elif decl.t == S.REPEAT_DECLARATION:
            expression = self.check_and_mark_expression(decl.expression, ctx)
            body = self.check_body("repeat", decl.body, ctx)
            return RepeatDeclaration(expression, body)
        elif decl.t == S.IF_ELSE_DECLARATION:
            if_expression = self.check_and_mark_expression(decl.if_expression, ctx)
            if_body = self.check_body("if", decl.if_body, ctx)
            else_body = self.check_body("else", decl.else_body, ctx)
            return IfElseDeclaration(if_expression, if_body, else_body)
        elif decl.t == S.ASSIGNMENT:
            return self.check_assignment(decl, ctx)
        elif decl.t == S.FUNCTION_CALL:
            return self.check_function_call(decl, ctx)
        elif decl.t == S.READ:
            e = decl.expression
            e = self.check_and_mark_expression(e, ctx)
            ctx.variable_initialized(e.name)
            decl.expression = e
            return decl
        elif decl.t == S.WRITE:
            decl.expression = self.check_and_mark_expression(decl.expression, ctx)
            return decl
        elif decl.t == S.RETURN_DECLARATION:
            return self.check_return(decl, ctx)
        elif decl.t == S.FUNCTION_CALL_LAZY:
            decl = self.check_and_mark_expression(decl, ctx)
            return self.dispatch_declaration(decl, ctx)
        else:
            print(decl.__class__.__name__)
            raise Exception("Unimplemented")

    def check_program(self, ast):
        """
        On program, check and collect:
            [X] FUNCTION_DECLARATION (check, collect, programa)
            [X] VARS_DECLARATION (collect)
            [X] ASSIGNMENT (check, collect)
        """
        ctx = self.program_ctx

        # collect all global functions and variables
        for decl in ast.declarations:
            if decl.t == S.FUNCTION_DECLARATION:
                name = decl.name

                if self.function_is_declared(name):
                    # check multiple function declaration
                    self.errors.append(
                        SemanticError(
                            SE.MULTIPLE_FUNCTION_DECLARATION,
                            ctx,
                            {"function": name},
                        )
                    )
                elif self.get_global_variable(name):
                    # function declaration shadow global variable
                    self.errors.append(
                        SemanticError(
                            SE.SYMBOL_ALREADY_EXISTS,
                            ctx,
                            {"function": name},
                        )
                    )

                # collect function declaration
                ctx.declare_function(decl)
            else:  # decl.t == S.VARS_DECLARATION:
                for v in decl.variables:
                    self.check_and_declare_variable(v, ctx)

        # All functions and variables was collected before
        # checking the function declaration
        declarations = [
            self.dispatch_declaration(decl, ctx) for decl in ctx.functions.values()
        ]

        self.check_variable_usage(ctx)
        self.check_function_main_exists()

        self.ast = Program(declarations)

    # checker start
    def check(self, ast):
        if ast and ast.t == S.PROGRAM:
            self.check_program(ast)
        else:
            self.errors.append(SemanticError(SE.AST_MALFORMED, self.program_ctx))
        return self
