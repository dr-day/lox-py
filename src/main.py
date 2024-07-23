from lexer import Scanner
from parser import create_parser, print_parse_tree
from evaluator import evaluate

#source = 'print 9+8;print 1+2;'
source = 'var x=2;print x;print 9+8;print 1+2;'
scanner = Scanner(source)
tokens = scanner.scanTokens()
#print(tokens)

parser = create_parser(tokens)
tree = parser()
#print_parse_tree(tree)
evaluate(tree)
