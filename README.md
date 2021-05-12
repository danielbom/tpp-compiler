# tpp-compiler

**Operational System**: Ubuntu 20.04

**Python version**: 3.8.5

# Get started

```bash
# Create virtual env
virtualenv -p python3 ./penv

# Activate virtual env
source ./penv/bin/activate

# Install deps
pip install ply
pip install llvmlite
pip install graphviz
pip install argh
```

# Running

Use the following commands to see the helpers of the tpp program.

```bash
./tpp.py tokenize --help
./tpp.py parse --help
./tpp.py semantic --help
```

# Compilation Process

- Lexer:
  * Read the source code and create a stream of tokens.

- Parser:
  * Receivies the stream of tokens and create the Syntax Tree (AST).

- Semantic:
  * preprocessing:
    * Simplify the AST, removing unnecessaries nodes.
    * Transform the AST into a specialized structure, preparing to generate the intermediate code.
  * functions:
    * Check if 'principal' function exists.
    * Check if has 'principal' call into the 'principal' function body.
    * Check if has only 1 declaration by function.
    * Check if all called function has been declared.
    * Check if the parameters length matches.
    * Check if typed function are return statement.
    * Check if has a return statement and the return type matches the value of the expression on the return statement.
  * variables:
    * Check if has only 1 declaration of variables by context.
    * Check if variables are declared.
    * Check if variables are initialized.
    * Check if variables are used.
    * arrays:
      * Check if index dimension are used correctly


- Generator:
  * Generate the intermediate code.

