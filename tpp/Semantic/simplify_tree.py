from tpp.Tree import Tree


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
    UNARY_EXPRESSION = ["negacao", "expressao_unaria"]
    BINARY_EXPRESSION = [
        "expressao",
        "expressoes_booleanas",
        "expressoes_booleanas_primario",
        "expressao_de_igualdade_primario",
        "expressoes_de_comparacao",
        "expressao_de_comparacao_primario",
        "expressao_matematica",
        "soma",
        "produto",
    ]
    BINARY_EXPRESSION_2 = [
        "adiciona_ou_subtrai",
        "conjuncao_ou_disjuncao",
        "multiplica_ou_divide",
        "expressoes_de_igualdade",
    ]
    GO_AHEAD = [
        "declaracao",
        "numero",
        "literal",
        "negacao",
        "tipo",
    ] + BINARY_EXPRESSION + BINARY_EXPRESSION_2
    VOID_TYPE = Tree("VAZIO", value="vazio")
    COMPARE_EXPRESSION = ["maior", "menor", "conjuncao", "disjuncao"]

    def rec(node: Tree):
        cs = node.children
        n = len(cs)

        if node.identifier in GO_AHEAD and n == 1:
            return rec(cs[0])

        if node.identifier in UNARY_EXPRESSION and n == 2:
            return Tree("expressao_unaria", [cs[0], rec(cs[1])])

        if node.identifier in BINARY_EXPRESSION_2:
            first, second = cs
            op, second = second.children
            second = rec(second)
            first = rec(first)
            return Tree("expression", [first, op, second])

        if node.identifier in BINARY_EXPRESSION:
            first, second = cs

            first = rec(first)
            second = rec(second)

            if "terminal" in second.identifier or second.identifier in COMPARE_EXPRESSION:
                op, second = second.children
                return Tree("expression", [first, op, second])
            else:
                # Rotate
                first2 = second.children[0]
                second.children[0] = Tree("expression", [first] + first2.children)
                return second

        if node.identifier == "literal" and n == 3:  # ( expression )
            return rec(cs[1])

        cs = [rec(c) for c in cs if c.identifier not in IGNORE_NODES]

        if node.identifier == "funcao_declaracao" and len(cs) == 2:
            cs = [VOID_TYPE] + cs

        return node.update_children(cs)

    return rec(root)
