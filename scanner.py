import re
import sys
import ply.lex as lex


class MyLexer(object):
    def __init__(self, input_data):
        self.input = input_data 

    
    reserved = {
        'if': 'T_If',
        'return': 'T_Return',
        'break': 'T_Break',
        'func': 'T_Func',
        'string': 'T_String',
        'continue': 'T_Continue',
        'else': 'T_Else',
        'int': 'T_Int',
        'var': 'T_Var',
        'extern': 'T_Extern',
        'null': 'T_Null',
        'package': 'T_Package',
        'void': 'T_Void',
        'while': 'T_While',
        'true': 'T_BoolConstant',
        'false': 'T_BoolConstant',
        'switch': 'T_Switch',
        'case_list': 'T_CaseList',
        'default'  : 'T_Default',
        'for' : 'T_For',


    }

    tokens = [
        'T_logicaland',
        'T_Assign',
        'T_BoolType',
        'T_Comment',
        'T_IDENTIFIER',
        'T_STRINGCONSTANT',
        'T_CHARCONSTANT',
        'T_FloatConstant',
        'T_IntConstant',
        'T_LeftShift',
        'T_RightShift',
        'T_Not',
        'T_Or',
        'T_Whitespace',
        'Keyword',
        'Operator',
        'Semicolon',
        'T_Print',
        'T_Main',
        'T_GreaterEqual',
        'T_LessEqual',
        'T_Float'
    ] + list(reserved.values())


    literals = [ 
    '{', 
    '}', 
    '+', 
    '-',
    '!',
    '*',
    '/',
    '<',
    '>',
    '=',
    '(',
    ')',
    ';',
    '%',
    ',',
    ]
    
    t_ignore = ' \t'


    def t_T_logicaland (self, t):
        r'\&&'
        return t
   
    def t_T_BoolType(self, t):
        r'\bool'
        return t
    
    def t_T_Void(self, t):
        r'void'
        return t
    def t_T_Print(self, t):
        r'Print'
        return t
    def t_T_IDENTIFIER(self, t):
        r'\b[a-zA-Z_][a-zA-Z0-9_]*!?'
        t.type = self.reserved.get(t.value, 'T_IDENTIFIER')
        return t

    def t_T_LEFTSHIFT(self, t):
        r'\<\<'
        return t
    def t_T_RIGHTSHIFT(self, t):
        r'\>\>'
        return t
    def t_T_LessEqual(self, t):
        r'<='
        t.type = 'T_LessEqual'
        return t
    def t_T_GreaterEqual(self, t):
        r'>='
        t.type = 'T_GreaterEqual'
        return t
    def t_T_If(self, t):
        r'if'
        return t
    def t_T_Else(self, t):
        r'else'
        return t
    def t_T_For(self, t):
        r'for'
        return t

    def t_T_String(self, t):
        r'(String)'
        return t

    def t_T_STRINGCONSTANT(self, t):
        # r'\".*\"'
        r'"(?:[^"\\\n]|\\.)*"'
        t.valid = t.value
        t.value = t.value
        return t
    def t_T_BoolConstant(self, t):
        r'(true|false)'
        return t
    

    def t_T_Return(self, t):
        r'Return'
        return t

    def t_Comment(self, t):
        r'//.*'
        return t

    def t_Int(self, t):
        r'int'
        return t

    def t_T_Float(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_T_IntConstant(self, t):
        r'[0-9]+'
        t.valid = int(t.value)
        t.value = int(t.value)
        return t
    def t_T_FloatConstant(self, t):
         r'\d+\.\d+'
         t.valid = float(t.value)
         t.value = float(t.value)
  
    # def t_WHITESPACE(self, t):
    #     r'\s+'
    #     return t
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)


