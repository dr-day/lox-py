from tokens import TokenType

def evaluate(tree):
    rule = tree[0]
    print(f'{rule}, {len(tree)}')
    if rule == 'expression':
        return evaluate(tree[1])
    elif rule in ('equality', 'comparision', 'term', 'factor'):
        left_op = evaluate(tree[1])
        for i in range(2, len(tree), 2):
            action = tree[i]
            action_token = action[1][0]
            right_op = evaluate(tree[i + 1])
            if action_token == TokenType.STAR:
                left_op = left_op * right_op
        return left_op
    elif rule == 'unary':
        if len(tree) == 2:
            return evaluate(tree[1])
        else: # must be length 3
            action = tree[1]
            action_token = action[1][0]
            if action_token == TokenType.MINUS:
                return -evaluate(tree[2])
    elif rule == 'primary':
        first_token = tree[1][1]
        if first_token.type == TokenType.NUMBER:
            return float(first_token.value)
    else:
        print(f"error no action for {rule}")
