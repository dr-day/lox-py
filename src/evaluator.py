from tokens import TokenType

binary_action_lookup ={
    TokenType.STAR: lambda x, y: x * y,
    TokenType.SLASH: lambda x, y: x / y,
    TokenType.PLUS: lambda x, y: x + y,
    TokenType.MINUS: lambda x, y: x - y

}


def evaluate(tree):
    rule = tree[0]
    if rule == 'expression':
        return evaluate(tree[1])
    elif rule in ('equality', 'comparision', 'term', 'factor'):
        left_op = evaluate(tree[1])
        for i in range(2, len(tree), 2):
            action = tree[i]
            right_op = evaluate(tree[i + 1])
            left_op = binary_action_lookup[action.type](left_op, right_op)
        return left_op
    elif rule == 'unary':
        if len(tree) == 2:
            return evaluate(tree[1])
        else: # must be length 3
            action = tree[1]
            if action.type == TokenType.MINUS:
                return -evaluate(tree[2])
    elif rule == 'primary':
        first_token = tree[1]
        if first_token.type == TokenType.NUMBER:
            return float(first_token.value)
    else:
        print(f"error no action for {rule}")