#literals
    def t_LBRACE(self, t):
        r'\{'
        t.type = '{'
        return t

    def t_RBRACE(self, t):
        r'\}'
        t.type = '}'
        return t
    def t_LEFTPAREN(self, t):
        r'\('
        t.type = '('
        return t 
    def t_RIGHTPAREN(self, t):
        r'\)'
        t.type = ')'
        return t
    def t_SemiColon(self, t):
        r';'
        t.type = ';'
        return t
    def t_Equal(self, t):
        r'='
        t.type = '='
        return t
    def t_T_Comma(self, t):
        r','
        t.type = ','
        return t
    def t_Plus(self, t):
        r'\+'
        t.type = '+'
        return t
    def t_Subtract(self, t):
        r'\-'
        t.type ='-'
        return t
    def t_Factorial(self, t):
        r'\!'
        t.type='!'
        return t
    def t_Multiply(self, t):
        r'\*'
        t.type = '*' 
        return t
    def t_Divide(self, t):
         r'\/'
         t.type = '/'
         return t
    def t_LessThan(self, t):
        r'\<'
        t.type='<'
        return t
    def t_GreaterThan(self, t):
        r'\>'
        t.type = '>'
        return t   
    def t_RightShift(self, t):
        r'>>'
        t.type = '>>'
        return t
    def t_LeftShift(self, t):
        r'<<'
        t.type = '<<'
        return t
        

        
    def t_error(self, t):
        print(f"Illegal character {t.value[0]}")
        t.lexer.skip(1)


    def find_column (self, token):
        line_start = self.input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1



    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok: 
                break
            #print(tok.type, tok.value, tok.lineno, tok.lexpos)
            start_col = self.find_column(tok)
            if (isinstance(tok.value, int)):
                end_col = start_col + len(str(tok.value)) - 1
            else:
                end_col = start_col + len(tok.value) - 1
           
            literals = set(self.literals)

            if (tok.type in literals):
                print(f" {tok.value:5} line {tok.lineno} Cols {start_col} - {end_col} is \'{tok.type}\'")
            elif (tok.type in ['T_IntConstant', 'T_STRINGCONSTANT']):
                print(f" {tok.value:4} line {tok.lineno} Cols {start_col} - {end_col} is {tok.type} (value = {tok.value})")
            elif (tok.type == 'T_BoolConstant'):
                print(f" {tok.value:5} line {tok.lineno} Cols {start_col} - {end_col} is {tok.type} (value = {tok.value})")
            else:
                print(f" {tok.value:5} line {tok.lineno} Cols {start_col} - {end_col} is {tok.type}")

           # print(f" {tok.value:5} line {tok.lineno} Cols {self.find_column(tok)} is {tok.type}")



def main():
    if (len(sys.argv) > 1):
        with open(sys.argv[1], 'r') as file:
            file_content = file.read()
    else:
        print("Please provide a file to scan")
        exit(1)

    m = MyLexer(file_content)
    m.build()
    m.test(file_content)

if __name__ == '__main__':
    main()

# this is my old attempt I just want to leave this here so you can see a failed attempt
# def scanner(file):
    
#     token_regex = re.compile(master_pattern)
#     line_num = 1
#     for match in token_regex.finditer(file):
#         kind = match.lastgroup
#         value = match.group(kind)
#         if kind == 'WHITESPACE':
#             continue
#         elif kind == 'COMMENT':
#             continue
#         elif kind == 'MISMATCH':
#             print(f'{value} is not a valid token')
    
#         print(f'{kind}: {value}')
#         print(f'{kind}: {value} at line {line_num}' )
#         # we need the token line col is the '('
#         #so ex: ( line 10 Col 8 -8 )
#         #         line_num+=1
# token_specification = [
#     ('KEYWORD', r'\b(if|else|while|for|break|continue|return)\b'),
#     ('NUMBER', r'\b[0-9]+\b'),
#     ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
#     ('OPERATOR', r'[+\-*/=]'),
#     ('PUNCTUATION', r'[.,;(){}[\]]'),
#     ('WHITESPACE', r'\s+'),
#     ('MISMATCH', r'.'),
#     ('COMMENT', r'//.*'),
# ]
# master_pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

