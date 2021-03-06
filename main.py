from tpp.Lexer import Lexer
from tpp.Parser import Parser

lexer = Lexer()
parser = Parser(lexer)

samples_declaration_variable = [
  "inteiro: x",
  "inteiro: x, y",
  "inteiro: x := 10",
  "inteiro: x := 10, y",
  "inteiro: x := 10, y, z := 20",
  "inteiro: x[]",
  "inteiro: x[], y",
  "inteiro: x[] := 10",
  "inteiro: x[] := 10, y",
  "inteiro: x[] := 10, y, z := 20",
  "inteiro: x[100]",
]

samples_declaration_function = [
  "principal() fim",
  "inteiro: principal() fim"
]

samples_if = [
  "se 0 então fim",
  "se 0 então senão fim",
  "se 0 então senão se fim",
  "se 0 então senão se fim",
  "se 0 então senão se senão fim",
]

samples = samples_if

for s in samples:
  print(s)
  # print()
  # lexer.tokenize(s)
  print()
  ast = parser.parse(s)
  print(ast)
  print()

