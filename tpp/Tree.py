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

    def str_tree(self):
        def str_rec(node, indentation: int):
            spaces = "  " * indentation

            if node.value is None:
                s = spaces + f"({node.identifier})"
            else:
                s = spaces + f"({node.identifier}, {node.value})"

            if node.children:
                s += " [\n"
                s += f",\n".join(str_rec(c, indentation + 1) for c in node.children)
                s += "\n" + spaces + "]"

            return s
        return str_rec(self, 0)

    def __str__(self):
        return f"Tree({self.identifier})"

    def __repr__(self):
        return str(self)
