class Tree:
    def __init__(self, identifier, children=[], value=None):
        self.identifier = identifier
        self.value = value
        self.children = children

    def update_identifier(self, identifier):
        return Tree(identifier, self.children, self.value)

    def str_rec(self, indentation: int):
        spaces = "  " * indentation

        if self.value is None:
            s = spaces + f"({self.identifier})"
        else:
            s = spaces + f"({self.identifier}, {self.value})"

        if self.children:
            s += " [\n"
            s += f",\n".join(c.str_rec(indentation + 1) for c in self.children)
            s += "\n" + spaces + "]"

        return s

    def __str__(self):
        return self.str_rec(0)

    def __repr__(self):
        return str(self)
