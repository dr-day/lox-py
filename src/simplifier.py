from tokens import  Token, TokenType
def simplifier(tree):
    if isinstance(tree, tuple) and not isinstance(tree, Token):
        if tree[0] in ('declaration', 'statement', 'expression', 'exprStmt'):
            return simplifier(tree[1])
        if tree[0] in ('assignment', 'comparision', 'equality', 'logic_or', 'logic_and', 'term', 'factor', 'unary', 'call') and len(tree) == 2:
             return simplifier(tree[1])
        else:
            return tuple([simplifier(node) for node in tree])
    else:
        return tree
    
def desugar(tree):
    if isinstance(tree, tuple) and not isinstance(tree, Token):
        if tree[0] == 'forStmt':
            while_loop = ('block', Token(type=TokenType.LEFT_BRACE))
            if not isinstance(tree[3], Token) or tree[3].type  != TokenType.SEMICOLON: #init condition exists
                while_loop += (desugar(tree[3]),)
            #Condition
            while_statement = ('whileStmt', Token(type=TokenType.WHILE), Token(type=TokenType.LEFT_PAREN))
            if not isinstance(tree[4], Token) or tree[4].type  != TokenType.SEMICOLON: #init condition exists:
                while_statement += (desugar(tree[4],),)
            else:
                while_statement += (('primary', Token(type=Token(type=TokenType.TRUE))),)
            while_statement += (Token(type=TokenType.RIGHT_PAREN),)
            if not isinstance(tree[-3], Token) or tree[-3].type  != TokenType.SEMICOLON:
                while_statement_block = ('block', Token(type=TokenType.LEFT_BRACE), desugar(tree[-1]), )
                while_statement_block += (desugar(tree[-3]),)
                while_statement_block += (Token(type=TokenType.RIGHT_BRACE),)
                while_statement += (while_statement_block,)
            else:
                while_statement += (desugar(tree[-1]),)

            while_loop += (while_statement, Token(type=TokenType.RIGHT_BRACE))
            return while_loop
            
        else:
            return tuple([desugar(node) for node in tree])
    else:
        return tree
    
