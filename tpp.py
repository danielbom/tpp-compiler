#!/usr/bin/env ./penv/bin/python3

import argh
import os
import subprocess
from subprocess import CalledProcessError

from tpp.Lexer import Lexer
from tpp.Parser import Parser
from tpp.Semantic import simplify_tree, semantic_check
from tpp.Tree import generate_anytree_tree
from anytree.exporter import UniqueDotExporter

__dirname = os.path.dirname(os.path.abspath(__file__))


def ensure_directory(pathdir):
    if not os.path.isdir(pathdir):
        os.mkdir(pathdir)


def execute_clojure_formatter(text):
    temp_file_name = os.path.join(__dirname, "tmp", "tpp-temp-str.temp.txt")
    clj_script = os.path.join(__dirname, "scripts", "update-output.clj")
    clj_cmd = ["clojure", "-M", clj_script, temp_file_name]

    ensure_directory(os.path.dirname(temp_file_name))

    with open(temp_file_name, mode='w') as tempfile:
        tempfile.write(text)

    try:
        subprocess.run(clj_cmd)
    except (CalledProcessError, FileNotFoundError):
        print(text)


def lexer_print_complete(text):
    for tok in Lexer().tokenize(text):
        print(tok)


def lexer_print_type(text):
    for tok in Lexer().tokenize(text):
        print(tok.type)


def lexer_report(text):
    print("{:^6} {:^9} {:<25} {}".format("Linha", "Posição", "Tipo", "Valor"))
    for tok in Lexer().tokenize(text):
        print("{:^6} {:^9} {:<25} {}".format(
            tok.lineno, tok.lexpos, tok.type, tok.value))


@argh.arg('-m', '--mode', choices=['report', 'type', 'complete'])
def tokenize(filename, mode='report'):
    executor = lexer_report
    if mode == 'type':
        executor = lexer_print_type
    elif mode == 'complete':
        executor = lexer_print_complete

    with open(filename, encoding="utf-8") as file:
        text = file.read()

    executor(text)


@argh.arg('-s', '--start', help="the begin expression to execute the parser [see BNF file]")
@argh.arg('-o', '--output', help="name of output file running on 'png' or 'dot' mode")
@argh.arg('-m', '--mode', choices=['strtree', 'strclojure', 'png', 'dot', 'noop'])
def parse(filename, start='programa', mode='strtree', output="tree", simplify=False):
    if not os.path.isfile(filename):
        print('Error: File not found')
        return

    if output == 'tree':
        output = os.path.join(__dirname, 'outputs', output)

    lexer = Lexer()
    parser = Parser(lexer, start=start)

    with open(filename, encoding="utf-8") as file:
        text = file.read()

    ast = parser.parse(text)

    if ast is None:
        print(None)
    elif mode == 'noop':
        pass
    else:
        if simplify:
            ast = simplify_tree(ast)

        if mode == 'strtree':
            print(ast.str_tree())
        elif mode == 'strclojure':
            text = ast.str_clojure()
            execute_clojure_formatter(text)
        elif mode == 'png':
            root = generate_anytree_tree(ast)
            UniqueDotExporter(root).to_picture(output + '.png')
        elif mode == 'dot':
            root = generate_anytree_tree(ast)
            UniqueDotExporter(root).to_dotfile(output + '.dot')

def semantic(filename, start='programa'):
    lexer = Lexer()
    parser = Parser(lexer, start=start)

    with open(filename, encoding="utf-8") as file:
        text = file.read()

    ast = parser.parse(text)
    semantic_check(ast)

parser = argh.ArghParser()
parser.add_commands([tokenize, parse, semantic])


if __name__ == '__main__':
    parser.dispatch()
