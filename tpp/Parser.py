from ply.yacc import yacc
from tpp.Tree import Tree


class ParserLeaf:
    # === tipos ===
    def p_tipo_inteiro(self, p):
        'tipo_inteiro : INTEIRO'
        p[0] = Tree('INTEIRO', value=p[1])

    def p_tipo_flutuante(self, p):
        'tipo_flutuante : FLUTUANTE'
        p[0] = Tree('FLUTUANTE', value=p[1])

    def p_tipo_texto(self, p):
        'tipo_texto : TEXTO'
        p[0] = Tree('TEXTO', value=p[1])

    # === simbolos especiais ===
    def p_colchete_direito(self, p):
        'colchete_direito : COLCHETE_DIR'
        p[0] = Tree('COLCHETE_DIR', value=p[1])

    def p_colchete_esquerdo(self, p):
        'colchete_esquerdo : COLCHETE_ESQ'
        p[0] = Tree('COLCHETE_ESQ', value=p[1])

    def p_parenteses_direito(self, p):
        'parenteses_direito : PARENTESES_DIR'
        p[0] = Tree('PARENTESES_DIR', value=p[1])

    def p_parenteses_esquerdo(self, p):
        'parenteses_esquerdo : PARENTESES_ESQ'
        p[0] = Tree('PARENTESES_ESQ', value=p[1])

    def p_virgula(self, p):
        'virgula : VIRGULA'
        p[0] = Tree('VIRGULA', value=p[1])

    def p_dois_pontos(self, p):
        'dois_pontos : DOIS_PONTOS'
        p[0] = Tree('DOIS_PONTOS', value=p[1])

    def p_atribuicao(self, p):
        'atribuicao : ATRIBUICAO'
        p[0] = Tree('ATRIBUICAO', value=p[1])

    # === operacoes matematicas ===
    def p_adicao(self, p):
        'adicao : ADICAO'
        p[0] = Tree('ADICAO', value=p[1])

    def p_subtracao(self, p):
        'subtracao : SUBTRACAO'
        p[0] = Tree('SUBTRACAO', value=p[1])

    def p_multiplicacao(self, p):
        'multiplicacao : MULTIPLICACAO'
        p[0] = Tree('MULTIPLICACAO', value=p[1])

    def p_divisao(self, p):
        'divisao : DIVISAO'
        p[0] = Tree('DIVISAO', value=p[1])

    # === operacoes e atribuicao ===
    def p_atribuicao_adicao(self, p):
        'atribuicao_adicao : ADICAO_ATRIBUICAO'
        p[0] = Tree('ADICAO_ATRIBUICAO', value=p[1])

    def p_atribuicao_subtracao(self, p):
        'atribuicao_subtracao : SUBTRACAO_ATRIBUICAO'
        p[0] = Tree('SUBTRACAO_ATRIBUICAO', value=p[1])

    def p_atribuicao_multiplicacao(self, p):
        'atribuicao_multiplicacao : MULTIPLICACAO_ATRIBUICAO'
        p[0] = Tree('MULTIPLICACAO_ATRIBUICAO', value=p[1])

    def p_atribuicao_divisao(self, p):
        'atribuicao_divisao : DIVISAO_ATRIBUICAO'
        p[0] = Tree('DIVISAO_ATRIBUICAO', value=p[1])

    # === operacoes de comparacao ===
    def p_comparacao_igual(self, p):
        'comparacao_igual : IGUAL'
        p[0] = Tree('IGUAL', value=p[1])

    def p_comparacao_diferente(self, p):
        'comparacao_diferente : DIFERENTE'
        p[0] = Tree('DIFERENTE', value=p[1])

    def p_comparacao_menor(self, p):
        'comparacao_menor : MENOR'
        p[0] = Tree('MENOR', value=p[1])

    def p_comparacao_maior(self, p):
        'comparacao_maior : MAIOR'
        p[0] = Tree('MAIOR', value=p[1])

    def p_comparacao_menor_igual(self, p):
        'comparacao_menor_igual : MENORIGUAL'
        p[0] = Tree('MENORIGUAL', value=p[1])

    def p_comparacao_maior_igual(self, p):
        'comparacao_maior_igual : MAIORIGUAL'
        p[0] = Tree('MAIORIGUAL', value=p[1])

    # === operacoes booleana ====
    def p_booleano_negacao(self, p):
        'booleano_negacao : NEGACAO'
        p[0] = Tree('NEGACAO', value=p[1])

    def p_booleano_e(self, p):
        'booleano_e : E_LOGICO'
        p[0] = Tree('E_LOGICO', value=p[1])

    def p_booleano_ou(self, p):
        'booleano_ou : OU_LOGICO'
        p[0] = Tree('OU_LOGICO', value=p[1])

    # === palavras reservadas ===
    def p_se(self, p):
        'se : SE'
        p[0] = Tree('SE', value=p[1])

    def p_entao(self, p):
        'entao : ENTAO'
        p[0] = Tree('ENTAO', value=p[1])

    def p_senao(self, p):
        'senao : SENAO'
        p[0] = Tree('SENAO', value=p[1])

    def p_fim(self, p):
        'fim : FIM'
        p[0] = Tree('FIM', value=p[1])

    def p_repita(self, p):
        'repita : REPITA'
        p[0] = Tree('REPITA', value=p[1])

    def p_ate(self, p):
        'ate : ATE'
        p[0] = Tree('ATE', value=p[1])

    def p_retorna(self, p):
        'retorna : RETORNA'
        p[0] = Tree('RETORNA', value=p[1])

    def p_leia(self, p):
        'leia : LEIA'
        p[0] = Tree('LEIA', value=p[1])

    def p_escreva(self, p):
        'escreva : ESCREVA'
        p[0] = Tree('ESCREVA', value=p[1])

    # === numero ===
    def p_numero_inteiro(self, p):
        'numero_inteiro : NUMERO_INTEIRO'
        p[0] = Tree('NUMERO_INTEIRO', value=p[1])

    def p_numero_flutuante(self, p):
        'numero_flutuante : NUMERO_FLUTUANTE'
        p[0] = Tree('NUMERO_FLUTUANTE', value=p[1])

    def p_numero_cientifico(self, p):
        'numero_cientifico : NUMERO_CIENTIFICO'
        p[0] = Tree('NUMERO_CIENTIFICO', value=p[1])

    # === outros ===
    def p_id(self, p):
        'id : ID'
        p[0] = Tree('ID', value=p[1])

    def p_caracteres(self, p):
        'caracteres : CARACTERES'
        p[0] = Tree('CARACTERES', value=p[1])


