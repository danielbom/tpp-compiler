class SemanticWarnings:
    MAIN_CALL_ITSELF = "MAIN_CALL_ITSELF"
    VARIABLE_NEVER_USED = "VARIABLE_NEVER_USED"
    VARIABLE_NEVER_INITIALIZED = "VARIABLE_NEVER_INITIALIZED"
    IMPLICIT_CAST = "IMPLICIT_CAST"


class SemanticWarning:
    MESSAGE_MAP = {
        "MAIN_CALL_ITSELF": "A função 'principal' está fazendo uma chamada para si mesma.",
        "VARIABLE_NEVER_USED": "A variável foi declarada mas nunca foi usada.",
        "VARIABLE_NEVER_INITIALIZED": "A variável foi declarada mas nunca foi inicializada.",
        "IMPLICIT_CAST": "Coerção implícita de tipos.",
    }

    def __init__(self, name, ctx, info={}):
        self.name = name
        self.ctx = ctx
        self.info = info

    def get_message(self):
        return self.MESSAGE_MAP[self.name]
