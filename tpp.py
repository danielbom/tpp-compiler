import argh
from tpp.Lexer import Lexer
from tpp.Parser import Parser
from tpp.Tree import generate_anytree_tree
from anytree.exporter import UniqueDotExporter


def lexer_print_type(text):
    for tok in Lexer().tokenize(text):
        print(tok.type)


def lexer_report(text):
    print("{:^6} {:^9} {:<25} {}".format("Linha", "Posição", "Tipo", "Valor"))
    for tok in Lexer().tokenize(text):
        print("{:^6} {:^9} {:<25} {}".format(
            tok.lineno, tok.lexpos, tok.type, tok.value))


def tokenize(filename, report=False):
    executor = lexer_report if report else lexer_print_type

    with open(filename, encoding="utf-8") as file:
        text = file.read()

    executor(text)


def parse(filename, start='programa', mode='print'):
    lexer = Lexer()
    parser = Parser(lexer, start=start)

    with open(filename, encoding="utf-8") as file:
        text = file.read()

    ast = parser.parse(text)

    if mode == 'print':
        if ast is not None:
            print(ast.str_tree())
        else:
            print(None)
    elif mode == 'dot':
        if ast is not None:
            root = generate_anytree_tree(ast)
            UniqueDotExporter(root).to_dotfile("tree.dot")
        else:
            print(None)


parser = argh.ArghParser()
parser.add_commands([tokenize, parse])


if __name__ == '__main__':
    parser.dispatch()
