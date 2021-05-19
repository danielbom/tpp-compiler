from tpp.Tree import Tree


def simplify_tree(root):
    def rotate_expression(first, second):
        if second.identifier == "expression":
            first2, op, second = second.children
            first = Tree("expression", [first] + first2.children)
            return Tree("expression", [first, op, second])
        else:
            op, second = second.children
            return Tree("expression", [first, op, second])

    def simplify_body(body):
        declarations = body.children
        declarations = [simplify_tree(d) for d in declarations]
        return body.update_children(declarations)

    VOID_TYPE = Tree("VAZIO", value="vazio")
    ANY_BINARY_FUNCTION = [
        "maior",
        "menor",
        "menor_igual",
        "maior_igual",
        "igual",
        "diferente",
        "conjuncao",
        "disjuncao",
    ]

    def rec(node):
        n = len(node.children)
        if node.identifier == "programa":
            declaration_list = simplify_body(node.children[0])
            return node.update_children([declaration_list])
        if node.identifier == "declaracao":
            return simplify_tree(node.children[0])

        # Vars Declaration
        if node.identifier == "criacao_de_variaveis_declaracao":
            typing, _, list_vars = node.children
            typing = simplify_tree(typing)
            list_vars = simplify_tree(list_vars)
            return node.update_children([typing, list_vars])
        if node.identifier == "criacao_de_variaveis_lista":
            variables = node.children[::2]
            variables = [simplify_tree(v) for v in variables]
            return node.update_children(variables)

        # Function Declaration
        if node.identifier == "funcao_declaracao":
            if n == 4:
                typing, head, body, _ = node.children
                typing = simplify_tree(typing)
                head = simplify_tree(head)
                declarations = simplify_body(body)
            else:  # if n == 3:
                typing = VOID_TYPE
                head, body, _ = node.children
                head = simplify_tree(head)
                declarations = simplify_body(body)
            return node.update_children([typing, head, declarations])
        if node.identifier == "cabecalho":
            id_, _, params, _ = node.children
            params = simplify_tree(params)
            return node.update_children([id_, params])
        if node.identifier == "lista_parametros":
            params = node.children[::2]
            params = [simplify_tree(p) for p in params]
            return node.update_children(params)
        if node.identifier == "parametro":
            typing, _, variable = node.children
            typing = simplify_tree(typing)
            variable = simplify_tree(variable)
            return node.update_children([typing, variable])

        # Return Declaration
        if node.identifier == "retorna_declaracao":
            _, expression = node.children
            expression = simplify_tree(expression)
            return node.update_children([expression])

        # Assignment Declaration
        if node.identifier == "atribuicao_declaracao":
            variable, assignment, expression = node.children
            variable = simplify_tree(variable)
            expression = simplify_tree(expression)
            return node.update_children([variable, assignment, expression])

        # Write Declaration
        if node.identifier == "escreva":
            variable = node.children[2]
            variable = simplify_tree(variable)
            return node.update_children([variable])

        # Write Declaration
        if node.identifier == "leia":
            variable = node.children[2]
            variable = simplify_tree(variable)
            return node.update_children([variable])

        # If Else Declaration
        if node.identifier == "se_declaracao":
            if n == 7:
                _, expression, _, if_body, _, else_body, _ = node.children
                expression = simplify_tree(expression)
                if_body = simplify_body(if_body)
                else_body = simplify_body(else_body)
                return node.update_children([expression, if_body, else_body])
            else:  # if n == 5
                _, expression, _, if_body, _ = node.children
                expression = simplify_tree(expression)
                if_body = simplify_body(if_body)
                return node.update_children([expression, if_body])

        # Repeat Declaration
        if node.identifier == "repita_declaracao":
            _, body, _, expression = node.children
            body = simplify_body(body)
            expression = simplify_tree(expression)
            return node.update_children([body, expression])

        # Call Function Declaration
        if node.identifier == "chamada_de_funcao_declaracao":
            id_, _, params, _ = node.children
            params = simplify_tree(params)
            return node.update_children([id_, params])
        if node.identifier == "chamada_de_funcao_parametros":
            params = node.children[::2]
            params = [simplify_tree(p) for p in params]
            return node.update_children(params)
        if node.identifier == "chamada_de_funcao_parametro":
            return simplify_tree(node.children[0])

        # Variables
        if node.identifier == "var":
            id_, *vector = node.children
            vector = [simplify_tree(d) for d in vector]
            return node.update_children([id_] + vector)
        if node.identifier == "vetor":
            expression = simplify_tree(node.children[1])
            return node.update_children([expression])

        # Expressions
        if node.identifier == "expressao":
            return simplify_tree(node.children[0])
        if node.identifier == "expressoes_booleanas":
            if n == 1:
                return simplify_tree(node.children[0])
            else:  # if n == 2
                first, second = node.children
                second = simplify_tree(second)
                first = simplify_tree(first)

                if second.identifier == "conjuncao_ou_disjuncao":
                    stack = []
                    it = second
                    while it.identifier == "conjuncao_ou_disjuncao":
                        stack.append((it.children[0], it.children[1]))
                        it = it.children[0]

                    first2, second2 = stack.pop()
                    first = Tree("expression", [first] + first2.children)
                    first = Tree("expression", [first] + second2.children)

                    while stack:
                        _, second2 = stack.pop()
                        first = Tree("expression", [first] + second2.children)

                    return first

                op, second = second.children
                return Tree("expression", [first, op, second])

        if node.identifier == "conjuncao_ou_disjuncao":
            if n == 1:
                return simplify_tree(node.children[0])
            else:  # if n == 2
                first, second = node.children
                first = simplify_tree(first)
                second = simplify_tree(second)
                return node.update_children([first, second])
        if node.identifier == "negacao":
            if n == 1:
                return simplify_tree(node.children[0])
            else:  # if n == 2
                first, second = node.children
                second = simplify_tree(second)
                return Tree("expressao_unaria", [first, second])
        if node.identifier == "expressoes_booleanas_primario":
            return simplify_tree(node.children[0])

        # Equality
        if node.identifier == "expressoes_de_igualdade":
            if n == 1:
                return simplify_tree(node.children[0])
            else:  # if n == 2
                first, second = node.children
                first = simplify_tree(first)
                second = simplify_tree(second)
                op, second = second.children
                return Tree("expression", [first, op, second])
        if node.identifier == "expressao_de_igualdade_primario":
            return simplify_tree(node.children[0])
        if node.identifier == "expressoes_de_comparacao":
            if n == 1:
                return simplify_tree(node.children[0])
            else:  # if n == 2:
                first, second = node.children
                first = simplify_tree(first)
                second = simplify_tree(second)
                op, second = second.children
                return Tree("expression", [first, op, second])
        if node.identifier in ANY_BINARY_FUNCTION:
            first, second = node.children
            second = simplify_tree(second)
            return node.update_children([first, second])
        if node.identifier == "expressao_de_comparacao_primario":
            return simplify_tree(node.children[0])

        if node.identifier == "expressao_matematica":
            return simplify_tree(node.children[0])

        # Sum
        if node.identifier == "soma":
            if n == 1:
                return simplify_tree(node.children[0])
            else:  # if n == 2:
                first, second = node.children
                first = simplify_tree(first)
                second = simplify_tree(second)
                return rotate_expression(first, second)
        if node.identifier == "adiciona_ou_subtrai":
            if n == 1:
                return simplify_tree(node.children[0])
            else:  # if n == 2:
                first, second = node.children
                first = simplify_tree(first)
                second = simplify_tree(second)
                op, second = second.children
                return Tree("expression", [first, op, second])
        if node.identifier == "adiciona_ou_subtrai_terminal":
            first, second = node.children
            second = simplify_tree(second)
            return node.update_children([first, second])

        # Product
        if node.identifier == "produto":
            if n == 1:
                return simplify_tree(node.children[0])
            else:  # if n == 2
                first, second = node.children
                first = simplify_tree(first)
                second = simplify_tree(second)
                return rotate_expression(first, second)
        if node.identifier == "multiplica_ou_divide":
            if n == 1:
                return simplify_tree(node.children[0])
            else:  # if n == 2:
                first, second = node.children
                first = simplify_tree(first)
                second = simplify_tree(second)
                op, second = second.children
                return Tree("expression", [first, op, second])
        if node.identifier == "multiplica_ou_divide_terminal":
            first, second = node.children
            second = simplify_tree(second)
            return node.update_children([first, second])

        # Literal
        if node.identifier == "literal":
            if n == 1:
                return simplify_tree(node.children[0])
            else:  # if n == 3: # ( expression )
                return simplify_tree(node.children[1])
        if node.identifier == "numero":
            return node.children[0]
        if node.identifier == "tipo":
            return node.children[0]
        if node.identifier == "vazio":
            return node

        print(node)
        print(node.children)
        print()
        raise Exception("Unimplemented")

    return rec(root)
