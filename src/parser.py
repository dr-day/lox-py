from tokens import TokenType, Token
from collections import namedtuple

Star = namedtuple("Star", ["rule"])

grammar = {
    'expression': 'equality',
    'equality': ['comparision', Star([( TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL ), 'comparision'])],
    'comparision': ['term', Star([( TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESSER, TokenType.LESSER_EQUAL ), 'term'])],
    'term': ['factor', Star([( TokenType.MINUS, TokenType.PLUS), 'factor'])],
    'factor': ['unary', Star([( TokenType.SLASH, TokenType.STAR ), 'unary'])],
    'unary': ('primary', [(TokenType.BANG, TokenType.MINUS), 'unary']),
    'primary': (TokenType.NUMBER, TokenType.STRING, TokenType.TRUE, TokenType.FALSE, TokenType.NIL, 
                [TokenType.LEFT_PAREN, 'expression', TokenType.RIGHT_PAREN])
}


def create_parser(tokens):
    def parse_rule(position, rule):
        if type(rule) is str:
            position, parse_result = parse_rule(position, grammar[rule])
            if parse_result:
                result = ((rule, *parse_result),)
            else:
                result = None

        elif type(rule) is list:
            result = ()
            for item in rule:
                position, parse_item = parse_rule(position, item)
                if parse_item: 
                    result = (*result, *parse_item) # lists are expanded
                elif parse_item is None: #Every item in a list must parse otherwise return None
                    result = None
                    break

        elif type(rule) is tuple:
            result = None
            for option in rule: #Find first option that parses
                position, parse_option = parse_rule(position, option)
                if parse_option:
                    result = parse_option
                    break

        elif type(rule) is Star:
            result = ()
            while True: # repeat parsing rule until fails
                check_position, check_result = parse_rule(position, rule.rule)
                if not check_result:
                    break
                result = (*result, *check_result)
                position = check_position
            return position, result
                
        elif type(rule) is TokenType:
            if position < len(tokens) and (tokens[position].type == rule):
                result = (tokens[position],)
                position += 1
            else:
                result = None

        else:
            print(f'ERROR: unknown {type(rule)}')


        return position, result
    
    def parser():
        position, result = parse_rule(0, 'expression')
        if position >= len(tokens):
            print(f'Parser error: all tokens consumed by no End of File token found.')
            return None
        if tokens[position].type != TokenType.EOF:
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






