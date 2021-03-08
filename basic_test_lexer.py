import sys
from tpp.Lexer import Lexer

DEFAULT_FILENAME = "./tpp-codes/test.tpp"

filename = sys.argv[1] if len(sys.argv) == 2 else DEFAULT_FILENAME
lexer = Lexer()

with open(filename) as file:
  text = file.read()

def on_token_dict(t):
  print(t.__dict__)

def on_token(t):
  print("{:^6} {:^9} {:<20} {}".format(t.lineno, t.lexpos, t.type, t.value))

print()
print("{:^6} {:^9} {:^20} {}".format("Linha", "Posição", "Tipo", "Valor"))
lexer.tokenize(text=text, executor=on_token)
print()
