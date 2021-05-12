from tpp.Semantic import T, S, A, O
from llvmlite import ir
from llvmlite import binding as llvm


class G:
    INT = ir.IntType(32)
    ZERO_INT = ir.Constant(INT, 0)
    FLOAT = ir.FloatType()
    ZERO_FLOAT = ir.Constant(FLOAT, 0.0)
    VOID = ir.VoidType()

    COMPARE_SYMBOLS = {
        O.GRANTER: '>',
        O.GRANTER_EQUAL: '>=',
        O.LESS: '<',
        O.LESS_EQUAL: '<=',
        O.EQUAL: '==',
        O.DIFFERENT: '!='
    }

    @staticmethod
    def const_float(value):
        return ir.Constant(G.FLOAT, value)

    @staticmethod
    def const_int(value):
        return ir.Constant(G.INT, value)

    @staticmethod
    def map_typing(typing):
        if typing == T.INTEGER:
            g = G()
            g.typing = G.INT
            g.initializer = G.ZERO_INT
            g.t = T.INTEGER
            return g
        if typing == T.FLOAT:
            g = G()
            g.typing = G.FLOAT
            g.initializer = G.ZERO_FLOAT
            g.t = T.FLOAT
            return g
        if typing == T.VOID:
            g = G()
            g.typing = G.VOID
            g.t = T.VOID
            return g

        raise Exception("Unimplemented")

    @staticmethod
    def map_typing_with_indexes(typing, indexes):
        g = G.map_typing(typing)
        t = g.typing

        for index in reversed(indexes):
            if index.t == S.POINTER:
                t = ir.PointerType(t)
            elif index.t == S.LITERAL_INTEGER:
                t = ir.VectorType(t, index.value)
            else:
                raise Exception("Unimplemented")

        g.typing = t

        if indexes:
            g.initializer = ir.Constant(t, None)

        return g


