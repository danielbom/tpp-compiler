from ply.yacc import yacc
from tpp.Tree import Tree


class Parser:
    def __init__(self, lexer, start = "root"):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.start = start
        self.parser = yacc(module=self)

    def extract_many(self, node, identifier):
        return node.children if node.identifier == identifier else [node]

    # === root ===
    def p_root(self, p):
        '''root : declaracao_de_funcao
                | declaracao_de_variavel'''
        p[0] = p[1]

    # === declaracões ===
    def p_declaracoes(self, p):
        'declaracoes : declaracoes declaracoes_terminal'
        p[0] = Tree('declaracoes', [*p[1].children, p[2]])
    
    def p_declaracoes1(self, p):
        'declaracoes : declaracoes_terminal'
        p[0] = Tree('declaracoes', [p[1]])

    def p_declaracoes_terminal(self, p):
        '''declaracoes_terminal : declaracao_retorno
                        | operacao_atribuicao
                        | declaracao_de_variavel'''
        p[0] = p[1]

    # === declaracao retorno ===
    def p_declaracao_retorno(self, p):
        'declaracao_retorno : RETORNA expressao'
        p[0] = Tree('retorna', [p[2]])

    def p_declaracao_retorno1(self, p):
        'declaracao_retorno : RETORNA'
        p[0] = Tree('retorna')

    # === declaracao se ===

    # === declaracao de funcao (0 ou mais parametros) ===
    def p_declaracao_de_funcao(self, p):
        'declaracao_de_funcao : cabecalho_de_funcao FIM'
        p[0] = Tree('declaracao_de_funcao', [p[1]])

    def p_declaracao_de_funcao1(self, p):
        'declaracao_de_funcao : cabecalho_de_funcao corpo_funcao FIM'
        p[0] = Tree('declaracao_de_funcao', [p[1], p[2]])
    
    def p_corpo_funcao(self, p):
        'corpo_funcao : declaracoes'
        p[0] = p[1].update_identifier('corpo_funcao')
    
    def p_cabecalho_de_funcao(self, p):
        '''cabecalho_de_funcao : cabecalho_de_funcao_com_retorno
                                | cabecalho_de_funcao_vazio'''
        p[0] = p[1]

    def p_cabecalho_de_funcao_com_retorno(self, p):
        'cabecalho_de_funcao_com_retorno : tipo DOIS_PONTOS cabecalho_de_funcao_vazio'
        p[0] = Tree('cabecalho_de_funcao_com_retorno', [p[1], p[3]])

    def p_cabecalho_de_funcao_vazio(self, p):
        'cabecalho_de_funcao_vazio : id PARENTESES_DIR PARENTESES_ESQ'
        p[0] = Tree('cabecalho_de_funcao_vazio', [p[1]])

    def p_cabecalho_de_funcao_vazio1(self, p):
        'cabecalho_de_funcao_vazio : id PARENTESES_DIR lista_parametros PARENTESES_ESQ'
        p[0] = Tree('cabecalho_de_funcao_vazio', [p[1], p[3]])

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

    def p_lista_declaracao(self, p):
        'lista_declaracao : lista_declaracao VIRGULA lista_declaracao_terminal'
        p[0] = Tree('lista_declaracao', [*p[1].children, p[3]])

    def p_lista_declaracao1(self, p):
        'lista_declaracao : lista_declaracao_terminal'
        p[0] = Tree('lista_declaracao', [p[1]])

    def p_lista_declaracao_terminal(self, p):
        '''lista_declaracao_terminal : lista_variaveis_terminal
                                    | atribuicao'''
        p[0] = p[1]

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
        p[0] = Tree('pointer', value = p[2])

    def p_id_multi_pointer(self, p):
        'id_pointer : id_pointer pointer'
        p[0] = Tree('id_pointer', [*p[1].children, p[2]], p[1].value)

    def p_id_pointer(self, p):
        'id_pointer : ID pointer'
        p[0] = Tree('id_pointer', [p[2]], p[1])

    # === operacao atribuicao ===
    def p_operacao_atribuicao(self, p):
        '''operacao_atribuicao : soma_atribuicao
                                | subtracao_atribuicao
                                | multiplicacao_atribuicao
                                | divisao_atribuicao'''
        p[0] = p[1]
    
    def p_soma_atribuicao(self, p):
        'soma_atribuicao : lista_variaveis_terminal ADICAO_ATRIBUICAO expressao'
        p[0] = Tree('soma_atribuicao', [p[1], p[3]])
    
    def p_subtracao_atribuicao(self, p):
        'subtracao_atribuicao : lista_variaveis_terminal SUBTRACAO_ATRIBUICAO expressao'
        p[0] = Tree('subtracao_atribuicao', [p[1], p[3]])
    
    def p_multiplicacao_atribuicao(self, p):
        'multiplicacao_atribuicao : lista_variaveis_terminal MULTIPLICACAO_ATRIBUICAO expressao'
        p[0] = Tree('multiplicacao_atribuicao', [p[1], p[3]])
    
    def p_divisao_atribuicao(self, p):
        'divisao_atribuicao : lista_variaveis_terminal DIVISAO_ATRIBUICAO expressao'
        p[0] = Tree('divisao_atribuicao', [p[1], p[3]])

    # === atribuicao ===
    def p_atribuicao(self, p):
        'atribuicao : lista_variaveis_terminal ATRIBUICAO atribuicao_terminal'
        p[0] = Tree('atribuicao', [p[1], p[3]])
    
    def p_atribuicao_terminal(self, p):
        '''atribuicao_terminal : expressao
                                | caracteres'''
        p[0] = p[1]

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
    
    # === caracteres ===
    def p_caracteres(self, p):
        'caracteres : CARACTERES'
        p[0] = Tree('caracteres', value=p[1])

    # === expressao ===
    def p_expressao(self, p):
        'expressao : expressoes_booleanas'
        p[0] = Tree('expressao', [p[1]])

    # E, OU, NOT
    # === expressoes de booleanas ===
    def p_expressoes_booleanas(self, p):
        'expressoes_booleanas : negacao conjuncao_ou_disjuncao'
        cs = self.extract_many(p[2], 'conjuncao_ou_disjuncao')
        p[0] = Tree('expressoes_booleanas', [p[1], *cs])

    def p_expressoes_booleanas1(self, p):
        'expressoes_booleanas : negacao'
        p[0] = p[1]
    
    # === negacao ===
    def p_negacao(self, p):
        'negacao : NEGACAO expressoes_booleanas_primario'
        p[0] = Tree('negacao', [p[2]])
    
    def p_negacao1(self, p):
        'negacao : expressoes_booleanas_primario'
        p[0] = p[1]

    def p_expressoes_booleanas_primario(self, p):
        'expressoes_booleanas_primario : PARENTESES_DIR expressoes_booleanas PARENTESES_ESQ'
        p[0] = p[2]
    
    def p_expressoes_booleanas_primario1(self, p):
        'expressoes_booleanas_primario : expressoes_de_comparacao'
        p[0] = p[1]

    # === conjuncao ou disjuncao ===
    def p_conjuncao_ou_disjuncao(self, p):
        'conjuncao_ou_disjuncao : conjuncao_ou_disjuncao conjuncao_ou_disjuncao_terminal'
        cs = self.extract_many(p[1], 'conjuncao_ou_disjuncao')
        p[0] = Tree('conjuncao_ou_disjuncao', [*cs, p[2]])
    
    def p_conjuncao_ou_disjuncao1(self, p):
        'conjuncao_ou_disjuncao : conjuncao_ou_disjuncao_terminal'
        p[0] = Tree('conjuncao_ou_disjuncao', [p[1]])
    
    def p_conjuncao_ou_disjuncao_terminal(self, p):
        'conjuncao_ou_disjuncao_terminal : E_LOGICO negacao'
        p[0] = Tree('conjuncao', [p[2]])
        
    def p_conjuncao_ou_disjuncao_terminal1(self, p):
        'conjuncao_ou_disjuncao_terminal : OU_LOGICO negacao'
        p[0] = Tree('disjuncao', [p[2]])

    # === expressoes de comparacao ===
    def p_expressoes_de_comparacao(self, p):
        'expressoes_de_comparacao : expressao_de_comparacao_primario qualquer_expressoes_de_comparacao'
        p[0] = Tree('expressoes_de_comparacao', [p[2].prepend(p[1])])

    def p_expressoes_de_comparacao1(self, p):
        'expressoes_de_comparacao : expressao_de_comparacao_primario'
        p[0] = p[1]
    
    def p_expressoes_de_comparacao_primario(self, p):
        'expressao_de_comparacao_primario : expressao_matematica'
        p[0] = p[1]
    
    # === qualquer expressao de comparacao ===
    def p_qualquer_expressoes_de_comparacao(self, p):
        'qualquer_expressoes_de_comparacao : MENOR expressao_de_comparacao_primario'
        p[0] = Tree('menor', [p[2]])

    def p_qualquer_expressoes_de_comparacao1(self, p):
        'qualquer_expressoes_de_comparacao : MAIOR expressao_de_comparacao_primario'
        p[0] = Tree('maior', [p[2]])

    def p_qualquer_expressoes_de_comparacao2(self, p):
        'qualquer_expressoes_de_comparacao : MENORIGUAL expressao_de_comparacao_primario'
        p[0] = Tree('menor_igual', [p[2]])

    def p_qualquer_expressoes_de_comparacao3(self, p):
        'qualquer_expressoes_de_comparacao : MAIORIGUAL expressao_de_comparacao_primario'
        p[0] = Tree('maior_igual', [p[2]])

    def p_qualquer_expressoes_de_comparacao4(self, p):
        'qualquer_expressoes_de_comparacao : IGUAL expressao_de_comparacao_primario'
        p[0] = Tree('igual', [p[2]])

    def p_qualquer_expressoes_de_comparacao5(self, p):
        'qualquer_expressoes_de_comparacao : DIFERENTE expressao_de_comparacao_primario'
        p[0] = Tree('diferente', [p[2]])

    # === expressao matematica ===
    def p_expressao_matematica(self, p):
        'expressao_matematica : soma'
        p[0] = p[1]

    # === soma ===
    def p_soma(self, p):
        '''soma : produto adiciona_ou_subtrai'''
        cs = self.extract_many(p[2], 'adiciona_ou_subtrai')
        p[0] = Tree('soma', [p[1], *cs])

    def p_soma1(self, p):
        'soma : produto'
        p[0] = p[1]

    def p_adiciona_ou_subtrai(self, p):
        'adiciona_ou_subtrai : adiciona_ou_subtrai adiciona_ou_subtrai_terminal'
        cs = self.extract_many(p[1], 'adiciona_ou_subtrai')
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
        cs = self.extract_many(p[2], 'multiplica_ou_divide')
        p[0] = Tree('produto', [p[1], *cs])

    def p_produto1(self, p):
        'produto : primario'
        p[0] = p[1]

    def p_multiplica_ou_divide(self, p):
        'multiplica_ou_divide : multiplica_ou_divide multiplica_ou_divide_terminal'
        cs = self.extract_many(p[1], 'multiplica_ou_divide')
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
    
    # === error ===
    def p_error(self, p):
        print("ERROR:")
        if p:
            print(p)
            print(p.__dict__)

    # === parse ===
    def parse(self, text: str):
        return self.parser.parse(text)
