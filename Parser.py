from ply.yacc import yacc

class Tree:
  def __init__(self, identifier, children = [], value = None):
    self.identifier = identifier
    self.value = value
    self.children = children
  
  def str_rec(self, indentation: int):
    spaces = "  " * indentation
    if self.value:
      return spaces + f"Node({self.identifier}, {self.value})"
    elif self.children:
      s = spaces
      s += f"Node({self.identifier}) [\n"
      s += f",\n".join(c.str_rec(indentation + 1) for c in self.children)
      s += "\n" + spaces + "]"
      return s
    else:
      return spaces + f"Node({self.identifier})"

  def __str__(self):
    return self.str_rec(0)
  
  def __repr__(self):
    return str(self)

class Parser:
  def __init__(self, lexer):
    self.lexer = lexer
    self.tokens = lexer.tokens
    self.parser = yacc(module=self)

  def p_declaracao_de_variavel(self, p):
    'declaracao_de_variavel : tipo DOIS_PONTOS lista_variaveis'
    p[0] = Tree('declaracao_de_variavel', [p[1], p[3]])

  def p_tipo(self, p):
    '''tipo : INTEIRO 
          | FLUTUANTE
          | TEXTO
    '''
    p[0] = Tree('tipo', value = p[1])

  def p_id(self, p):
    'id : ID'
    p[0] = Tree('id', value = p[1])

  def p_atribuicao(self, p):
    'atribuicao : id ATRIBUICAO expressao'
    p[0] = Tree('atribuicao', [p[1], p[3]])

  def p_lista_variaveis(self, p):
    '''lista_variaveis : lista_variaveis VIRGULA id
                      | lista_variaveis VIRGULA atribuicao
    '''
    p[0] = Tree('lista_variaveis', [*p[1].children, p[3]])
  
  def p_lista_variaveis1(self, p):
    '''lista_variaveis : atribuicao
                      | id
    '''
    p[0] = Tree('lista_variaveis', [p[1]])
  
  def p_numero(self, p):
    'numero : NUMERO'
    p[0] = Tree('numero', value = p[1])


  def p_expressao(self, p):
    'expressao : numero'
    p[0] = Tree('expressao', [p[1]])

  def parse(self, text: str):
    return self.parser.parse(text)
