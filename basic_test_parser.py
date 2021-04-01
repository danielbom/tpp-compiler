from tpp.Lexer import Lexer, report
from tpp.Parser import Parser
from tpp.Tree import generate_anytree_tree
from anytree.exporter import UniqueDotExporter

code = '''
principal()
    inteiro: x
    x := 10

    repita
        se x > 0 então
            x += 1
        senão
            x -= 1
        fim
    ((x > 0 && x < 100) || (x < 0 && x > -100))

    retorna (0)
fim
'''


lexer = Lexer()
report(code)
parser = Parser(lexer, start='programa')
ast = parser.parse(code)

if ast is not None:
    root = generate_anytree_tree(ast)
    if root is not None:
        UniqueDotExporter(root).to_dotfile("tree.dot")
        UniqueDotExporter(root).to_picture("tree.png")

