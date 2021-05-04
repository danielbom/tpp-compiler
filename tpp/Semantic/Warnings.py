class SemanticWarnings:
    MAIN_CALL_ITSELF = "MAIN_CALL_ITSELF"
    VARIABLE_NEVER_USED = "VARIABLE_NEVER_USED"
    IMPLICIT_FLOAT = "IMPLICIT_FLOAT"


class SemanticWarning:
    MESSAGE_MAP = {
        "MAIN_CALL_ITSELF": "A função 'principal' está fazendo uma chamada para si mesma.",
        "VARIABLE_NEVER_USED": "A variável foi declarada mas nunca utilizada.",
        "IMPLICIT_FLOAT": "Coerção implícita de tipos",
    }

    def __init__(self, name, ctx, info={}):
        self.name = name
        self.ctx = ctx
        self.info = info

    def get_message(self):
        return self.MESSAGE_MAP[self.name]
