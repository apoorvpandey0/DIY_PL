from typing import List,Tuple


#########################################################
# CONSTANTS
#########################################################

DIGITS = '0123456789'
TT_INT     =  'INT'
TT_FLOAT   =  'FLOAT'
TT_PLUS    =  'PLUS'
TT_MINUS   =  'MINUS'
TT_MUL     =  'MUL'
TT_DIV     =  'DIV'
TT_LPAREN  =  'LPAREN'
TT_RPAREN  =  'RPAREN'


#########################################################
# ERROR
#########################################################

class Error:
    def __init__(self,name,details):
        self.name = name
        self.details = details
    
    def __str__(self):
        return '{}: {}'.format(self.name,self.details)

class IllegalCharError(Error):
    def __init__(self,pos,details):
        super().__init__('Illegal Character',
                         '{} at position {}'.format(details,pos))


#########################################################
# TOKEN
#########################################################

class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, etc
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', etc
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INT, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

#########################################################
# LEXER
#########################################################

class Lexer:
    def __init__(self,text) -> None:
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()
    
    def advance(self) -> None:
        self.pos+=1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def make_tokens(self) -> Tuple[List[Token],Error]:
        tokens = []

        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, '+'))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, '-'))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, '*'))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, '/'))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, '('))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, ')'))
                self.advance()
            elif self.current_char.isdigit():
                token, error = self.get_number()
                if error: return [], error
                tokens.append(token)
            else:
                return [], IllegalCharError(self.pos,self.current_char)
            
        return tokens, None
    
    def get_number(self) -> Tuple[Token,Error]:
        number_str = ''
        dot_count = 0
        while self.current_char is not None and self.current_char.isdigit() or self.current_char == '.':
            if self.current_char == '.':
                dot_count += 1
                if dot_count > 1: return None, Error('Illegal number','Number having two or more decimal points')
            number_str += self.current_char
            self.advance()
        if dot_count == 1:
            return Token(TT_FLOAT, float(number_str)), None
        elif dot_count >1:
            print('Too many dots')
        else: 
            return Token(TT_INT, int(number_str)), None 

#########################################################
# RUN
#########################################################

def run(text) -> Tuple[List[Token],Error]:
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    return tokens,error