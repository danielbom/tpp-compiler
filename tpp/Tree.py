from anytree import Node


def generate_anytree_tree(root):
    def _rec(node, parent):
        anytree_node = Node(node.identifier, parent=parent)
        
        if node._value is not None:
            Node(node._value, parent=anytree_node)
        else:
            for c in node.children:
                _rec(c, anytree_node)

        return anytree_node

    return _rec(root, None)


class Tree:
    def __init__(self, identifier, children=[], value=None):
        self.identifier = identifier
        self._value = value
        self.children = children
    
    @property
    def value(self):
        if self.is_leaf():
            return self._value
        raise TypeError(f"Can't access value for this node Tree! {self}")

    def is_leaf(self):
        return not self.children

    def update_identifier(self, identifier):
        return Tree(identifier, self.children, self._value)
    
    def update_children(self, children):
        return Tree(self.identifier, children, self._value)

    def str_tree(self, indentation = 0):
        spaces = "  " * indentation

        if self._value is None:
            s = spaces + f"({indentation}, {self.identifier})"
        else:
            s = spaces + f"({indentation}, {self.identifier}, \"{self.value}\")"

        if self.children:
            s += "\n"
            s += f"\n".join(c.str_tree(indentation + 1) for c in self.children)

        return s
    
    def str_clojure(self, indentation = 0):
        spaces = "  " * indentation
        if self._value: # literal
            return f"\"{self.value}\""
        if self.children: # common
            return f"\n{spaces}({self.identifier} {' '.join(c.str_clojure(indentation + 1) for c in self.children)})"
        return f"{self.identifier}"

    def __str__(self):
        return f"Tree({self.identifier})"

    def __repr__(self):
        return str(self)
