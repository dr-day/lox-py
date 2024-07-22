from lexer import Scanner
from parser import create_parser, print_parse_tree
from tokens import TokenType
from evaluator import evaluate
tokens = [TokenType.MINUS, TokenType.NUMBER, TokenType.STAR, TokenType.NUMBER, TokenType.STAR, TokenType.NUMBER]

source = "-9*7"
scanner = Scanner(source)
tokens = scanner.scanTokens()
print(tokens)
parser = create_parser(tokens)
tree = parser('expression')
print(tree)
print_parse_tree(tree)
print(evaluate(tree[0]))
