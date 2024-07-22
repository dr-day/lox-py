from tokens import TokenType

def plus_action(x, y):
    if type(x) == type(y) and type(x) in (float, str):
        return x + y
    else:
        raise TypeError(f"For + operator types must both be either float or str: {x} has type {type(x)} and {y} has type {type(y)}")

def check_numeric(x):
    if type(x) != float:
        raise TypeError(f"For operator need numeric argument: {x} has type {type(x)}")
    return x

def check_numeric_non_zero(x):
    check_numeric(x)
    if x == 0:
        raise ValueError(f"Division by 0")
    return x


binary_action_lookup ={
    TokenType.STAR: lambda x, y: check_numeric(x) * check_numeric(y),
    TokenType.SLASH: lambda x, y: check_numeric(x) / check_numeric_non_zero(y),
    TokenType.PLUS: plus_action,
    TokenType.MINUS: lambda x, y: check_numeric(x) - check_numeric(y),
    TokenType.BANG_EQUAL: lambda x, y: x != y,
    TokenType.EQUAL_EQUAL: lambda x, y: x == y,
    TokenType.GREATER: lambda x, y: check_numeric(x) > check_numeric(y),
    TokenType.GREATER_EQUAL: lambda x, y: check_numeric(x) >= check_numeric(y),
    TokenType.LESSER: lambda x, y: check_numeric(x) < check_numeric(y),
    TokenType.LESSER_EQUAL: lambda x, y: check_numeric(x) <= check_numeric(y)

}

def truth_of(x): 
    return bool(x) #will change in future to match lox's truthiness definiton

def evaluate(tree):
    try:
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
                    return - evaluate(tree[2])
                elif action.type == TokenType.BANG:
                    return not (truth_of(evaluate(tree[2])))
        elif rule == 'primary':
            first_token = tree[1]
            if (first_token.type == TokenType.NUMBER): 
                return float(first_token.value)
            elif (first_token.type == TokenType.STRING):
                return str(first_token.value)
            elif first_token.type == TokenType.TRUE:
                return True
            elif first_token.type == TokenType.FALSE:
                return False
            elif first_token.type == TokenType.NIL:
                return None
            elif first_token.type == TokenType.LEFT_PAREN:
                return evaluate(tree[2])
            print(f"Evaluate error: primary token {first_token} no found.")
        else:
            print(f"error no action for {rule}")
    except (ValueError, TypeError) as error:
        print(error)
        exit(70)
