from Lexer import Lexer

l = Lexer()

with open('./teste.tpp') as file:
  text = file.read()

def on_token(t):
  print(t.type)

l.tokenize(text=text)
