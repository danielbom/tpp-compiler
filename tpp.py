#!/usr/bin/env ./penv/bin/python3

import argh
import os
import subprocess
from subprocess import CalledProcessError

from tpp.Lexer import Lexer
from tpp.Parser import Parser
from tpp.Semantic import simplify_tree, semantic_check, T
from tpp.Generator import build_intermediate_code
from tpp.Tree import generate_anytree_tree
from anytree.exporter import UniqueDotExporter
from anytree import RenderTree, AsciiStyle

__dirname = os.path.dirname(os.path.abspath(__file__))


def ensure_directory(pathdir):
    if not os.path.isdir(pathdir):
        os.mkdir(pathdir)


def shell(*args, **kwargs):
    try:
        subprocess.run(*args, **kwargs)
        return True
    except (CalledProcessError, FileNotFoundError) as e:
        print(e)
        return False


def execute_clojure_formatter(text):
    temp_file_name = os.path.join(__dirname, "tmp", "tpp-temp-str.temp.txt")
    clj_script = os.path.join(__dirname, "scripts", "update-output.clj")
    clj_cmd = ["clojure", "-M", clj_script, temp_file_name]

    ensure_directory(os.path.dirname(temp_file_name))

    with open(temp_file_name, mode="w") as tempfile:
        tempfile.write(text)

    shell(clj_cmd)


def generate_binary(input_ll, output_exe):
    shell(["llc", input_ll, "-filetype=obj"])
    shell(["gcc", "out.o", "-o", output_exe])


def generate_execution(filename_ll, output_dot, png=True, xdot_open=False):
    """
    Auxiliary function to view the result of the code generation process

    Parameters
    ----------
    filename_ll : str
        Filename of intermediate code (ext: .ll)
    output_dot : str
        Filename of output_dot dot file (ext: .dot)
    """
    output_png = output_dot
    if not output_dot.endswith(".dot"):
        output_png = f"{output_png}.png"
        output_dot = f"{output_dot}.dot"
    else:
        output_png = f"{output_dot[:-4]}.png"

    # Generate .dot file
    opt_cmd = ["opt", "--dot-cfg", "-analyze", filename_ll]
    mv_cmd = ["mv", ".main.dot", output_dot]
    if shell(opt_cmd) and shell(mv_cmd):
        # Generate png
        if png:
            with open(output_png, "wb") as redirect:
                shell(["dot", "-Tpng", output_dot], stdout=redirect)
        # Open xdot viewer
        if xdot_open:
            shell(["xdot", output_dot])


def lexer_print_complete(text):
    for tok in Lexer().tokenize(text):
        print(tok)


def lexer_print_type(text):
    for tok in Lexer().tokenize(text):
        print(tok.type)


def lexer_report(text):
    print("{:^6} {:^9} {:<25} {}".format("Linha", "Posição", "Tipo", "Valor"))
    for tok in Lexer().tokenize(text):
        print("{:^6} {:^9} {:<25} {}".format(tok.lineno, tok.lexpos, tok.type, tok.value))


def semantic_log(result):
    types_map = {
        T.INTEGER: "inteiro",
        T.FLOAT: "flutuante",
        T.TEXT: "texto",
        T.VOID: "vazio",
        None: "{?}",
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
            ex = len_params["expect"]
            ex = f"{ex} parâmetro" if ex == 1 else f"{ex} parâmetros"

            re = len_params["result"]
            re = f"apenas {re} parâmetro" if re == 1 else f"{re} parâmetros"
            print(f"\tEsperava {ex}, mas recebeu {re}.")

        typing = info.get("type_match")
        if typing:
            ex = types_map[typing["expect"]]
            re = types_map[typing["result"]]
            print(f'\tEsperava tipo "{ex}", mas recebeu "{re}"')

        typ = info.get("type")
        if typ:
            print(f"\tTipo atual {typ}.")

        dym = info.get("dimention_check")
        if dym:
            re = dym["result"]
            re = f"{re} dimensão" if re == 1 else f"{re} dimensões"
            ex = dym["expect"]
            print(f'\tEsperava acesso aproapriado a dimensão {ex}, mas recebeu um acesso de {re}.')

        idx = info.get("index_access")
        if idx:
            ex = idx["expect"]
            re = idx["result"]
            print(f"\tEsperava acesso aproapriado ao comprimento {ex}, mas recebeu um acesso no índice {re}.")

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

        log_info(w.info)

        print("\t", w.get_message(), sep="")


@argh.arg("-m", "--mode", choices=["report", "type", "complete"])
def lexer(filename, mode="report"):
    executor = lexer_report
    if mode == "type":
        executor = lexer_print_type
    elif mode == "complete":
        executor = lexer_print_complete

    with open(filename, encoding="utf-8") as file:
        text = file.read()

    executor(text)

@argh.arg("-s", "--start", help="The begin expression to execute the parser [see BNF file]")
@argh.arg("-o", "--output", help="Name of output file running on 'png' or 'dot' mode")
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


@argh.arg("-o", "--output")
@argh.arg("--dot", help="Generate a dot file with the result of execution")
@argh.arg("--png", help="Generate a dot file and a png with the result of execution")
@argh.arg("--xdot-open", help="Generate a dot file and open the xdot viewer of the result of execution")
def generate(filename, output="out.ll", outdot="out.dot", outexec="a.out", dot=False, png=False, xdot_open=False, binary=False):
    output_dot = outdot
    output_ll = output
    output_exe = outexec

    lexer = Lexer()
    parser = Parser(lexer)

    with open(filename, encoding="utf-8") as file:
        text = file.read()

    ast = parser.parse(text)
    result = semantic_check(ast)
    semantic_log(result)

    if result.errors:
        print()
        print("Falha durante o processo de compilação.")
        print("O código não deve possuir erros para poder ser compilado!")
    else:
        filename = os.path.basename(filename)
        ast = result.ast
        ctx = result.program_ctx
        intermediate_code = build_intermediate_code(filename, ast, ctx)

        with open(output_ll, "w") as file:
            file.write(str(intermediate_code))
        
        if dot or png or xdot_open:
            generate_execution(output_ll, output_dot, png, xdot_open)
        
        if binary:
            generate_binary(output_ll, output_exe)


parser = argh.ArghParser()
parser.add_commands([lexer, parse, semantic, generate])


if __name__ == "__main__":
    parser.dispatch()
