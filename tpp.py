from Lexer import Lexer
from Parser import Parser

lexer = Lexer()
parser = Parser(lexer)

samples = [
  "inteiro: x",
  "inteiro: x, y",
  "inteiro: x := 10",
  "inteiro: x := 10, y",
  "inteiro: x := 10, y, z := 20",
]

for s in samples:
  print(s)
  # print()
  # lexer.tokenize(s)
  print()
  ast = parser.parse(s)
  print(ast)
  print()

