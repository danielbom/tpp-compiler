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
    GO_AHEAD = ["declaracao", "numero", "literal"]
    BINARY_EXPRESSION = [
        "expressao",
        "expressoes_booleanas",
        "negacao",
        "expressoes_booleanas_primario",
        "expressoes_de_igualdade",
        "expressao_de_igualdade_primario",
        "expressoes_de_comparacao",
        "expressao_de_comparacao_primario",
        "expressao_matematica",
        "soma",
        "produto",
    ]
    EXTRACT_FIRST_CHILDREN = ["conjuncao_ou_disjuncao", "adiciona_ou_subtrai", "tipo"]
    VOID_TYPE = Tree("VAZIO", value="vazio")

    def rec(node: Tree):
        cs = node.children
        n = len(cs)

        if node.identifier in BINARY_EXPRESSION:
            if n == 1:
                return rec(cs[0])

            if n == 2:
                first, second = cs

                second = rec(second)
                op, second = second.children
                first = rec(first)
                second = rec(second)

                return Tree("expression", [first, op, second])

        if node.identifier == "literal" and n == 3:  # ( expression )
            return rec(cs[1])

        if node.identifier in GO_AHEAD:
            return rec(cs[0])

        if node.identifier in EXTRACT_FIRST_CHILDREN:
            return rec(node.children[0])

        cs = (c for c in cs if c.identifier not in IGNORE_NODES)
        cs = list(map(rec, cs))

        if node.identifier == "funcao_declaracao" and len(cs) == 2:
            cs = [VOID_TYPE] + cs

        return node.update_children(cs)

    return rec(root)
