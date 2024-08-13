from lexer import Scanner
from parser import create_parser, print_parse_tree
from evaluator import evaluate

#source = 'print 9+8;print 1+2;'
source = """
var x=2;
{
    print x;
    var x = 4;
    {
        print x;
        x = 7;
        print x;
    }
    print x;
}
print x;
if (x > 8) print "hi"; else print "bye";
"""
scanner = Scanner(source)
tokens = scanner.scanTokens()
print(tokens)

parser = create_parser(tokens)
tree = parser()
print_parse_tree(tree)
evaluate(tree)