class FunctionBuilder:
    def __init__(self, decl, function_name, program):
        self.decl = decl
        self.function_name = function_name
        self.program = program
        self.return_name = "ret_val"

        self.parameters = None
        self.return_g = None
        self.function_typing = None
        self.function = None
        self.entry_block = None
        self.exit_block = None
        self.entry_builder = None
        self.exit_builder = None
        self.variables = {}
        self.early_exit = False

    # Utils
    def consume_early_exit(self):
        if self.early_exit:
            self.early_exit = False
            return True 
        return False 

    def get_variable(self, name):
        return self.variables[name]
    
    def get_binary_operator(self, expr):
        if expr.operation == O.ADD:
            return lambda t1, t2, n: self.entry_builder.add(t1, t2, name=n)
        elif expr.operation == O.SUBTRACT:
            return lambda t1, t2, n: self.entry_builder.sub(t1, t2, name=n)
        elif expr.operation == O.MULTIPLY:
            return lambda t1, t2, n: self.entry_builder.mul(t1, t2, name=n)
        elif expr.operation == O.DIVIDE:
            return lambda t1, t2, n: self.entry_builder.sdiv(t1, t2, name=n)
        elif expr.operation == O.AND:
            return lambda t1, t2, n: self.entry_builder.and_(t1, t2, name=n)
        elif expr.operation == O.OR:
            return lambda t1, t2, n: self.entry_builder.or_(t1, t2, name=n)

        if expr.operation in G.COMPARE_SYMBOLS:
            op = G.COMPARE_SYMBOLS[expr.operation]
            if expr.first.typing == T.INTEGER:
                if expr.second.typing == T.INTEGER:
                    return lambda t1, t2, n: self.entry_builder.icmp_signed(op, t1, t2, name=n)
            return lambda t1, t2, n: self.entry_builder.fcmp_signed(op, t1, t2, name=n)
            
    # Solver
    def solve_expression(self, expr):
        if expr.t == S.LITERAL_INTEGER:
            return G.const_int(expr.value)
        elif expr.t == S.LITERAL_VARIABLE:
            variable = self.get_variable(expr.name)
            return self.entry_builder.load(variable, name=self.program.get_temp_name())
        elif expr.t == S.BINARY_EXPRESSION:
            temp1 = self.solve_expression(expr.first)
            temp2 = self.solve_expression(expr.second)
            operator = self.get_binary_operator(expr)

            if operator is None:
                print("solve_expression:", expr.operation)
                print()
                raise Exception("Unimplemented")

            return operator(temp1, temp2, self.program.get_temp_name())
            
        print("solve_expression:", expr.__class__.__name__)
        print()
        raise Exception("Unimplemented")
    
    def solve_var_declaration(self, decl):
        for v in decl.variables:
            g = G.map_typing_with_indexes(v.typing, v.indexes)
            variable = self.entry_builder.alloca(g.typing, name=v.name)
            self.entry_builder.store(g.initializer, variable)
            self.variables[v.name] = variable

    def solve_assignment(self, decl):
        variable = self.get_variable(decl.variable.name)
        expression = self.solve_expression(decl.expression)

        if decl.assignment == A.INITIALIZE:
            self.entry_builder.store(expression, variable)
        else:
            print(decl.__class__.__name__, ':', decl.t)
            print(decl.assignment)
            print()
            raise Exception("Unimplemented")

    def solve_body(self, body):
        for decl in body:
            self.dispatch_declaration(decl)

    def solve_return(self, decl):
        g = self.return_g
        if g.t != T.VOID:
            expression = self.solve_expression(decl.expression)
            self.entry_builder.store(expression, self.return_value)
        self.early_exit = True

    def solve_if_else(self, decl):
        if_names = self.program.get_if_names()
            
        if_block = self.entry_builder.append_basic_block(if_names["if"])
        else_block = self.entry_builder.append_basic_block(if_names["else"])
        early_block = self.entry_builder.append_basic_block(if_names["early"])
        end_block = self.entry_builder.append_basic_block(if_names["end"])

        # Expression
        expression = self.solve_expression(decl.if_expression)
        self.entry_builder.cbranch(expression, if_block, else_block)

        # If
        self.entry_builder.position_at_end(if_block)
        self.solve_body(decl.if_body)
        if self.consume_early_exit():
            self.entry_builder.branch(early_block)
        else:
            self.entry_builder.branch(end_block)

        # Else
        self.entry_builder.position_at_end(else_block)
        self.solve_body(decl.else_body)
        if self.consume_early_exit():
            self.entry_builder.branch(early_block)
        else:
            self.entry_builder.branch(end_block)

        # Early
        self.entry_builder.position_at_end(early_block)
        self.entry_builder.branch(self.exit_block)

        # Finish declaration
        self.entry_builder.position_at_end(end_block)

    def solve_repeat(self, decl):
        repeat_names = self.program.get_repeat_names()

        repeat_block = self.entry_builder.append_basic_block(repeat_names["repeat"])
        cond_block = self.entry_builder.append_basic_block(repeat_names["cond"])
        early_block = self.entry_builder.append_basic_block(repeat_names["early"])
        end_block = self.entry_builder.append_basic_block(repeat_names["end"])

        # Repeat
        self.entry_builder.branch(repeat_block)
        self.entry_builder.position_at_end(repeat_block)
        self.solve_body(decl.body)
        if self.consume_early_exit():
            self.entry_builder.branch(early_block)
        else:
            self.entry_builder.branch(cond_block)

        # Expression
        self.entry_builder.position_at_end(cond_block)
        expression = self.solve_expression(decl.expression)
        self.entry_builder.cbranch(expression, end_block, repeat_block)

        # Early
        self.entry_builder.position_at_end(early_block)
        self.entry_builder.branch(self.exit_block)

        # Finish declaration
        self.entry_builder.position_at_end(end_block)

    # Dispatch
    def dispatch_declaration(self, decl):
        if decl.t == S.EMPTY:
            return
        elif decl.t == S.RETURN_DECLARATION:
            self.solve_return(decl)
        elif decl.t == S.VARS_DECLARATION:
            self.solve_var_declaration(decl)
        elif decl.t == S.REPEAT_DECLARATION:
            self.solve_repeat(decl)
        elif decl.t == S.IF_ELSE_DECLARATION:
            self.solve_if_else(decl)
        elif decl.t == S.ASSIGNMENT:
            self.solve_assignment(decl)
        # elif decl.t == S.FUNCTION_CALL:
        # elif decl.t == S.READ:
        # elif decl.t == S.WRITE:
        else:
            print(decl.__class__.__name__, ':', decl.t)
            print()
            raise Exception("Unimplemented")

    # Process
    def _build_parameters(self):
        parameters = self.decl.parameters
        parameters = (G.map_typing_with_indexes(p.typing, p.indexes) for p in parameters)
        self.parameters = [p.typing for p in parameters]

    def _build_function_type(self):
        self.return_g = G.map_typing(self.decl.return_type)
        self.function_typing = ir.FunctionType(self.return_g.typing, self.parameters)

    def _declare_function(self):
        module = self.program.module
        self.function = ir.Function(module, self.function_typing, self.function_name)

    def _name_parameters(self):
        for arg, param in zip(self.function.args, self.decl.parameters):
            arg.name = param.name

    def _declare_entry_and_exit_blocks_and_builders(self):
        self.entry_block = self.function.append_basic_block(self.function_name + ".entry")
        self.exit_block = self.function.append_basic_block(self.function_name + ".exit")
        self.entry_builder = ir.IRBuilder(self.entry_block)
        self.exit_builder = ir.IRBuilder(self.exit_block)

    def _declare_return_value(self):
        g = self.return_g
        if g.t != T.VOID:
            self.return_value = self.entry_builder.alloca(g.typing, name=self.return_name)
            self.entry_builder.store(g.initializer, self.return_value)

    def _build_body(self):
        for decl in self.decl.body:
            self.dispatch_declaration(decl)
    
    def _build_exit_of_function(self):
        self.entry_builder.branch(self.exit_block)
        if self.return_g.t == T.VOID:
            self.exit_builder.ret_void()
        else:
            # Add return declaration
            return_loaded = self.exit_builder.load(self.return_value, self.return_name)
            self.exit_builder.ret(return_loaded)

    # Start
    def build(self):
        # Methods calls are dependents and must executed in this order
        self._build_parameters()
        self._build_function_type()
        self._declare_function()
        self._name_parameters()
        self._declare_entry_and_exit_blocks_and_builders()
        self._declare_return_value()
        self._build_body()
        self._build_exit_of_function()


