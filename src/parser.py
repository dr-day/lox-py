from tokens import TokenType, Token
from collections import namedtuple

Star = namedtuple("Star", ["rule"])
Option = namedtuple("Option", ["rule"])

# Keyword = namedtuple("Keyword", ["name"])

grammar = {
    'program': [Star('declaration'), TokenType.EOF],
    'declaration': ('varDecl', 'statement'),
    'varDecl': [TokenType.VAR, TokenType.IDENTIFIER, Option([TokenType.EQUAL, 'expression']), TokenType.SEMICOLON],
    'statement': ('exprStmt', 'printStmt'),
    'exprStmt': ['expression', TokenType.SEMICOLON],
    'printStmt': [TokenType.PRINT, 'expression', TokenType.SEMICOLON],
    'expression': 'assignment',
    'assignment': ([TokenType.IDENTIFIER, TokenType.EQUAL, 'assignment'], 'equality'),
    'equality': ['comparision', Star([( TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL ), 'comparision'])],
    'comparision': ['term', Star([( TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESSER, TokenType.LESSER_EQUAL ), 'term'])],
    'term': ['factor', Star([( TokenType.MINUS, TokenType.PLUS), 'factor'])],
    'factor': ['unary', Star([( TokenType.SLASH, TokenType.STAR ), 'unary'])],
    'unary': ('primary', [(TokenType.BANG, TokenType.MINUS), 'unary']),
    'primary': (TokenType.NUMBER, TokenType.IDENTIFIER, TokenType.STRING, TokenType.TRUE, TokenType.FALSE, TokenType.NIL, 
                [TokenType.LEFT_PAREN, 'expression', TokenType.RIGHT_PAREN])
}


def create_parser(tokens):

    def parse_rule(position, rule):
        # When calling this function recursively, you must
        # ignore the position value returned if the result value returned is None.
        # This simplifies the code in some cases because you don't need to 
        # track the original position value.
        
        if type(rule) is str:
            position, result = parse_rule(position, grammar[rule])
            if result:
                result = ((rule, *result),)

        elif type(rule) is list:
            result = ()
            for item in rule:
                position, parse_item = parse_rule(position, item)
                if parse_item: 
                    result = (*result, *parse_item) # lists are expanded
                elif parse_item is None: #If any item in a list doesn't parse return None
                    result = None
                    break
                elif len(parse_item) == 0: #Can occur due to an Option or Star rule
                    pass 

        elif type(rule) is tuple:
            start_position = position
            for option in rule: 
                position, result = parse_rule(start_position, option)
                if result: #Find first option that parses
                    break

        elif type(rule) is Star:
            result = ()
            while True: # repeat parsing rule until fails
                check_position, check_result = parse_rule(position, rule.rule)
                if check_result:
                    result = (*result, *check_result)
                    position = check_position
                else:
                    break
        
        elif type(rule) is Option:
            check_position, check_result = parse_rule(position, rule.rule)
            if check_result:
                result = check_result
                position = check_position
            else:
                result = ()
                
        elif type(rule) is TokenType:
            if position < len(tokens) and (tokens[position].type == rule):
                result = (tokens[position],)
                position += 1
            else:
                result = None
        else:
            print(f'ERROR: unknown {type(rule)}')

        #print(type(rule), result)
        return position, result
    
    def parser():
        position, result = parse_rule(0, 'program')
        if position < len(tokens):
            print(f'Parser error: tokens remain after parsing.')
            return None
        return result[0]
    return parser


def print_parse_tree(parse_tree):
    indent = 0
    for c in str(parse_tree):
        if c == '(':
            indent +=1
        elif c == ')':
            indent -=1
        print(c, end="")
        if c == ",":
            print("\n" + "  " * indent, end="")
    print("\n")






