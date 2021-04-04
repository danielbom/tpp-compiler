from anytree import Node


def generate_anytree_tree(root):
    def _rec(node, parent):
        anytree_node = Node(node.identifier, parent=parent)
        
        if node.value:
            value = Node(node.value, parent=anytree_node)
        else:
            for c in node.children:
                _rec(c, anytree_node)

        return anytree_node

    return _rec(root, None)


class Tree:
    def __init__(self, identifier, children=[], value=None):
        self.identifier = identifier
        self.value = value
        self.children = children

    def update_identifier(self, identifier):
        return Tree(identifier, self.children, self.value)

    def prepend(self, tree):
        return Tree(self.identifier, [tree] + self.children, self.value)

    def str_tree(self, indentation = 0):
        spaces = "  " * indentation

        if self.value is None:
            s = spaces + f"({indentation}, {self.identifier})"
        else:
            s = spaces + f"({indentation}, {self.identifier}, \"{self.value}\")"

        if self.children:
            s += "\n"
            s += f"\n".join(c.str_tree(indentation + 1) for c in self.children)

        return s
    
    def str_clojure(self, indentation = 0):
        spaces = "  " * indentation
        if self.value: # literal
            return f"\"{self.value}\""
        if self.children: # common
            return f"\n{spaces}({self.identifier} {' '.join(c.str_clojure(indentation + 1) for c in self.children)})"
        return f"{self.identifier}"

    def __str__(self):
        return f"Tree({self.identifier})"

    def __repr__(self):
        return str(self)
