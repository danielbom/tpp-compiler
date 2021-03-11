from ply.yacc import yacc


class Tree:
    def __init__(self, identifier, children=[], value=None):
        self.identifier = identifier
        self.value = value
        self.children = children

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


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc(module=self)

    def extract_identifier(self, node, identifier):
        return node.children if node.identifier == identifier else [node]

    # === root ===
    def p_root(self, p):
        '''root : expressao_matematica'''
        p[0] = p[1]

    # === expressao matematica ===
    def p_expressao_matematica(self, p):
        'expressao_matematica : soma'
        p[0] = p[1]

    # === soma ===
    def p_soma(self, p):
        '''soma : produto adiciona_ou_subtrai'''
        cs = self.extract_identifier(p[2], 'adiciona_ou_subtrai')
        p[0] = Tree('soma', [p[1], *cs])

    def p_soma1(self, p):
        'soma : produto'
        p[0] = p[1]

    def p_adiciona_ou_subtrai(self, p):
        'adiciona_ou_subtrai : adiciona_ou_subtrai adiciona_ou_subtrai_terminal'
        cs = self.extract_identifier(p[1], 'adiciona_ou_subtrai')
        p[0] = Tree('adiciona_ou_subtrai', [*cs, p[2]])

    def p_adiciona_ou_subtrai1(self, p):
        'adiciona_ou_subtrai : adiciona_ou_subtrai_terminal'
        p[0] = Tree('adiciona_ou_subtrai', [p[1]])

    def p_adiciona_ou_subtrai_terminal(self, p):
        'adiciona_ou_subtrai_terminal : SUBTRACAO produto'
        p[0] = Tree('subtracao', [p[2]])

    def p_adiciona_ou_subtrai_terminal1(self, p):
        'adiciona_ou_subtrai_terminal : ADICAO produto'
        p[0] = Tree('adicionar', [p[2]])

    # === produto ===
    def p_produto(self, p):
        'produto : primario multiplica_ou_divide'
        cs = self.extract_identifier(p[2], 'multiplica_ou_divide')
        p[0] = Tree('produto', [p[1], *cs])

    def p_produto1(self, p):
        'produto : primario'
        p[0] = p[1]

    def p_multiplica_ou_divide(self, p):
        'multiplica_ou_divide : multiplica_ou_divide multiplica_ou_divide_terminal'
        cs = self.extract_identifier(p[1], 'multiplica_ou_divide')
        p[0] = Tree('multiplica_ou_divide', [*cs, p[2]])

    def p_multiplica_ou_divide1(self, p):
        'multiplica_ou_divide : multiplica_ou_divide_terminal'
        p[0] = Tree('multiplica_ou_divide', [p[1]])

    def p_multiplica_ou_divide_terminal(self, p):
        'multiplica_ou_divide_terminal : MULTIPLICACAO primario'
        p[0] = Tree('multiplicar', [p[2]])

    def p_multiplica_ou_divide_terminal1(self, p):
        'multiplica_ou_divide_terminal : DIVISAO primario'
        p[0] = Tree('dividir', [p[2]])

    # === expressao unaria ===
    def p_expressao_unaria(self, p):
        'expressao_unaria : ADICAO primario'
        p[0] = Tree('adicao_unaria', [p[2]])

    def p_expressao_unaria1(self, p):
        'expressao_unaria : SUBTRACAO primario'
        p[0] = Tree('subtracao_unaria', [p[2]])

    # === primario ===
    def p_primario(self, p):
        'primario : PARENTESES_DIR expressao_matematica PARENTESES_ESQ'
        p[0] = p[2]

    def p_primario1(self, p):
        '''primario : numero
                    | id
                    | expressao_unaria'''
        p[0] = p[1]

    # === declaracao de funcao ===
    def p_declaracao_de_funcao(self, p):
        '''declaracao_de_funcao : cabecalho_de_funcao_com_retorno FIM
                                | cabecalho_de_funcao FIM'''
        p[0] = Tree('declaracao_de_funcao', [p[1]])

    def p_declaracao_de_funcao1(self, p):
        '''declaracao_de_funcao : cabecalho_de_funcao_com_retorno declaracoes FIM
                                | cabecalho_de_funcao declaracoes FIM'''
        p[0] = Tree('declaracao_de_funcao', [p[1], p[2]])

    # === declaracões ===
    def p_declaracoes(self, p):
        'declaracoes : numero'
        p[0] = Tree('declaracoes', [p[1]])

    # === cabecalho de funcao (0 ou mais parametros) ===
    def p_cabecalho_de_funcao_com_retorno(self, p):
        'cabecalho_de_funcao_com_retorno : tipo DOIS_PONTOS cabecalho_de_funcao'
        p[0] = Tree('cabecalho_de_funcao_com_retorno', [p[1], p[3]])
    
    def p_cabecalho_de_funcao(self, p):
        'cabecalho_de_funcao : id PARENTESES_DIR PARENTESES_ESQ'
        p[0] = Tree('cabecalho_de_funcao', [p[1]])

    def p_cabecalho_de_funcao1(self, p):
        'cabecalho_de_funcao : id PARENTESES_DIR lista_parametros PARENTESES_ESQ'
        p[0] = Tree('cabecalho_de_funcao', [p[1], p[3]])

    # === lista parametros ===
    def p_lista_parametros(self, p):
        'lista_parametros : lista_parametros VIRGULA lista_variaveis_terminal'
        p[0] = Tree('lista_parametros', [*p[1].children, p[3]])

    def p_lista_parametros_terminal(self, p):
        'lista_parametros : lista_variaveis_terminal'
        p[0] = Tree('lista_parametros', [p[1]])

    # === declaracao de variavel (1 ou mais declaracoes) ===
    def p_declaracao_de_variavel(self, p):
        'declaracao_de_variavel : tipo DOIS_PONTOS lista_declaracao'
        p[0] = Tree('declaracao_de_variavel', [p[1], p[3]])
    
    # === lista declaracao ===
    def p_declaracao_terminal(self, p):
        '''declaracao_terminal : lista_variaveis_terminal
                                | atribuicao'''
        p[0] = p[1]

    def p_lista_declaracao(self, p):
        'lista_declaracao : lista_declaracao VIRGULA declaracao_terminal'
        p[0] = Tree('lista_declaracao', [*p[1].children, p[3]])

    def p_lista_declaracao1(self, p):
        'lista_declaracao : declaracao_terminal'
        p[0] = Tree('lista_declaracao', [p[1]])

    # === tipo ===
    def p_tipo(self, p):
        '''tipo : INTEIRO 
              | FLUTUANTE
              | TEXTO
        '''
        p[0] = Tree('tipo', value=p[1])

    # === id ===
    def p_id(self, p):
        'id : ID'
        p[0] = Tree('id', value=p[1])
    
    def p_pointer(self, p):
        'pointer : COLCHETE_DIR COLCHETE_ESQ'
        p[0] = Tree('pointer')
    
    def p_pointer1(self, p):
        'pointer : COLCHETE_DIR numero_inteiro COLCHETE_ESQ'
        p[0] = p[2]

    def p_id_multi_pointer(self, p):
        'id_pointer : id_pointer pointer'
        p[0] = Tree('id_pointer', [*p[1].children, p[2]], p[1].value)

    def p_id_pointer(self, p):
        'id_pointer : ID pointer'
        p[0] = Tree('id_pointer', [p[2]], p[1])

    # === atribuicao ===
    def p_atribuicao(self, p):
        'atribuicao : lista_variaveis_terminal ATRIBUICAO expressao'
        # '''atribuicao : id_pointer ATRIBUICAO expressao
        #               | id ATRIBUICAO expressao
        # '''
        p[0] = Tree('atribuicao', [p[1], p[3]])

    # === lista de variaveis ===
    def p_lista_variaveis_terminal(self, p):
        '''lista_variaveis_terminal : id_pointer
                                    | id
        '''
        p[0] = p[1]

    # === numero ===
    def p_numero_inteiro(self, p):
        'numero_inteiro : NUMERO_INTEIRO'
        p[0] = Tree('numero_inteiro', value=p[1])

    def p_numero_flutuante(self, p):
        'numero_flutuante : NUMERO_FLUTUANTE'
        p[0] = Tree('numero_flutuante', value=p[1])

    def p_numero_cientifico(self, p):
        'numero_cientifico : NUMERO_CIENTIFICO'
        p[0] = Tree('numero_cientifico', value=p[1])

    def p_numero(self, p):
        '''numero : numero_cientifico
                  | numero_flutuante
                  | numero_inteiro
        '''
        p[0] = p[1]

    # === expressao ===
    def p_expressao(self, p):
        'expressao : numero'
        p[0] = Tree('expressao', [p[1]])

    def p_error(self, p):
        print("ERROR:", p.__dict__ if p else p)

    def parse(self, text: str):
        return self.parser.parse(text)
