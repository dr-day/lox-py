from tokens import TokenType, Token

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

class Scope:
    def __init__(self):
        self.data = dict()

    def add(self, index):
        self.data[index] = None

    def contains(self, index):
        return index in self.data.keys()

    def __setitem__(self, index, value):
        if index in self.data.keys():
            self.data[index] = value
        else:
            raise ValueError(f'{index} variable not defined')
        
    def __getitem__(self, index):
        if index in self.data.keys():
            return self.data[index]
        else:
            raise ValueError(f'{index} variable not found')

class Environment:
    def __init__(self):
        self.scopes = [Scope()]
    
    def enter_scope(self):
        self.scopes.append(Scope())

    def exit_scope(self):
        self.scopes.pop()

    def add(self, index):
        print(f'adding {index}')
        self.scopes[-1].add(index)

    def __setitem__(self, index, value):
        for scope in reversed(self.scopes):
            if scope.contains(index):
                scope[index] = value
                return
        raise ValueError(f'{index} variable not defined')
        
    def __getitem__(self, index):
        for scope in reversed(self.scopes):
            if scope.contains(index):
                return scope[index]
        raise ValueError(f'{index} variable not found')


environment = Environment()

def evaluate(tree):
    #print(environment.scopes[-1].data)

    try:
        rule = tree[0]
        if rule == 'program':
            for subrule in tree[1:]:
                if not (type(subrule) == Token and subrule.type == TokenType.EOF):
                    evaluate(subrule)
        elif rule == 'block':
            environment.enter_scope()
            for i in range(2, len(tree) - 1):
                evaluate(tree[i])
            environment.exit_scope()
        elif rule in ('declaration', 'statement', 'expression', 'exprStmt'):
            return evaluate(tree[1])
        elif rule == 'assignment':
            if len(tree) == 2:
                return evaluate(tree[1])
            else:
                var_name = tree[1].value
                environment[var_name] = evaluate(tree[3])
        elif rule == 'varDecl':
            var_name = tree[2].value
            environment.add(var_name)
            if len(tree) == 6:
                environment[var_name] = evaluate(tree[4])
            else:
                environment[var_name] = None
        elif rule == 'printStmt':
            print(evaluate(tree[2]))
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
            elif (first_token.type == TokenType.IDENTIFIER):
                return environment[first_token.value]
            elif first_token.type == TokenType.TRUE:
                return True
            elif first_token.type == TokenType.FALSE:
                return False
            elif first_token.type == TokenType.NIL:
                return None
            elif first_token.type == TokenType.LEFT_PAREN:
                return evaluate(tree[2])
            print(f"Evaluate error: primary token {first_token} no found.")
        elif rule == 'ifStmt':
            if truth_of(evaluate(tree[3])):
                return evaluate(tree[5])
            elif len(tree) == 8:
                return evaluate(tree[7])
            else:
                return None
        else:
            print(f"error no action for {rule}")
    except (ValueError, TypeError) as error:
        print(error)
        exit(70)