class ProgramBuilder:
    def __init__(self, filename, ast, program_ctx):
        self.ast = ast
        self.program_ctx = program_ctx
        self.filename = filename

        self.module = None  # Create on call build()

        self.temp_counter = 1
        self.if_counter = 1
        self.repeat_counter = 1
        self.function_counter = 1
    
    # Utils
    def get_temp_name(self):
        counter = self.temp_counter
        self.temp_counter += 1
        return f"t.{counter}"
    
    def get_if_names(self):
        counter = self.if_counter
        self.if_counter += 1
        return {
            "if": f"if.{counter}",
            "else": f"else.{counter}",
            "end": f"end.{counter}",
            "early": f"early.{counter}"
        }

    def get_repeat_names(self):
        counter = self.repeat_counter
        self.repeat_counter += 1
        return {
            "repeat": f"repeat.{counter}",
            "cond": f"cond.{counter}",
            "end": f"end.{counter}",
            "early": f"early.{counter}"
        }
    
    # Outer resolution
    def _build_function(self, function_name: str, decl):
        build_function = FunctionBuilder(decl, function_name, self)
        build_function.build()
    
    # Process
    def _startup_llvm(self):
        llvm.initialize()
        llvm.initialize_all_targets()
        llvm.initialize_all_asmprinters()
        # llvm.initialize_native_target()
        # llvm.initialize_native_asmprinter()

    def _create_module(self):
        self.module = ir.Module(self.filename)
        self.module.triple = llvm.get_process_triple()

        target = llvm.Target.from_triple(self.module.triple)
        target_machine = target.create_target_machine()
        self.module.data_layout = target_machine.target_data

    def _declare_global_variables(self):
        for decl in self.program_ctx.variables.values():
            g = G.map_typing(decl.typing)
            v = ir.GlobalVariable(self.module, g.typing, decl.name)
            v.linkage = "common"
            v.align = 4
            v.initializer = g.initializer
    
    def _declare_functions(self):
        MAIN_NAME = "principal"

        for name, decl in self.program_ctx.functions.items():
            if name == MAIN_NAME:
                name = "main"
            self._build_function(name, decl)

    def _finish_llvm_process(self):
        llvm.shutdown()
    
    # Start
    def build(self):
        # Methods calls are dependents and must executed in this order
        self._startup_llvm()
        self._create_module()
        self._declare_global_variables()
        self._declare_functions()
        self._finish_llvm_process()
        return self.module


def build_intermediate_code(filename, ast, program_ctx):
    g = ProgramBuilder(filename, ast, program_ctx)
    return g.build()
