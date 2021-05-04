class SemanticContext:
    def __init__(self, scope, parent=None):
        self.scope = scope

        self.functions = {}
        self.variables = {}

        self.children = []
        self.parent = parent

        if parent:
            self.parent.children.append(self)

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
        if self.is_global():
            return None
        if self.parent.is_global():
            return self.scope
        return self.parent.get_function_name()

    def get_variable(self, name):
        if self.variable_is_declared_local(name):
            return self.variables[name]
        elif not self.is_global():
            return self.parent.get_variable(name)
        else:
            return None
