class SemanticErrors:
    AST_MALFORMED = "AST_MALFORMED"
    MAIN_NOT_FOUND = "MAIN_NOT_FOUND"
    CALL_UNDECLARED_FUNCTION = "CALL_UNDECLARED_FUNCTION"
    SYMBOL_ALREADY_EXISTS = "SYMBOL_ALREADY_EXISTS"

    ASSIGN_VARIABLE_UNDECLARED = "ASSIGN_VARIABLE_UNDECLARED"
    USING_VARIABLE_UNDECLARED = "USING_VARIABLE_UNDECLARED"
    USING_VARIABLE_UNINITIALIZED = "USING_VARIABLE_UNINITIALIZED"
    MULTIPLE_VARIABLE_DECLARATION = "MULTIPLE_VARIABLE_DECLARATION"

    NEGATIVE_VECTOR_SIZE = "NEGATIVE_VECTOR_SIZE"

    WRONG_NUMBER_OF_PARAMETERS = "WRONG_NUMBER_OF_PARAMETERS"
    TYPE_ERROR_ON_FUNCTION_CALL = "TYPE_ERROR_ON_FUNCTION_CALL"
    MULTIPLE_FUNCTION_DECLARATION = "MULTIPLE_FUNCTION_DECLARATION"
    RETURN_VALUE_ON_VOID_FUNCTION = "RETURN_VALUE_ON_VOID_FUNCTION"
    RETURN_NONE_ON_TYPED_FUNCTION = "RETURN_NONE_ON_TYPED_FUNCTION"

    NO_INITIALIZE_STATIC_ARRAY = "NO_INITIALIZE_STATIC_ARRAY"
    INDEX_OUT_OF_THE_RANGE = "INDEX_OUT_OF_THE_RANGE"
    INVALID_INDEX_VALUE = "INVALID_INDEX_VALUE"
    INVALID_INITIALIZATION_INDEX = "INVALID_INITIALIZATION_INDEX"


class SemanticError:
    MESSAGE_MAP = {
        "AST_MALFORMED": "Erro fatal: Algum problema ocorreu e seu programa não pode ser construído.",
        "MAIN_NOT_FOUND": "Função principal não encontrada.",
        "TYPE_ERROR_ON_FUNCTION_CALL": "Chamada de função com tipos incompatíveis.",
        "SYMBOL_ALREADY_EXISTS": "Variáveis e funções com nomes iguais.",
        "ASSIGN_VARIABLE_UNDECLARED": "Tentativa de atribuição em uma variável não declarada.",
        "USING_VARIABLE_UNDECLARED": "Tentativa de utilização de uma variável não declarada.",
        "USING_VARIABLE_UNINITIALIZED": "Tentativa de utilização de uma variável não inicializada.",
        "MULTIPLE_VARIABLE_DECLARATION": "Multiplas declarações de uma variável no mesmo escopo.",
        "CALL_UNDECLARED_FUNCTION": "Tentativa de invocar uma função não declarada.",
        "WRONG_NUMBER_OF_PARAMETERS": "Quantidade incorreta de parametros.",
        "NEGATIVE_VECTOR_SIZE": "Tamanho de vetor não deve ser negativo ou nulo (0).",
        "RETURN_VALUE_ON_VOID_FUNCTION": "Existem valores sendo retornados de uma função sem retorno.",
        "RETURN_NONE_ON_TYPED_FUNCTION": "Nenhum valor esta sendo retornado de uma função tipada.",
        "NO_INITIALIZE_STATIC_ARRAY": "Vetores estáticos não deve receber atribuições.",
        "INDEX_OUT_OF_THE_RANGE": "Tentativa de acessar um índice inválido.",
        "INVALID_INITIALIZATION_INDEX": "Tentativa de inicialização de ponteiro invalida.",
        "INVALID_INDEX_VALUE": "Valor inválido para uso de índice e declaração de vetor.",
    }

    def __init__(self, name, ctx, info={}):
        self.name = name
        self.ctx = ctx
        self.info = info

    def get_message(self):
        return self.MESSAGE_MAP[self.name]
