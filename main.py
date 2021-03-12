from tpp.Lexer import Lexer
from tpp.Parser import Parser


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

samples_multidimensional_array = [
  "inteiro: var[10]",
  "inteiro: var[10][100]",
  "inteiro: var[10][100][1000]",
  "inteiro: var[]",
  "inteiro: var[][]",
  "inteiro: var[][100]",
  "inteiro: var[100][]",
  "inteiro: var[][100][]",
]

samples_declaration_function = [
  "principal() fim",
  "inteiro: principal() fim"
]

samples_if = [
  "se 0 então fim",
  "se 0 então 0 fim",
  "se 0 então se 0 então fim fim",
  "se 0 então senão fim",
  "se 0 então 0 senão fim",
  "se 0 então senão 0 fim",
  "se 0 então 0 senão 0 fim",
  "se 0 então se 0 então fim senão fim",
  "se 0 então senão se 0 então senão fim",
  "se 0 então senão se 0 então fim",
]

samples_math_expr = [
  "1",
  "1 + 1",
  "0 - 10",
  "2 * 8",
  "1 + 2 - 5",
  "1 + 2 - 3 * 4 + 5 - 6 + 7 * 8",
  "(1 + 2) * (4 - 2)"
]

samples_math_expr_2 = [
  "-1",
  "-1 + 2",
  "+1",
  "+1 - 2",
  "-(8 / 3 + 1)",
  "1 + 2 - 3 * 4 + 5 - 6 / 7 * 8",
  "x + y - z * x + y - z / g * x",
]

samples_codes = [
  '''
  principal()
    inteiro: x := 10
    x += 1
    retorna (0)
  fim
  '''
]

samples_comparison = [
  '1',
  '1 > 2',
  '1 < 2',
  '1 <> 2',
  '1 = 2',
  '1 >= 2',
  '1 <= 2',
]

samples_booleans = [
  "1",
  "1 && 2",
  "1 || 2",
  "!12",
  "1 && 2 || 3 && 4",
]

samples_pairs_all = [
  ("declaracao_de_variavel", samples_declaration_variable),
  ("declaracao_de_funcao", samples_declaration_function),
  ("declaracao_se", samples_if),
  ("expressao_matematica", samples_math_expr),
  ("expressao_matematica", samples_math_expr_2),
  ("root", samples_codes),
  ('expressoes_de_comparacao', samples_comparison),
  ('expressoes_booleanas', samples_booleans)
]

samples_pairs = [samples_pairs_all[-1]]

i = 0
for pair in samples_pairs:
  start, samples = pair
  lexer = Lexer()
  parser = Parser(lexer, start = start)
  print(start)
  print()
  for s in samples:
    print(f"[{i}]: {s}")
    print('=' * 50)
    ast = parser.parse(s)
    print(ast)
    print('=' * 50)
    print()
    i += 1