class ParserErrorCatcher:
    # === errors ===
    def p_criacao_de_variavel_lista_error(self, p):
        'criacao_de_variaveis_lista : criacao_de_variaveis_lista error var'
        if self.error_state == 1:
            self.error_state += 1
            print('Erro de sintáxe durante a declaração de variáveis.')
            print('É esperado virgulas como separador das variáveis.')
        p.error()

    def p_criacao_de_variaveis_declaracao_error(self, p):
        'criacao_de_variaveis_declaracao : tipo error criacao_de_variaveis_lista'
        if self.error_state == 1:
            self.error_state += 1
            print('Erro de sintáxe durante a declaração de variáveis.')
            print('É esperado ":" (dois pontos) depois do tipo.')
        p.error()

    def p_se_declaracao_error1(self, p):
        'se_declaracao : se expressao error declaracoes se_fim'
        if self.error_state == 1:
            self.error_state += 1
            print('Erro de sintáxe durante a criação da declaração "se".')
            print('É esperado "então" após a expressão da declaração "se".')
        p.error()

    def p_se_declaracao_error2(self, p):
        'se_declaracao : error expressao entao declaracoes se_fim'
        if self.error_state == 1:
            self.error_state += 1
            print('Erro de sintáxe durante a criação da declaração "se".')
            print('É esperado "se" antes da palavra reservada "então".')
        p.error()

    def p_repita_declaracao_error1(self, p):
        'repita_declaracao : repita declaracoes error expressao'
        if self.error_state == 1:
            self.error_state += 1
            print([t.identifier if t else None for t in p])
            print('Erro de sintáxe durante a criação da declaração "repita".')
            print('É esperado "até" após o corpo da declaração "repita"')
        p.error()

    def p_repita_declaracao_error2(self, p):
        'repita_declaracao : error declaracoes ate expressao'
        if self.error_state == 1:
            self.error_state += 1
            print('Erro de sintáxe durante a criação da declaração "repita".')
            print('É esperado "repita" antes das declaração do corpo do "repita"')
        p.error()

    def p_funcao_declaracao_error(self, p):
        'funcao_declaracao : tipo funcao_cabecalho declaracoes error'
        if self.error_state == 1:
            self.error_state += 1
            print('Erro de sintáxe durante declaração de função.')
            print('É esperado "fim" após o corpo da declaração da função')
        p.error()

    def p_funcao_lista_parametros_error(self, p):
        'funcao_cabecalho_lista_parametros : funcao_cabecalho_lista_parametros error funcao_parametro'
        if self.error_state == 1:
            self.error_state += 1
            print('Erro de sintáxe durante declaração de função.')
            print('É esperado "," (virgulas) para a separação de parametros.')
        p.error()

    def p_funcao_parametro_error1(self, p):
        'funcao_parametro : error dois_pontos var'
        if self.error_state == 1:
            self.error_state += 1
            print('Erro de sintáxe durante declaração de função.')
            print(
                'É esperado um tipo antes dos ":" (dois pontos) na declaração de parametros.')
        p.error()

    def p_funcao_parametro_error2(self, p):
        'funcao_parametro : tipo error var'
        if self.error_state == 1:
            self.error_state += 1
            print('Erro de sintáxe durante declaração de função.')
            print(
                'É esperado ":" (dois pontos) depois do tipo na declaração de parametros.')
        p.error()

    def p_adiciona_ou_subtrai_adicao_error(self, p):
        'adiciona_ou_subtrai_terminal : error produto'
        if self.error_state == 1:
            self.error_state += 1
            print('Erro de sintáxe durante uma expressão de soma ou subtração.')
        p.error()

    def p_error(self, p):
        if not p:
            print('Erro fatal: Existem declarações incompletas!')

        if self.error_state == 0 and p:
            print(f'Erro próximo da linha: {p.lineno}')
        self.error_state += 1


