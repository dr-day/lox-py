from lexer import Scanner
from parser import create_parser, print_parse_tree
from evaluator import evaluate
from simplifier import simplifier, desugar

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
print true and 9 and "hi";
print false or 0 or "love";
var y = 2;
while (y < 5) {
    print y;
    y = y +1;
}
"""

# source = """
# var a = 0;
# var temp;

# for (var b = 1; a < 10000; b = temp + b) {
#   print a;
#   temp = a;
#   a = b;
# }
# #  """



source = """
for (var x =1; x <4; x = x + 1) print x;
 """
source = """
var x = 1;
for (; x <4; x = x + 1) print x;
 """


source = """
for (var x = 1; ; x = x + 1) print x;
 """

source = """
for (var x = 1; x < 5; ){
 print x;
 x = x + 1;
 }
"""

# source = """
# var x = 1;
# while (x < 3) {
#  x = x+1;
#  }
# """

scanner = Scanner(source)
tokens = scanner.scanTokens()
#print(tokens)

parser = create_parser(tokens)
tree = parser()
stree = desugar(tree)
stree = simplifier(stree)

# print_parse_tree(stree)
evaluate(stree)
