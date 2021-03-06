from ply.lex import lex


class Lexer:
    keywords = {
        "inteiro": "INTEIRO",
        "flutuante": "FLUTUANTE",
        "texto": "TEXTO",
        "se": "SE",
        "então": "ENTAO",
        "senão": "SENAO",
        "repita": "REPITA",
        "fim": "FIM",
        "retorna": "RETORNA",
        "leia": "LEIA",
        "escreva": "ESCREVA"
    }

    tokens = [
        "NUMERO_INTEIRO",
        "NUMERO_FLUTUANTE",
        "NUMERO_CIENTIFICO",
        "ADICAO",
        "ADICAO_ATRIBUICAO",
        "SUBTRACAO",
        "SUBTRACAO_ATRIBUICAO",
        "MULTIPLICACAO",
        "MULTIPLICACAO_ATRIBUICAO",
        "DIVISAO",
        "DIVISAO_ATRIBUICAO",
        "PARENTESES_DIR",
        "PARENTESES_ESQ",
        "COLCHETE_DIR",
        "COLCHETE_ESQ",
        "MENOR",
        "MAIOR",
        "MENORIGUAL",
        "MAIORIGUAL",
        "IGUAL",
        "ID",
        "CARACTERES",
        "DIFERENTE",
        "NEGACAO",
        "VIRGULA",
        "DOIS_PONTOS",
        "ATRIBUICAO",
        "E_LOGICO",
        "OU_LOGICO",
    ] + list(keywords.values())

    t_NUMERO_INTEIRO = r"[+\-]?(0|[1-9]\d*)"
    t_NUMERO_FLUTUANTE = r"[+\-]?(0|[1-9]\d*)\.\d+"
    t_NUMERO_CIENTIFICO = r"[+\-]?(0|[1-9]\d*)(\.\d+)?[eE][\+\-]?\d+"
    t_CARACTERES = r"\"(\\\"|[^\"])*\""
    t_ADICAO = r"\+"
    t_SUBTRACAO = r"\-"
    t_MULTIPLICACAO = r"\*"
    t_DIVISAO = r"\/"
    t_ADICAO_ATRIBUICAO = r"\+="
    t_SUBTRACAO_ATRIBUICAO = r"\-="
    t_MULTIPLICACAO_ATRIBUICAO = r"\*="
    t_DIVISAO_ATRIBUICAO = r"\/="
    t_PARENTESES_DIR = r"\("
    t_PARENTESES_ESQ = r"\)"
    t_COLCHETE_DIR = r"\["
    t_COLCHETE_ESQ = r"\]"
    t_MENOR = r"<"
    t_MAIOR = r">"
    t_MENORIGUAL = r"<="
    t_MAIORIGUAL = r">="
    t_IGUAL = r"="
    t_DIFERENTE = r"<>"
    t_NEGACAO = r"\!"
    t_VIRGULA = r","
    t_DOIS_PONTOS = r":"
    t_ATRIBUICAO = r":="
    t_E_LOGICO = r"&&"
    t_OU_LOGICO = r"\|\|"

    t_ignore = ' \t'

    def t_ID(self, t):
        r"[a-zA-Zá-ñÁ-Ñ][_a-zA-Zá-ñÁ-Ñ0-9]*"
        t.type = self.keywords.get(t.value, 'ID')
        return t

    def t_NOVA_LINHA(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_COMENTARIO(self, t):
        r'{(\\}|[^}])*}'

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def __init__(self):
        self.lexer = lex(module=self)

    def tokenize(
        self, text: str = None, filename: str = None, executor=None):
        if executor is None:
            executor = print

        if filename:
            with open(filename) as file:
                text = file.read()

        if not text:
            print("You must pass a text or a filename!")
            return

        self.lexer.input(text)

        # Tokenize
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            executor(tok)