class Parser(ParserLeaf, ParserErrorCatcher):
    def __init__(self, lexer, start="programa"):
        self.predecendes = [
            ('left', 'PARENTESES_ESQ', 'COLCHETE_ESQ'),
            ('right', 'PARENTESES_DIR', 'COLCHETE_DIR'),

            ('left', 'VIRGULA'),
            ('left', 'ATRIBUICAO', 'ADICAO_ATRIBUICAO', 'SUBTRACAO_ATRIBUICAO',
             'MULTIPLICACAO_ATRIBUICAO', 'DIVISAO_ATRIBUICAO'),

            ('right', 'ADICAO', 'SUBTRACAO'),
            ('right', 'MULTIPLICACAO', 'DIVISAO'),
            ('right', 'MENOR', 'MAIOR', 'MENORIGUAL', 'MAIORIGUAL'),
            ('right', 'IGUAL', 'DIFERENTE'),
            ('right', 'E_LOGICO', 'OU_LOGICO'),
            ('left', 'NEGACAO'),

            ('left', 'SE', 'REPITA'),
            ('left', 'SENAO'),
            ('left', 'FIM'),
        ]
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.start = start
        self.error_state = 0
        self.parser = yacc(module=self)

    def parse(self, code: str):
        self.error_state = 0
        return self.parser.parse(code)

    def p_vazio(self, p):
        'vazio :'
        p[0] = Tree('vazio')

    def p_tipo(self, p):
        '''tipo : tipo_inteiro
            | tipo_flutuante
            | tipo_texto'''
        p[0] = Tree('tipo', p[1:])

    # programa
    def p_programa(self, p):
        'programa : programa_lista_declaracao'
        p[0] = Tree('programa', p[1:])

    def p_programa_lista_declaracao(self, p):
        'programa_lista_declaracao : programa_lista_declaracao programa_lista_declaracao_terminal'
        p[0] = Tree('programa_lista_declaracao', [*p[1].children, p[2]])

    def p_programa_lista_declaracao_um(self, p):
        'programa_lista_declaracao : programa_lista_declaracao_terminal'
        p[0] = Tree('programa_lista_declaracao', p[1:])

    def p_programa_lista_declaracao_terminal(self, p):
        '''programa_lista_declaracao_terminal : funcao_declaracao
            | criacao_de_variaveis_declaracao
            | atribuicao_declaracao'''
        p[0] = Tree('declaracao', p[1:])

    # === variavel ===
    def p_ponteiro(self, p):
        'ponteiro : colchete_esquerdo colchete_direito'
        p[0] = Tree('ponteiro', p[1:])

    def p_vetor(self, p):
        'vetor : colchete_esquerdo expressao colchete_direito'
        p[0] = Tree('vetor', p[1:])

    def p_var(self, p):
        '''var : var ponteiro
            | var vetor'''
        p[0] = Tree('var', [*p[1].children, p[2]])

    def p_var_um(self, p):
        'var : id'
        p[0] = Tree('var', p[1:])

    # === declaracoes ===
    def p_declaracoes(self, p):
        'declaracoes : declaracoes declaracoes_terminal'
        p[0] = Tree('declaracoes', [*p[1].children, p[2]])

    def p_declaracoes_um(self, p):
        'declaracoes : declaracoes_terminal'
        p[0] = Tree('declaracoes', p[1:])

    def p_declaracoes_terminal(self, p):
        '''declaracoes_terminal : se_declaracao
            | repita_declaracao
            | atribuicao_declaracao
            | retorna_declaracao
            | escreva_declaracao
            | leia_declaracao
            | chamada_de_funcao_declaracao
            | criacao_de_variaveis_declaracao
            | vazio'''
        p[0] = Tree('declaracao', p[1:])

    # === declaracao retorna ===
    def p_retorna_declaracao(self, p):
        'retorna_declaracao : retorna expressao'
        p[0] = Tree('retorna_declaracao', p[1:])

    def p_retorna_declaracao_vazio(self, p):
        'retorna_declaracao : retorna'
        p[0] = Tree('retorna_declaracao', p[1:])

    # === declaracao criacao de variaveis
    def p_criacao_de_variaveis_declaracao(self, p):
        'criacao_de_variaveis_declaracao : tipo dois_pontos criacao_de_variaveis_lista'
        p[0] = Tree('criacao_de_variaveis_declaracao', p[1:])

    def p_criacao_de_variavel_lista(self, p):
        'criacao_de_variaveis_lista : criacao_de_variaveis_lista virgula var'
        p[0] = Tree('criacao_de_variaveis_lista', [*p[1].children, p[2], p[3]])

    def p_criacao_de_variavel_lista_um(self, p):
        'criacao_de_variaveis_lista : var'
        p[0] = Tree('criacao_de_variaveis_lista', p[1:])

    # === declaracao leia ===
    def p_leia_declaracao(self, p):
        'leia_declaracao : leia parenteses_esquerdo var parenteses_direito'
        p[0] = Tree('leia', p[1:])

    # === declaracao escreva ===
    def p_escreva_declaracao(self, p):
        'escreva_declaracao : escreva parenteses_esquerdo expressao parenteses_direito'
        p[0] = Tree('escreva', p[1:])

    # === declaracao chamada de funcao ===
    def p_chamada_de_funcao_declaracao(self, p):
        'chamada_de_funcao_declaracao : id parenteses_esquerdo chamada_de_funcao_parametros parenteses_direito'
        p[0] = Tree('chamada_de_funcao_declaracao', p[1:])

    def p_chamada_de_funcao_parametros(self, p):
        'chamada_de_funcao_parametros : chamada_de_funcao_parametros virgula chamada_de_funcao_parametro'
        p[0] = Tree('chamada_de_funcao_parametros', p[1:])

    def p_chamada_de_funcao_parametros_um(self, p):
        'chamada_de_funcao_parametros : chamada_de_funcao_parametro'
        p[0] = Tree('chamada_de_funcao_parametros', p[1:])

    def p_chamada_de_funcao_parametro(self, p):
        'chamada_de_funcao_parametro : expressao'
        p[0] = Tree('chamada_de_funcao_parametro', p[1:])

    def p_chamada_de_funcao_parametros_vazio(self, p):
        'chamada_de_funcao_parametros : vazio'
        p[0] = Tree('chamada_de_funcao_parametros', p[1:])

    # === declaracao se ===
    def p_se_declaracao(self, p):
        'se_declaracao : se expressao entao declaracoes se_fim'
        corpo = p[4].update_identifier('se_corpo')
        p[0] = Tree('se_declaracao', [p[1], p[2], p[3], corpo, *p[5].children])

    def p_se_fim(self, p):
        'se_fim : fim'
        p[0] = Tree('se_fim', p[1:])

    def p_se_senao_fim(self, p):
        'se_fim : senao declaracoes fim'
        corpo = p[2].update_identifier('se_corpo')
        p[0] = Tree('se_fim', [p[1], corpo, p[3]])

    # === declaracao repita ===
    def p_repita_declaracao(self, p):
        'repita_declaracao : repita declaracoes ate expressao'
        corpo = p[2].update_identifier('repita_corpo')
        p[0] = Tree("repita_declaracao", [p[1], corpo, p[3], p[4]])

    # === declaracao atribuicao ===
    def p_atribuicao_declaracao(self, p):
        'atribuicao_declaracao : var atribuicao_operacao expressao'
        p[0] = Tree('atribuicao_declaracao', p[1:])

    def p_atribuicao_operacao(self, p):
        '''atribuicao_operacao : atribuicao
            | atribuicao_adicao
            | atribuicao_subtracao
            | atribuicao_multiplicacao
            | atribuicao_divisao'''
        p[0] = p[1]

    # === declaracao funcao ===
    def p_funcao_declaracao(self, p):
        'funcao_declaracao : tipo funcao_cabecalho declaracoes fim'
        corpo = p[3].update_identifier('funcao_corpo')
        p[0] = Tree('funcao_declaracao', [p[1], p[2], corpo, p[4]])

    def p_funcao_declaracao_sem_tipo(self, p):
        'funcao_declaracao : funcao_cabecalho declaracoes fim'
        corpo = p[2].update_identifier('funcao_corpo')
        p[0] = Tree('funcao_declaracao', [p[1], corpo, p[3]])

    # === funcao cabecalho ===
    def p_funcao_cabecalho(self, p):
        'funcao_cabecalho : id parenteses_esquerdo funcao_cabecalho_lista_parametros parenteses_direito'
        p[0] = Tree('cabecalho', p[1:])

    def p_funcao_lista_parametros(self, p):
        'funcao_cabecalho_lista_parametros : funcao_cabecalho_lista_parametros virgula funcao_parametro'
        p[0] = Tree('lista_parametros', [*p[1].children, p[2], p[3]])

    def p_funcao_lista_parametros_um(self, p):
        'funcao_cabecalho_lista_parametros : funcao_parametro'
        p[0] = Tree('lista_parametros', p[1:])

    def p_funcao_lista_parametros_vazio(self, p):
        'funcao_cabecalho_lista_parametros : vazio'
        p[0] = Tree('lista_parametros', p[1:])

    def p_funcao_parametro(self, p):
        'funcao_parametro : tipo dois_pontos var'
        p[0] = Tree('parametro', p[1:])

    def p_numero(self, p):
        '''numero : numero_cientifico
            | numero_flutuante
            | numero_inteiro'''
        p[0] = Tree('numero', p[1:])

    # === expressao ===
    def p_expressao(self, p):
        'expressao : expressoes_booleanas'
        p[0] = Tree('expressao', p[1:])

    # E, OU, NOT
    # === expressoes de booleanas ===
    def p_expressoes_booleanas(self, p):
        'expressoes_booleanas : negacao conjuncao_ou_disjuncao'
        p[0] = Tree('expressoes_booleanas', p[1:])

    def p_expressoes_booleanas1(self, p):
        'expressoes_booleanas : negacao'
        p[0] = Tree('expressoes_booleanas', p[1:])

    # === negacao ===
    def p_negacao(self, p):
        'negacao : booleano_negacao expressoes_booleanas_primario'
        p[0] = Tree('negacao', p[1:])

    def p_negacao1(self, p):
        'negacao : expressoes_booleanas_primario'
        p[0] = Tree('negacao', p[1:])

    def p_expressoes_booleanas_primario(self, p):
        'expressoes_booleanas_primario : parenteses_esquerdo expressoes_booleanas parenteses_direito'
        p[0] = Tree('expressoes_booleanas_primario', p[1:])

    def p_expressoes_booleanas_primario1(self, p):
        'expressoes_booleanas_primario : expressoes_de_igualdade'
        p[0] = Tree('expressoes_booleanas_primario', p[1:])

    # === conjuncao ou disjuncao ===
    def p_conjuncao_ou_disjuncao(self, p):
        'conjuncao_ou_disjuncao : conjuncao_ou_disjuncao conjuncao_ou_disjuncao_terminal'
        p[0] = Tree('conjuncao_ou_disjuncao', p[1:])

    def p_conjuncao_ou_disjuncao1(self, p):
        'conjuncao_ou_disjuncao : conjuncao_ou_disjuncao_terminal'
        p[0] = Tree('conjuncao_ou_disjuncao', p[1:])

    def p_conjuncao_ou_disjuncao_terminal(self, p):
        'conjuncao_ou_disjuncao_terminal : booleano_e negacao'
        p[0] = Tree('conjuncao', [p[2]])

    def p_conjuncao_ou_disjuncao_terminal1(self, p):
        'conjuncao_ou_disjuncao_terminal : booleano_ou negacao'
        p[0] = Tree('disjuncao', [p[2]])

    # === expressao de igualdade ===
    def p_expressoes_de_igualdade(self, p):
        'expressoes_de_igualdade : expressao_de_igualdade_primario qualquer_expressoes_de_igualdade'
        p[0] = Tree('expressoes_de_igualdade', p[1:])

    def p_expressoes_de_igualdade1(self, p):
        'expressoes_de_igualdade : expressao_de_igualdade_primario'
        p[0] = Tree('expressoes_de_igualdade', p[1:])

    def p_expressoes_de_igualdade_primario(self, p):
        'expressao_de_igualdade_primario : expressoes_de_comparacao'
        p[0] = Tree('expressao_de_igualdade_primario', p[1:])

    # === qualquer expressao de igualdade ===
    def p_qualquer_expressoes_de_igualdade(self, p):
        'qualquer_expressoes_de_igualdade : comparacao_igual expressao_de_igualdade_primario'
        p[0] = Tree('igual', p[1:])

    def p_qualquer_expressoes_de_igualdade1(self, p):
        'qualquer_expressoes_de_igualdade : comparacao_diferente expressao_de_igualdade_primario'
        p[0] = Tree('diferente', p[1:])

    # === expressoes de comparacao ===
    def p_expressoes_de_comparacao(self, p):
        'expressoes_de_comparacao : expressao_de_comparacao_primario qualquer_expressoes_de_comparacao'
        p[0] = Tree('expressoes_de_comparacao', p[1:])

    def p_expressoes_de_comparacao1(self, p):
        'expressoes_de_comparacao : expressao_de_comparacao_primario'
        p[0] = Tree('expressoes_de_comparacao', p[1:])

    def p_expressoes_de_comparacao_primario(self, p):
        'expressao_de_comparacao_primario : expressao_matematica'
        p[0] = Tree('expressao_de_comparacao_primario', p[1:])

    # === qualquer expressao de comparacao ===
    def p_qualquer_expressoes_de_comparacao(self, p):
        'qualquer_expressoes_de_comparacao : comparacao_menor expressao_de_comparacao_primario'
        p[0] = Tree('menor', p[1:])

    def p_qualquer_expressoes_de_comparacao1(self, p):
        'qualquer_expressoes_de_comparacao : comparacao_maior expressao_de_comparacao_primario'
        p[0] = Tree('maior', p[1:])

    def p_qualquer_expressoes_de_comparacao2(self, p):
        'qualquer_expressoes_de_comparacao : comparacao_menor_igual expressao_de_comparacao_primario'
        p[0] = Tree('menor_igual', p[1:])

    def p_qualquer_expressoes_de_comparacao3(self, p):
        'qualquer_expressoes_de_comparacao : comparacao_maior_igual expressao_de_comparacao_primario'
        p[0] = Tree('maior_igual', p[1:])

    # === expressao matematica ===
    def p_expressao_matematica(self, p):
        'expressao_matematica : soma'
        p[0] = Tree('expressao_matematica', p[1:])

    # === soma ===
    def p_soma(self, p):
        'soma : produto adiciona_ou_subtrai'
        p[0] = Tree('soma', p[1:])

    def p_soma1(self, p):
        'soma : produto'
        p[0] = Tree('soma', p[1:])

    def p_adiciona_ou_subtrai(self, p):
        'adiciona_ou_subtrai : adiciona_ou_subtrai adiciona_ou_subtrai_terminal'
        p[0] = Tree('adiciona_ou_subtrai', p[1:])

    def p_adiciona_ou_subtrai1(self, p):
        'adiciona_ou_subtrai : adiciona_ou_subtrai_terminal'
        p[0] = Tree('adiciona_ou_subtrai', p[1:])

    def p_adiciona_ou_subtrai_adicao(self, p):
        'adiciona_ou_subtrai_terminal : adicao produto'
        p[0] = Tree('adiciona_ou_subtrai_terminal', p[1:])

    def p_adiciona_ou_subtrai_subtracao(self, p):
        'adiciona_ou_subtrai_terminal : subtracao produto'
        p[0] = Tree('adiciona_ou_subtrai_terminal', p[1:])

    # === produto ===
    def p_produto(self, p):
        'produto : literal multiplica_ou_divide'
        p[0] = Tree('produto', p[1:])

    def p_produto1(self, p):
        'produto : literal'
        p[0] = Tree('produto', p[1:])

    def p_multiplica_ou_divide(self, p):
        'multiplica_ou_divide : multiplica_ou_divide multiplica_ou_divide_terminal'
        p[0] = Tree('multiplica_ou_divide', p[1:])

    def p_multiplica_ou_divide1(self, p):
        'multiplica_ou_divide : multiplica_ou_divide_terminal'
        p[0] = Tree('multiplica_ou_divide', p[1:])

    def p_multiplica_ou_divide_terminal(self, p):
        'multiplica_ou_divide_terminal : multiplicacao literal'
        p[0] = Tree('multiplica_ou_divide_terminal', p[1:])

    def p_multiplica_ou_divide_terminal1(self, p):
        'multiplica_ou_divide_terminal : divisao literal'
        p[0] = Tree('multiplica_ou_divide_terminal', p[1:])

    # === expressao unaria ===
    def p_expressao_unaria(self, p):
        'expressao_unaria : adicao literal'
        p[0] = Tree('expressao_unaria', p[1:])

    def p_expressao_unaria1(self, p):
        'expressao_unaria : subtracao literal'
        p[0] = Tree('expressao_unaria', p[1:])

    # === literal ===
    def p_literal(self, p):
        '''literal : numero
                    | caracteres
                    | var
                    | expressao_unaria
                    | chamada_de_funcao_declaracao'''
        p[0] = Tree('literal', p[1:])

    def p_literal1(self, p):
        'literal : parenteses_esquerdo expressao parenteses_direito'
        p[0] = Tree('literal', p[1:])
