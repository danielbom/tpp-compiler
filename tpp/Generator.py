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
                t = ir.ArrayType(t, index.value)
            else:
                raise Exception("Unimplemented")

        g.typing = t

        if indexes:
            g.initializer = ir.Constant(t, None)

        return g


class GeneratorContext:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

        self.variables = {}

    def get_variable(self, name):
        var = self.variables.get(name)
        return self.parent.get_variable(name) if var is None else var


class FunctionBuilder:
    def __init__(self, decl, function_name, function, program):
        self.decl = decl
        self.function_name = function_name
        self.function = function
        self.program = program

        self.return_g = G.map_typing(decl.return_type)
        self.return_name = function_name + ".return"

        self.entry_block = None
        self.exit_block = None
        self.entry_builder = None
        self.exit_builder = None
        self.early_exit = False

    # Utils
    def consume_early_exit(self):
        if self.early_exit:
            self.early_exit = False
            return True 
        return False 

    def get_binary_operator(self, expr):
        if expr.operation == O.AND:
            return lambda t1, t2, n: self.entry_builder.and_(t1, t2, name=n)
        if expr.operation == O.OR:
            return lambda t1, t2, n: self.entry_builder.or_(t1, t2, name=n)

        if expr.operation == O.ADD:
            if expr.first.typing == T.INTEGER and expr.second.typing == T.INTEGER:
                return lambda t1, t2, n: self.entry_builder.add(t1, t2, name=n)
            elif expr.first.typing == T.FLOAT and expr.second.typing == T.FLOAT:
                return lambda t1, t2, n: self.entry_builder.fadd(t1, t2, name=n)
        if expr.operation == O.SUBTRACT:
            if expr.first.typing == T.INTEGER and expr.second.typing == T.INTEGER:
                return lambda t1, t2, n: self.entry_builder.sub(t1, t2, name=n)
            elif expr.first.typing == T.FLOAT and expr.second.typing == T.FLOAT:
                return lambda t1, t2, n: self.entry_builder.fsub(t1, t2, name=n)
        if expr.operation == O.MULTIPLY:
            if expr.first.typing == T.INTEGER and expr.second.typing == T.INTEGER:
                return lambda t1, t2, n: self.entry_builder.mul(t1, t2, name=n)
            elif expr.first.typing == T.FLOAT and expr.second.typing == T.FLOAT:
                return lambda t1, t2, n: self.entry_builder.fmul(t1, t2, name=n)
        if expr.operation == O.DIVIDE:
            if expr.first.typing == T.INTEGER and expr.second.typing == T.INTEGER:
                return lambda t1, t2, n: self.entry_builder.sdiv(t1, t2, name=n)
            elif expr.first.typing == T.FLOAT and expr.second.typing == T.FLOAT:
                return lambda t1, t2, n: self.entry_builder.fdiv(t1, t2, name=n)

        if expr.operation in G.COMPARE_SYMBOLS:
            op = G.COMPARE_SYMBOLS[expr.operation]
            if expr.first.typing == T.INTEGER and expr.second.typing == T.INTEGER:
                return lambda t1, t2, n: self.entry_builder.icmp_signed(op, t1, t2, name=n)
            return lambda t1, t2, n: self.entry_builder.fcmp_ordered(op, t1, t2, name=n)
          
    def declare_variables(self, decl, ctx):
        for v in decl.variables:
            g = G.map_typing_with_indexes(v.typing, v.indexes)
            variable = self.entry_builder.alloca(g.typing, name=v.name)
            self.entry_builder.store(g.initializer, variable)
            ctx.variables[v.name] = variable
  
    # Solver
    def solve_function_call(self, decl, ctx):
        # parameters: Gen<(Variable, LLVM)> -> [LLVM]
        parameters = ((p, self.solve_expression(p, ctx)) for p in decl.parameters)
        parameters = [expr for p, expr in parameters]
        function = self.program.get_function(decl.name)
        result = self.entry_builder.call(function, parameters, name=self.program.get_temp_name())
        return result

    def get_variable(self, decl, ctx):
        variable = ctx.get_variable(decl.name)

        ptr = variable
        for i in decl.indexes:
            if i.t == S.LITERAL_INTEGER:
                index = G.INT(i.value)
            else:
                index = self.solve_expression(i, ctx)
                index = self.entry_builder.sext(index, G.INT, name=self.program.get_temp_name())
            ptr = self.entry_builder.gep(ptr, [G.INT(0), index], name=self.program.get_temp_name())
        return ptr

    def solve_expression(self, expr, ctx):
        if expr.t == S.LITERAL_INTEGER:
            return G.const_int(expr.value)
        elif expr.t == S.LITERAL_FLOAT:
            return G.const_float(expr.value)
        elif expr.t == S.LITERAL_VARIABLE:
            ptr = self.get_variable(expr, ctx)
            return self.entry_builder.load(ptr, name=self.program.get_temp_name())
        elif expr.t == S.BINARY_EXPRESSION:
            temp1 = self.solve_expression(expr.first, ctx)
            cast = self.implicit_cast(expr.typing, expr.first.typing)
            temp1 = cast(temp1)

            temp2 = self.solve_expression(expr.second, ctx)
            cast = self.implicit_cast(expr.typing, expr.second.typing)
            temp2 = cast(temp2)

            operator = self.get_binary_operator(expr)

            if operator is None:
                print("solve_expression:", expr.operation)
                print()
                raise Exception("Unimplemented")

            return operator(temp1, temp2, self.program.get_temp_name())
        elif expr.t == S.UNARY_EXPRESSION:
            if expr.operation == O.NEGATE:
                temp = self.solve_expression(expr.variable, ctx)
                return self.entry_builder.not_(temp, name=self.program.get_temp_name())
            else:
                print(expr.operation)
                raise Exception("Unimplemented")
        elif expr.t == S.FUNCTION_CALL:
            return self.solve_function_call(expr, ctx)

        print("solve_expression:", expr.__class__.__name__)
        print()
        raise Exception("Unimplemented")
    
    def implicit_cast(self, typing1, typing2):
        if typing1 != typing2:
            if typing1 == T.INTEGER:
                if typing2 == T.FLOAT:
                    return lambda x: self.entry_builder.fptosi(x, G.INT, name=self.program.get_temp_name())
                else:
                    raise Exception("Unimplemented")
            elif typing1 == T.FLOAT:
                if typing2 == T.INTEGER:
                    return lambda x: self.entry_builder.sitofp(x, G.FLOAT, name=self.program.get_temp_name())
                else:
                    raise Exception("Unimplemented")
            else:
                raise Exception("Unimplemented")
        return lambda x: x
    
    def solve_assignment(self, decl, ctx):
        variable = self.get_variable(decl.variable, ctx)
        expression = self.solve_expression(decl.expression, ctx)

        if decl.assignment == A.INITIALIZE:
            cast = self.implicit_cast(decl.variable.typing, decl.expression.typing)
            expression = cast(expression)
            self.entry_builder.store(expression, variable)
        else:
            if decl.assignment == A.ADD:
                operator = self.entry_builder.add
            elif decl.assignment == A.SUBTRACT:
                operator = self.entry_builder.sub
            elif decl.assignment == A.MULTIPLY:
                operator = self.entry_builder.mul
            elif decl.assignment == A.DIVIDE:
                operator = self.entry_builder.sdiv
            else:
                print(decl.__class__.__name__, ':', decl.t)
                print(decl.assignment)
                print()
                raise Exception("Unimplemented")

            temp1 = self.entry_builder.load(variable, name=self.program.get_temp_name())
            temp2 = operator(temp1, expression, name=self.program.get_temp_name())
            self.entry_builder.store(temp2, variable)

    def solve_body(self, body, ctx):
        for decl in body:
            self.dispatch_declaration(decl, ctx)

    def solve_return(self, decl, ctx):
        g = self.return_g
        if g.t != T.VOID:
            expression = self.solve_expression(decl.expression, ctx)
            self.entry_builder.store(expression, self.return_value)
        self.early_exit = True

    def solve_if_else(self, decl, ctx):
        if_names = self.program.get_if_names()
            
        if_block = self.entry_builder.append_basic_block(if_names["if"])
        else_block = self.entry_builder.append_basic_block(if_names["else"])
        early_block = self.entry_builder.append_basic_block(if_names["early"])
        end_block = self.entry_builder.append_basic_block(if_names["end"])

        # Expression
        expression = self.solve_expression(decl.if_expression, ctx)
        self.entry_builder.cbranch(expression, if_block, else_block)

        # If
        self.entry_builder.position_at_end(if_block)
        self.solve_body(decl.if_body, GeneratorContext(if_names["if"], ctx))
        if self.consume_early_exit():
            self.entry_builder.branch(early_block)
        else:
            self.entry_builder.branch(end_block)

        # Else
        self.entry_builder.position_at_end(else_block)
        self.solve_body(decl.else_body, GeneratorContext(if_names["else"], ctx))
        if self.consume_early_exit():
            self.entry_builder.branch(early_block)
        else:
            self.entry_builder.branch(end_block)

        # Early
        self.entry_builder.position_at_end(early_block)
        self.entry_builder.branch(self.exit_block)

        # Finish declaration
        self.entry_builder.position_at_end(end_block)

    def solve_repeat(self, decl, ctx):
        repeat_names = self.program.get_repeat_names()

        repeat_block = self.entry_builder.append_basic_block(repeat_names["repeat"])
        cond_block = self.entry_builder.append_basic_block(repeat_names["cond"])
        early_block = self.entry_builder.append_basic_block(repeat_names["early"])
        end_block = self.entry_builder.append_basic_block(repeat_names["end"])

        # Start
        self.entry_builder.branch(repeat_block)

        # Body
        self.entry_builder.position_at_end(repeat_block)
        self.solve_body(decl.body, GeneratorContext(repeat_names["repeat"], ctx))
        if self.consume_early_exit():
            self.entry_builder.branch(early_block)
        else:
            self.entry_builder.branch(cond_block)

        # Expression
        self.entry_builder.position_at_end(cond_block)
        expression = self.solve_expression(decl.expression, ctx)
        self.entry_builder.cbranch(expression, end_block, repeat_block)

        # Early
        self.entry_builder.position_at_end(early_block)
        self.entry_builder.branch(self.exit_block)

        # Finish declaration
        self.entry_builder.position_at_end(end_block)

    # Dispatch
    def dispatch_declaration(self, decl, ctx):
        if decl.t == S.EMPTY:
            return
        elif decl.t == S.RETURN_DECLARATION:
            self.solve_return(decl, ctx)
        elif decl.t == S.VARS_DECLARATION:
            self.declare_variables(decl, ctx)
        elif decl.t == S.REPEAT_DECLARATION:
            self.solve_repeat(decl, ctx)
        elif decl.t == S.IF_ELSE_DECLARATION:
            self.solve_if_else(decl, ctx)
        elif decl.t == S.ASSIGNMENT:
            self.solve_assignment(decl, ctx)
        elif decl.t == S.FUNCTION_CALL:
            return self.solve_function_call(decl, ctx)
        elif decl.t == S.READ:
            variable = ctx.get_variable(decl.variable.name)
            if decl.variable.typing == T.INTEGER:
                result = self.entry_builder.call(self.program.read_int, [])
            elif decl.variable.typing == T.FLOAT:
                result = self.entry_builder.call(self.program.read_float, [])
            else:
                raise Exception("Unimplemented")
            self.entry_builder.store(result, variable)
        elif decl.t == S.WRITE:
            temp = self.solve_expression(decl.expression, ctx)

            if decl.expression.typing == T.INTEGER:
                self.entry_builder.call(self.program.write_int, [temp])
            elif decl.expression.typing == T.FLOAT:
                self.entry_builder.call(self.program.write_float, [temp])
            else:
                raise Exception("Unimplemented")
        else:
            print(decl.__class__.__name__, ':', decl.t)
            print()
            raise Exception("Unimplemented")

    # Process
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

    def _declare_parameters_as_variables(self, ctx):
        for p, a in zip(self.decl.parameters, self.function.args):
            g = G.map_typing_with_indexes(p.typing, p.indexes)
            variable = self.entry_builder.alloca(g.typing, name=p.name)
            self.entry_builder.store(a, variable)
            ctx.variables[p.name] = variable

    def _build_body(self, ctx):
        for decl in self.decl.body:
            self.dispatch_declaration(decl, ctx)
    
    def _build_exit_of_function(self):
        self.entry_builder.branch(self.exit_block)
        if self.return_g.t == T.VOID:
            self.exit_builder.ret_void()
        else:
            # Add return declaration
            temp = self.exit_builder.load(self.return_value, name=self.program.get_temp_name())
            self.exit_builder.ret(temp)

    # Start
    def build(self):
        # Methods calls are dependents and must executed in this order
        self._declare_entry_and_exit_blocks_and_builders()
        self._declare_return_value()

        ctx = GeneratorContext(self.function_name, self.program.global_ctx)
        self._declare_parameters_as_variables(ctx)
        self._build_body(ctx)
        
        self._build_exit_of_function()


