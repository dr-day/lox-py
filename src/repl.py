from lexer import Scanner
from parser import create_parser
from evaluator import evaluate

print("Lox REPL")
while True:
    source = input("> ")
    if source == "":
        exit()
    scanner = Scanner(source)
    tokens = scanner.scanTokens()
    parser = create_parser(tokens)
    tree = parser()
    if tree:
        evaluate(tree)