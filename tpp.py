import argh
from tpp.Lexer import Lexer

def lexer_print_type(text):
    for tok in Lexer().tokenize(text):
        print(tok.type)

def lexer_report(text):
    print("{:^6} {:^9} {:<25} {}".format("Linha", "Posição", "Tipo", "Valor"))
    for tok in Lexer().tokenize(text):
        print("{:^6} {:^9} {:<25} {}".format(tok.lineno, tok.lexpos, tok.type, tok.value))

def tokenize(filename, report=False):
    executor = lexer_report if report else lexer_print_type

    with open(filename, encoding="utf-8") as file:
        text = file.read()
    
    executor(text)

parser = argh.ArghParser()
parser.add_commands([tokenize])


if __name__ == '__main__':
    parser.dispatch()
