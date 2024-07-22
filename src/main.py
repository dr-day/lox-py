from lexer import Scanner
from parser import create_parser, print_parse_tree
from evaluator import evaluate

source = '9+8'
#source = '"sdfds" + false'
scanner = Scanner(source)
tokens = scanner.scanTokens()
# print(tokens)

#parser = create_parser(tokens[:-1])
#parser = create_parser(tokens[:-1] + [Token(TokenType.MINUS)])
parser = create_parser(tokens)
tree = parser()
print_parse_tree(tree)
print(evaluate(tree))