class ProgramBuilder:
    def __init__(self, filename, ast, program_ctx):
        self.ast = ast
        self.program_ctx = program_ctx
        self.filename = filename

        self.functions = {}
        self.module = None  # Create on call build()

        self.temp_counter = 1
        self.if_counter = 1
        self.repeat_counter = 1
        self.function_counter = 1
        self.global_ctx = GeneratorContext("__global")
    
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

    def get_function(self, name):
        return self.functions[name]

    def declare_function(self, name, decl):
        # Parameters typing
        parameters = decl.parameters
        parameters = (G.map_typing_with_indexes(p.typing, p.indexes) for p in parameters)
        parameters = [p.typing for p in parameters]

        # Function typing
        return_g = G.map_typing(decl.return_type)
        function_typing = ir.FunctionType(return_g.typing, parameters)

        # Function declaration
        function = ir.Function(self.module, function_typing, name)

        # Name parameters
        for arg, param in zip(function.args, decl.parameters):
            arg.name = param.name

        # Store function declaration
        self.functions[name] = function

        return function

    # Read and Write
    def declare_write_functions(self):
        function_typing_int = ir.FunctionType(G.VOID, [G.INT])
        self.write_int = ir.Function(self.module, function_typing_int, "__write_int")

        function_typing_float = ir.FunctionType(G.VOID, [G.FLOAT])
        self.write_float = ir.Function(self.module, function_typing_float, "__write_float")

    def declare_read_functions(self):
        function_typing_int = ir.FunctionType(G.INT, [])
        self.read_int = ir.Function(self.module, function_typing_int, "__read_int")

        function_typing_float = ir.FunctionType(G.FLOAT, [])
        self.read_float = ir.Function(self.module, function_typing_float, "__read_float")

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

        self.declare_write_functions()
        self.declare_read_functions()

    def _declare_global_variables(self):
        for decl in self.program_ctx.variables.values():
            g = G.map_typing_with_indexes(decl.typing, decl.indexes)
            v = ir.GlobalVariable(self.module, g.typing, decl.name)
            v.linkage = "common"
            v.align = 4
            v.initializer = g.initializer
            self.global_ctx.variables[decl.name] = v
    
    def _declare_functions(self):
        MAIN_NAME = "principal"

        for name, decl in self.program_ctx.functions.items():
            if name == MAIN_NAME:
                name = "main"
            self.declare_function(name, decl)

    def _build_functions(self):
        MAIN_NAME = "principal"

        for name, decl in self.program_ctx.functions.items():
            if name == MAIN_NAME:
                name = "main"
            function = self.functions[name]
            build_function = FunctionBuilder(decl, name, function, self)
            build_function.build()

    def _finish_llvm_process(self):
        llvm.shutdown()
    
    # Start
    def build(self):
        # Methods calls are dependents and must executed in this order
        self._startup_llvm()
        self._create_module()
        self._declare_global_variables()
        self._declare_functions()
        self._build_functions()
        self._finish_llvm_process()
        return self.module


def build_intermediate_code(filename, ast, program_ctx):
    g = ProgramBuilder(filename, ast, program_ctx)
    return g.build()
