#!/usr/bin/env ./penv/bin/python3

import argh
import os
import subprocess
from subprocess import CalledProcessError

from tpp.Lexer import Lexer
from tpp.Parser import Parser
from tpp.Semantic import simplify_tree, semantic_check, T
from tpp.Tree import generate_anytree_tree
from anytree.exporter import UniqueDotExporter
from anytree import RenderTree, AsciiStyle

__dirname = os.path.dirname(os.path.abspath(__file__))


def ensure_directory(pathdir):
    if not os.path.isdir(pathdir):
        os.mkdir(pathdir)


def execute_clojure_formatter(text):
    temp_file_name = os.path.join(__dirname, "tmp", "tpp-temp-str.temp.txt")
    clj_script = os.path.join(__dirname, "scripts", "update-output.clj")
    clj_cmd = ["clojure", "-M", clj_script, temp_file_name]

    ensure_directory(os.path.dirname(temp_file_name))

    with open(temp_file_name, mode="w") as tempfile:
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
        print(
            "{:^6} {:^9} {:<25} {}".format(tok.lineno, tok.lexpos, tok.type, tok.value)
        )


def semantic_log(result):
    types_map = {
        T.INTEGER: "inteiro",
        T.FLOAT: "flutuante",
        T.TEXT: "texto",
        T.VOID: "vazio",
        None: "{?}"
    }
    def log_info(info):
        var_name = info.get("variable")
        if var_name:
            print(f'\tNome da variável: "{var_name}"')

        func_name = info.get("function")
        if func_name:
            print(f'\tNome da função: "{func_name}"')

        len_params = info.get("length_parameters")
        if len_params:
            expect = len_params["expect"]
            expect = f"{expect} parâmetro" if expect == 1 else f"{expect} parâmetros"

            result = len_params["result"]
            result = f"apenas {result} parâmetro" if result == 1 else f"{result} parâmetros"
            print(f"\tEsperava {expect}, mas recebeu {result}.")

        typing = info.get("type_match")
        if typing:
            expect = types_map[typing["expect"]]
            result = types_map[typing["result"]]
            print(f'\tEsperava tipo "{expect}", mas recebeu "{result}"')

        typ = info.get("type")
        if typ:
            print(f"\tTipo atual {typ}.")

        dym = info.get("dimention_check")
        if dym:
            result = dym['result']
            result = f"{result} dimensão" if result == 1 else f"{result} dimensões"
            print(f'\tEsperava acesso aproapriado a dimensão {dym["expect"]}, mas recebeu um acesso de {re}.')

        idx = info.get("index_access")
        if idx:
            expect = idx["expect"]
            result = idx["result"]
            print(f'\tEsperava acesso aproapriado ao comprimento {expect}, mas recebeu um acesso no índice {result}.')

    errors_count = len(result.errors)
    warnings_count = len(result.warnings)

    if errors_count:
        e = errors_count
        es = f"{e} erro" if e == 1 else f"{e} erros"
        print(f"Verificação Semantica encontrou {es}.")

    if warnings_count:
        w = warnings_count
        ws = f"{w} alerta" if w == 1 else f"{w} alertas"
        print(f"Verificação Semantica encontrou {ws}.")

    for e in result.errors:
        print()
        print(f">>> Erro: {e.name}")
        if e.ctx.is_global():
            print('\tErro encontrado no escopo "global".')
        else:
            scope_func_name = e.ctx.get_function_name()
            print(f'\tErro encontrado na função "{scope_func_name}"')

        log_info(e.info)

        print("\t", e.get_message(), sep="")

    for w in result.warnings:
        print()
        print(f">>> Alerta: {w.name}")

        if w.ctx.is_global():
            print('\tAlerta encontrado no escopo "global".')
        else:
            scope_func_name = w.ctx.get_function_name()
            print(f'\tAlerta encontrado na função "{scope_func_name}"')

        log_info(e.info)

        print("\t", w.get_message(), sep="")


@argh.arg("-m", "--mode", choices=["report", "type", "complete"])
def tokenize(filename, mode="report"):
    executor = lexer_report
    if mode == "type":
        executor = lexer_print_type
    elif mode == "complete":
        executor = lexer_print_complete

    with open(filename, encoding="utf-8") as file:
        text = file.read()

    executor(text)


@argh.arg(
    "-s", "--start", help="the begin expression to execute the parser [see BNF file]"
)
@argh.arg("-o", "--output", help="name of output file running on 'png' or 'dot' mode")
@argh.arg("-m", "--mode", choices=["strtree", "strclojure", "stranytree", "png", "dot", "noop"])
def parse(filename, start="programa", mode="strtree", output="tree", simplify=False):
    if not os.path.isfile(filename):
        print("Error: File not found")
        return

    if output == "tree":
        output = os.path.join(__dirname, "outputs", output)

    lexer = Lexer()
    parser = Parser(lexer, start=start)

    with open(filename, encoding="utf-8") as file:
        text = file.read()

    ast = parser.parse(text)

    if ast is None:
        print(None)
    elif mode == "noop":
        pass
    else:
        if simplify:
            ast = simplify_tree(ast)

        if mode == "strtree":
            print(ast.str_tree())
        elif mode == "strclojure":
            text = ast.str_clojure()
            execute_clojure_formatter(text)
        elif mode == "png":
            root = generate_anytree_tree(ast)
            UniqueDotExporter(root).to_picture(output + ".png")
        elif mode == "dot":
            root = generate_anytree_tree(ast)
            UniqueDotExporter(root).to_dotfile(output + ".dot")
        elif mode == "stranytree":
            root = generate_anytree_tree(ast)
            print(RenderTree(root, style=AsciiStyle()).by_attr())


def semantic(filename, start="programa"):
    lexer = Lexer()
    parser = Parser(lexer, start=start)

    with open(filename, encoding="utf-8") as file:
        text = file.read()

    ast = parser.parse(text)
    result = semantic_check(ast)
    semantic_log(result)


parser = argh.ArghParser()
parser.add_commands([tokenize, parse, semantic])


if __name__ == "__main__":
    parser.dispatch()
