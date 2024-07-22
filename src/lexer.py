from tokens import TokenType, simple_tokens, something_equal_tokens, keywords_map, Token

class Scanner:
    def __init__(this, source):
        this.source = source

    def atEnd(this):
        return this.current == len(this.source)
    
    def advance(this):
        next = this.source[this.current]
        this.current += 1
        return next

    def peek(this):
        return(this.source[this.current])

    def match(this, check):
        if this.atEnd():
            return False
        are_same = check == this.source[this.current]
        if are_same:
            this.current += 1
        return are_same
    
    def consume_string_literal(this):
        literal_start = this.current
        while (not this.atEnd()) and this.peek() !='"':
            if this.peek() == '\n':
                this.line += 1
            this.advance()
        if this.atEnd():
            error(this.line, "Unterminated string")
        this.advance()
        return this.source[literal_start: this.current - 1]

    def consume_number_literal(this):
        literal_start = this.current
        while (not this.atEnd()) and check_digit(this.peek()):
            this.advance()
        if this.current + 2 <= len(this.source) and this.peek() =="." and check_digit(this.source[this.current + 1]):
            this.advance()
            while (not this.atEnd()) and check_digit(this.peek()):
                this.advance()
        return this.source[literal_start - 1: this.current]
    
    def consume_identifier(this):
        literal_start = this.current
        while (not this.atEnd()) and (check_identifier(this.peek()) or check_digit(this.peek())):
            this.advance()
        return this.source[literal_start - 1: this.current]
    
    def scanTokens(this):
        this.current = 0
        this.line = 1
        this.tokens = []

        while not this.atEnd():
            next = this.advance()
            if next.isspace():
                if next == "\n":
                    this.line += 1
                continue

            # check for double character symbols like != 
            # comments
            if next =="/" and this.match("/"): 
                while not this.atEnd() and this.peek() != "\n":
                    this.advance()
                continue

            if next in ("!", "<", ">", "=") and this.match("="):
                this.tokens.append(something_equal_tokens[next],)
                continue
 
            if next in simple_tokens:
                this.tokens.append(simple_tokens[next])
                continue
            
            if next =='"':
                literal = this.consume_string_literal()
                this.tokens.append(Token(TokenType.STRING, literal))
                continue

            if check_digit(next):
                literal = this.consume_number_literal()
                this.tokens.append(Token(TokenType.NUMBER, literal))
                continue

            if check_identifier(next):
                literal = this.consume_identifier()
                if literal in keywords_map:
                    this.tokens.append(keywords_map[literal],)
                else:
                    this.tokens.append(Token(TokenType.STRING, literal))
                continue



            error(this.line, f"unexpected {next}")
        
        this.tokens.append((TokenType.EOF,))
        return this.tokens


def check_digit(char):
    return char in "0123456789"

def check_identifier(char):
    return char in "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"




def error(line, message):
    report(line, "", message)


def report(line, where, message):
    print("[line " + str(line) + "] Error" + where + ": " + message)
  

source = """
"this" != "test";
<=  // stuff
/* 09 - 88
6786. 7.89 ?
iouoi_sdf = dsffd
true or false
"""

if __name__ == "__main__":
    scanner = Scanner(source)
    tokens = scanner.scanTokens()

    print(tokens)

    