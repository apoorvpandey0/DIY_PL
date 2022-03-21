from typing import *


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
    def __init__(self,pos_start,pos_end,name,details):

        # Starting position of the error
        self.pos_start = pos_start

        # Ending position of the error - idk
        self.pos_end = pos_end

        # Error name and details
        self.name = name
        self.details = details
    
    def __str__(self) -> str:
        """
            Input: 
                calc> 12+23.3+g
            Output: 
                Illegal Character: g
                File <stdin> , line 1
                12+23.3+g
                        ^
        """
        # Illegal Character: g
        result = f'{self.name}: {self.details}'

        # File <stdin> , line 1
        result += f'\nFile {self.pos_start.filename}, line {self.pos_start.ln + 1}'
        
        line = self.pos_start.filetext[:self.pos_start.col+1]
        
        # 12+23.3+g
        result += f'\n{line}'
        
        #         ^
        result += '\n' + ' ' * (self.pos_start.col) + '^'
        return result

class IllegalCharError(Error):
    def __init__(self,pos_start,pos_end,details):
        super().__init__(pos_start,pos_end,'Illegal Character',details)
                         

#########################################################
# POSITION
#########################################################

class Position:
    def __init__(self,idx,ln,col,filename,filetext):
        # The file will be read as a continuous string of characters, this index represents the position of the character in the string.
        self.idx = idx

        # The line number is the line number in the file.
        self.ln = ln

        # The column number is the column number in the line.
        self.col = col

        # The filename is the name of the file.
        self.filename = filename
        
        # The filetext is the text of the file.
        self.filetext = filetext
    
    def __str__(self):
        return '({},{})'.format(self.ln,self.col)

    def advance(self,current_char) -> None:

        # Move the index to the next character and increase the column number.
        self.idx += 1
        self.col += 1

        # If the current character is a newline, then the line number should be incremented,
        # And the column number should be reset to 0.
        if current_char == '\n':
            self.ln += 1
            self.col = 0
    
    def copy(self) -> 'Position':
        return Position(self.idx,self.ln,self.col,self.filename,self.filetext)


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
    def __init__(self,filename,text) -> None:
        self.text = text
        self.pos = Position(-1,0,-1,filename,text)
        self.current_char = None

        # index and col will get updated to 0
        self.advance()
    
    def advance(self) -> None:
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
    
    def make_tokens(self) -> Tuple[List[Token],Error]:
        tokens = []

        # Build a list of tokens while there are still characters in the input string.
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
                pos_start = self.pos.copy()
                curr_char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start,self.pos,curr_char)
            
        return tokens, None
    
    def get_number(self) -> Tuple[Token,Error]:
        number_str = ''
        dot_count = 0
        while self.current_char is not None and self.current_char.isdigit() or self.current_char == '.':
            # Handle decimal points
            if self.current_char == '.':
                dot_count += 1
                if dot_count > 1: return None, Error(self.pos,self.pos,'Illegal number','Number having two or more decimal points')
            
            # Add to the number string and move to the next character.
            number_str += self.current_char
            self.advance()
        
        # Decide if the number is an integer or a float.
        if dot_count == 1:
            return Token(TT_FLOAT, float(number_str)), None
        else: 
            return Token(TT_INT, int(number_str)), None 

#########################################################
# RUN
#########################################################

def run(filename,text) -> Tuple[List[Token],Error]:
    lexer = Lexer(filename,text)
    tokens, error = lexer.make_tokens()
    return tokens,error