import sys
from tpp.Lexer import Lexer

DEFAULT_FILENAME = "./tpp-codes/test.tpp"

filename = sys.argv[1] if len(sys.argv) == 2 else DEFAULT_FILENAME
lexer = Lexer()

with open(filename) as file:
    text = file.read()

print()
print("{:^6} {:^9} {:^20} {}".format("Linha", "Posição", "Tipo", "Valor"))
for t in lexer.tokenize(text=text):
    print("{:^6} {:^9} {:<20} {}".format(t.lineno, t.lexpos, t.type, t.value))
print()
