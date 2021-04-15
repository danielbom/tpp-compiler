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
```

# Compilation Process

- Lexer:
  * Read the source code and create a stream of tokens.

- Parser:
  * Receivies the stream of tokens and create the Syntax Tree (AST).

- Semantic:
  * Simplify the AST, removing unnecessaries nodes.
  * Transform the AST into a specialized structure, preparing to generate the intermediate code.
  * Check if 'principal' function exists.
  * Check if variables are used after the declaration.
  * Check if all called function has been declared.
  * Check if has a return statement and the return type matches the value of the expression on the return statement.

- Generator:
  * Generate the intermediate code.

