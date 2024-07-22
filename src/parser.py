from tokens import TokenType
from collections import namedtuple

Star = namedtuple("Star", ["rule"])
List = namedtuple("List", ["rule"])
Option = namedtuple("Option", ["rule"])

grammar = {
    'expression': 'equality',
    'equality': ['comparision', Star([( TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL ), 'comparision'])],
    'comparision': ['term', Star([( TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL ), 'term'])],
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
                # ignore empty length lists.
                if parse_item:
                    result = (*result, *parse_item)
                elif parse_item is None:
                    result = None
                    break

        elif type(rule) is tuple:
            result = None
            for option in rule:
                position, parse_option = parse_rule(position, option)
                if parse_option:
                    result = parse_option
                    break

        elif type(rule) is TokenType:
            if position < len(tokens) and (tokens[position][0] == rule):
                result = (('token', tokens[position]),)
                position += 1
            else:
                result = None
        elif type(rule) is Star:
            result = ()
            # print(f'checking starrule {rule.rule}')
            while True:
                check_position, check_result = parse_rule(position, rule.rule)
                if check_result:
                    result = (*result, *check_result)
                    position = check_position
                else:
                    # print(f'returning {position}, {result}')
                    return position, result
            
        else:
            print(f'ERROR: unknown {type(rule)}')
        return position, result

    # simplify calling of parser so do not need to specify position or have it returned
    return lambda x: parse_rule(0, x)[1] 




def print_parse_tree(parse_tree):
    indent = 0
    for c in str(*parse_tree):
        if c == '(':
            print("\n" + "  " * indent, end="")
            indent +=1
        elif c == ')':
            indent -=1
        print(c, end="")
    print("\n")






