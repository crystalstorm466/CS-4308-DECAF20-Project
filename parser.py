import re
import sys
import ply.lex as lex
import ply.yacc as yacc
from scanner import MyLexer


precedence = {}
#yeah this works -LT
class myParser(object): 
    tokens = MyLexer.tokens
    def __init__(self, input_data):
        self.input = input_data
        self.lexer = MyLexer(input_data)
        self.lexer.build()
        self.parser = yacc.yacc(module=self)
    

    def p_program(self, p):
        '''program : statement_list'''
        pass

    def p_statement_list(self, p):
        '''statement_list : statement statement_list
                     | empty '''
        if len(p) == 2:  # Single statement
            p[0] = p[1]  # Pass through
        else:  # Multiple statements
            p[0] = f"{p[1]} {p[2]}"  # Concatenate statements
        pass
    def p_parameter_list(self, p):
        '''parameter_list : T_Int T_IDENTIFIER
                        | empty '''
        pass

    def p_expression_list(self, p):
        '''expression_list : expression
                       | expression "," expression_list '''
    pass      

    def p_statement(self, p):
        '''statement : expression ";"
                     | var_declaration
                     | assignment ";"
                     | T_IDENTIFIER
                     | T_While "(" expression ")" "{" statement_list "}"
                     | T_If if
                     | T_If if_else_statement
                     | T_Return expression ";"
                     | function_declaration "(" expression ")"  "{" statement_list "}" ";"
                     | function_declaration "(" ")" ";"
                     | T_Print
                     | T_Switch "(" expression ")" "{" statement_list "}"'''
        pass

    def p_expression(self, p):
        '''expression : T_IDENTIFIER "=" expression
                  | T_IntConstant
                  | expression "+" expression
                  | expression "-" expression
                  | expression "*" expression
                  | expression "/" expression
                  | expression "<" expression
                  | expression ">" expression
                  | T_IDENTIFIER
                  | expression T_LessEqual expression
                  | expression T_GreaterEqual expression
                  | T_BoolConstant
                  | "(" expression ")"
                  | "{" expression "}"'''
        if len(p) == 4:
            p[0] = f"{p[1]} = {p[3]}"
        elif len(p) == 3:
                if p[2] in ['+', '-', '*', '/', '<', '>', '<=', '>=']:
                    p[0] = f"{p[1]} {p[2]} {p[3]}"
                else:
                    p[0] = p[2]
        elif len(p) == 2:
                p[0] = p[1]
        pass
    def p_T_Print(self, p):
        '''statement : T_Print "("  ")" ";"
                    | T_Print "(" expression ")" ";"
                    | T_Print "(" T_String ")" ";"
                    | T_Print "(" T_Float ")" ";"
                    | T_Print "(" T_Int ")" ";"
                    | T_Print "(" T_BoolConstant ")" ";"
                    | T_Print "(" T_IDENTIFIER ")" ";"'''
        pass

    def p_T_IDENTIFIER(self, p):
        '''x : T_IDENTIFIER "(" ")" ";" 
                 | T_IDENTIFIER "(" expression_list ")" ";"
                 | T_IDENTIFIER "(" T_IDENTIFIER ")" ";"'''
        pass

    def p_T_If(self, p):
        '''if : T_If "(" expression ")" "{" statement_list "}"
                        | T_If "(" expression ")" "{" statement_list "}" T_Else "{" statement_list "}"'''
        pass
    def p_if_else_statement(self, p):
        '''if_else_statement : T_If "(" expression ")" "{" statement_list "}" T_Else "{" statement_list "}"'''
        pass
    def p_T_Switch(self, p):
        '''switch : T_Switch "(" expression ")" "{" T_CaseList "}"
                  | T_Switch "(" expression ")" "{" T_CaseList "}" T_Default ":" statement_list "}"'''
        pass
    def p_T_While(self, p):
        '''while : T_While "(" expression ")" "{" statement_list "}"
                | T_While "(" T_IDENTIFIER ")" "{" statement_list "}" 
                | T_While "(" T_BoolConstant ")" "{" statement_list "}"
                | T_While "(" T_Float ")" "{" statement_list "}"
                | T_While "(" T_Int ")" "{" statement_list "}"
                | T_While "(" T_String ")" "{" statement_list "}"
                | T_While "(" ")" "{" statement_list "}"
                | T_While  "(" x ")" "{" statement_list "}"'''

        pass
    
    def p_term(self, p):
        '''term : factor
                | term "*" factor
                | term "/" factor
                | T_Int "." T_Int'''
        pass

    def p_factor(self, p):
        '''factor : T_IntConstant "="
                  | "(" expression ")"'''
        pass

    def p_empty(self, p):
        'empty :'
        pass

    def p_T_Return(self, p):
        '''return : T_Return expression ";"
                  | T_Return ";"'''
        pass

    def p_function_declaration(self, p):
        '''function_declaration : T_Void T_IDENTIFIER "(" parameter_list ")" "{" statement_list "}"
                            | T_Int T_IDENTIFIER "(" parameter_list ")" "{" statement_list "}"
                            | T_Float T_IDENTIFIER "(" parameter_list ")" "{" statement_list "}"'''
        pass

 
    def p_var_declaration(self, p):
        '''var_declaration : T_Int T_IDENTIFIER ";"
                       | T_Float T_IDENTIFIER ";"
                       | T_String T_IDENTIFIER ";"
                       | T_BoolConstant T_IDENTIFIER ";"
                       | T_Int T_IDENTIFIER "=" T_Int ";"
                       | T_Int T_IDENTIFIER "=" T_Int "." T_Int ";"
                       | T_Float T_IDENTIFIER "=" T_Float "." T_Int ";"
                       | T_Float T_IDENTIFIER "=" T_Float ";"'''
        pass

  
   

    def p_assignment(self, p):
        '''assignment  : T_IDENTIFIER "=" expression "=" ";"
                        | T_IDENTIFIER "=" T_IDENTIFIER "-" expression ";"
                        | assignment ";"
                        | T_IDENTIFIER "=" T_Int "." T_Int ";"
                        | T_IDENTIFIER "=" T_Float "." T_Float ";"'''
        pass
            
    
    


    def find_column(self, input_data, token):
        last_cr = self.input.rfind('\n', 0, token.lexpos)

        if (last_cr < 0):
            last_cr = -1
        col = (token.lexpos - last_cr)
        return (col)

    def p_error(self, p):

        if p:

            line = p.lineno
            col = self.find_column(self.input, p)

            error_line = self.input.splitlines()[line - 1]

            if (hasattr(p, 'value') and isinstance(p.value, str)):
                error_len = len(p.value)
            else:
                    error_len = 1
            
            if p.type == "T_ELSE":
                print(f"*** Error line {line}")
                print(f"{error_line}")
                print(f" " * (col - 1) + "^" * error_len)
                print(f"*** Syntax error")
                exit()
            elif p.type == 'T_IntConstant':
                    max = 3
                    invalid_seqeuence = self.input[col - 1:]
                    for char in invalid_seqeuence:
                        if char.isalnum or char in ['.', '_']:
                            error_len += 1
                            if error_len > max:
                                error_len = max #so it wont spam 
                                break
                        else:
                            break
                    
                    print(f"*** Error line {line}")
                    print(f"{error_line}")
                    print(f" " * (col - 1) + "^" * error_len )
                    print(f"*** Syntax error")
                    exit()
            else:
                 print(f"*** Error line {line}.")
                 print(f"{self.input.splitlines()[p.lineno - 1]}")
                 print(" " * (col - 1) + "^" * error_len) #this line is giving me trouble for bad4.decaf ^^^
                 print("*** Syntax error")
                 exit()
           
        while True:
            tok = self.parser.token()
            if not tok or tok.type == ";":
                break
            
        self.parser.restart()

    def parse(self):
        return self.parser.parse(self.input, lexer=self.lexer.lexer)


def main(): 
    if (len(sys.argv) > 1):
        with open(sys.argv[1], 'r') as file:
            file_content = file.read()
    else:
        print("Error no arguments provided!  Usage: python parser.py <filename>")
        exit(1)
    
    parser = myParser(file_content)
    result = parser.parse()
    print(result)

def check_syntax(file_content):
    lexer.input(file_content)
    for tok in lexer:
        print(tok)
    
    parser = myParser(file_content)

if __name__ == '__main__':
    main()
