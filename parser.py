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
                     | T_If "(" ")" "{" statement_list "}"
                     | T_Return expression ";"
                     | function_declaration "(" expression ")"  "{" statement_list "}" ";"
                     | function_declaration "(" ")" ";"
                     | T_Print
                     | T_Switch "(" expression ")" "{" statement_list "}"
                     | function_call ";"'''
        pass
    def p_function_call(self, p):
        '''function_call : T_IDENTIFIER "(" expression_list ")"'''
        p[0] = f"{p[1]}({p[3]})"


    def p_expression(self, p):
        '''expression : T_IDENTIFIER "=" expression
                  | T_IntConstant
                  | expression "+" expression
                  | expression "-" expression
                  | expression "*" expression
                  | expression "/" expression
                  | expression "<" expression
                  | expression ">" expression
                  | expression "=" expression
                  | T_STRINGCONSTANT
                  | T_IDENTIFIER
                  | expression T_LessEqual expression
                  | expression T_GreaterEqual expression
                  | T_BoolConstant
                  | "(" expression ")"
                  | "{" expression "}"
                  | function_call'''
        if len(p) == 4:
            node = Node("BinaryOp", p[2])
            node.add_child(p[1])
            node.add_child(p[3])
            p[0] = node
        elif len(p) == 3:
                if p[2] in ['+', '-', '*', '/', '<', '>', '<=', '>=']:
                    p[0] = f"{p[1]} {p[2]} {p[3]}"
                else:
                    p[0] = p[2]
        elif len(p) == 2:
                p[0] = p[1]
        else:
            p[0] = Node("Value", p[1])
        
    def p_T_Print(self, p):
        '''statement : T_Print "("  ")" ";"
                    | T_Print "(" expression ")" ";"
                    | T_Print "(" T_String ")" ";"
                    | T_Print "(" T_Float ")" ";"
                    | T_Print "(" T_Int ")" ";"
                    | T_Print "(" T_BoolConstant ")" ";"
                    | T_Print "(" T_IDENTIFIER ")" ";"'''
        if len (p) == 6:
            p[0] = Node("PrintStatement", p[2])
            p[0].add_child(Node("Keyword", p[1])) #T_Print 
            p[0].add_child(Node("OpenParen", [p[2]])) # "("
            p[0].add_child(Node("statement", p[3])) # expression
            p[0].add_child(Node("CloseParen", [p[4]])) # ")"
            p[0].add_child(Node("SemiColon", [p[5]])) # ";"
        else:
            p[0] = Node("PrintStatement". p[2])
            p[0].add_child(Node("Keyword", p[1])) #T_Print 
            p[0].add_child(Node("OpenParen", [p[2]])) # "("
            p[0].add_child(Node("CloseParen", [p[3]])) # ")"
            p[0].add_child(Node("SemiColon", [p[4]])) # ";"


    def p_T_IDENTIFIER(self, p):
        '''x : T_IDENTIFIER "(" ")" ";" 
                 | T_IDENTIFIER "(" expression_list ")" ";"
                 | T_IDENTIFIER "(" T_IDENTIFIER ")" ";"'''
        if len(p) == 6:
            p[0] = Node("Identifier", p[1])
            p[0].add_child(Node("OpenParen", [p[2]])) # "("  
            p[0].add_child(Node("expression_list", p[3])) # expression_list
            p[0].add_childNode("CloseParen", [p[4]]) # ")"
            p[0].add_child(Node("SemiColon", p[5])) # ";"
          #  p[0] = f"{p[1]}({p[3]})"
        else:
            p[0] = Node("Identifier", p[1])
            p[0].add_child(Node("OpenParen", [p[2]])) # "("
            p[0].add_child(Node("CloseParen", [p[3]])) # ")"
            p[0].add_child(Node("SemiColon", [p[4]])) # ";"
            #p[0] = f"{p[1]}()"

    def p_T_If(self, p):
        '''if : T_If "(" expression ")" "{" statement_list "}"
                        | T_If "(" expression ")" "{" statement_list "}" T_Else "{" statement_list "}"'''
        
        if len(p) == 12:
            p[0] = Node("IfStatement", p[1])
            p[0].add_child(Node("OpenParen", [p[2]])) # "("
            p[0].add_child(Node("expression", p[3])) # expression
            p[0].add_child(Node("CloseParen", [p[4]]))
            p[0].add_child(Node("OpenBrace", [p[5]])) # "{"
            p[0].add_child(Node("statement_list", p[6])) # statement_list
            p[0].add_child(Node("CloseBrace", [p[7]])) # "}"
            p[0].add_child(Node("Else", p[8])) # "else"
            p[0].add_child(Node("OpenBrace", [p[9]])) # "{"
            p[0].add_child(Node("statement_list", p[10]))
            p[0].add_child(Node("CloseBrace", p[11]))
        else:
            p[0] = Node("IfStatement", p[1])
            p[0].add_child(Node("OpenParen", [p[2]]))
            p[0].add_child(Node("expression", p[3]))
            p[0].add_child(Node("CloseParen", p[4]))
            p[0].add_child(Node("OpenBrace", p[5]))
            p[0].add_child(Node("statement_list", p[6]))
            p[0].add_child(Node("CloseBrace", p[7]))
        
        
    def p_if_else_statement(self, p):
        '''if_else_statement : T_If "(" expression ")" "{" statement_list "}" T_Else "{" statement_list "}"'''
        
        if len(p) == 12:
            p[0] = Node("IfElseStatement", p[1])
            p[0].add_child(Node("OpenParen", [p[2]]))
            p[0].add_child(Node("expression", p[3]))
            p[0].add_child(Node("CloseParen", p[4]))
            p[0].add_child(Node("OpenBrace", p[5]))
            p[0].add_child(Node("statement_list", p[6]))
            p[0].add_child(Node("CloseBrace", p[7]))
            p[0].add_child(Node("Else", p[8]))
            p[0].add_child(Node("OpenBrace", p[9]))
            p[0].add_child(Node("statement_list", p[10]))
            p[0].add_child(Node("CloseBrace", p[11]))

    def p_T_Switch(self, p):
        '''switch : T_Switch "(" expression ")" "{" T_CaseList "}"
                  | T_Switch "(" expression ")" "{" T_CaseList "}" T_Default ":" statement_list'''
        if len(p) == 11:
            p[0] = Node("SwitchStatement", p[1])
            p[0].add_child(Node("OpenParen", [p[2]]))
            p[0].add_child(Node("expression", p[3]))
            p[0].add_child(Node("CloseParen", p[4]))
            p[0].add_child(Node("OpenBrace", p[5]))
            p[0].add_child(Node("CaseList", p[6]))
            p[0].add_child(Node("CloseBrace", p[7]))
            p[0].add_child(Node("Default", p[8]))
            p[0].add_child(Node("Colon", p[9]))
            p[0].add_child(Node("statement_list", p[10]))
        else:
            p[0] = Node("SwitchStatement", p[1])
            p[0].add_child(Node("OpenParen", [p[2]]))
            p[0].add_child(Node("expression", p[3]))
            p[0].add_child(Node("CloseParen", p[4]))
            p[0].add_child(Node("OpenBrace", p[5]))
            p[0].add_child(Node("CaseList", p[6]))
            p[0].add_child(Node("CloseBrace", p[7]))


    def p_T_While(self, p):
        '''while : T_While "(" expression ")" "{" statement_list "}"
                | T_While "(" T_IDENTIFIER ")" "{" statement_list "}" 
                | T_While "(" T_BoolConstant ")" "{" statement_list "}"
                | T_While "(" T_Float ")" "{" statement_list "}"
                | T_While "(" T_Int ")" "{" statement_list "}"
                | T_While "(" T_String ")" "{" statement_list "}"
                | T_While "(" ")" "{" statement_list "}"
                | T_While  "(" x ")" "{" statement_list "}"'''

        if len(p) == 8:
            p[0] = Node("WhileStatement", p[1])
            p[0].add_child(Node("OpenParen", [p[2]]))
            p[0].add_child(Node("expression", p[3]))
            p[0].add_child(Node("CloseParen", p[4]))
            p[0].add_child(Node("OpenBrace", p[5]))
            p[0].add_child(Node("statement_list", p[6]))
            p[0].add_child(Node("CloseBrace", p[7]))
    
    def p_term(self, p):
        '''term : factor
                | term "*" factor
                | term "/" factor
                | T_Int "." T_Int'''
        if len(p) == 2: #term is a single factor
            p[0] = Node("Term")
            p[0].add_child(p[1])
        elif len(p) == 4: #term is a binary operation (multiplication or division)
            p[0] = Node("BinaryOp", p[2]) # * or /
            p[0].add_child(p[1]) # left operand
            p[0].add_child(p[3]) # right operand
        elif len(p) == 4 and p[2] == ".": #term is a decimal number
            p[0] = Node("Decimal")
            p[0].add_child((IntegerPart, p[1])) #T_int before "."
            p[0].add_child((DecimalPart, p[2])) #.
            p[0].add_child((FractionPart, p[3])) #T_int after "."


    def p_factor(self, p):
        '''factor : T_IntConstant "="
                  | "(" expression ")"'''
        if len(p) == 3:
            p[0] = Node("Assignment")
            p[0].add_child(p[1])
            p[0].add_child(p[2])

    def p_empty(self, p):
        'empty :'
        pass

    def p_T_Return(self, p):
        '''return : T_Return expression ";"
                  | T_Return ";"'''
        if len(p) == 4:
            p[0] = Node("ReturnStatement")
            p[0].add_child(p[1])
            p[0].add_child(p[2])
            p[0].add_child(p[3])

    def p_function_declaration(self, p):
        '''function_declaration : T_Void T_IDENTIFIER "(" parameter_list ")" "{" statement_list "}"
                            | T_Int T_IDENTIFIER "(" parameter_list ")" "{" statement_list "}"
                            | T_Float T_IDENTIFIER "(" parameter_list ")" "{" statement_list "}"
                            | T_BoolType T_IDENTIFIER "(" parameter_list ")" "{" statement_list "}"'''

        p[0] = Node("FunctionDeclaration")
        p[0].add_child(Node("Type", p[1])) #T_Void, T_Int, T_Float, T_BoolType
        p[0].add_child(Node("Identifier", p[2])) #function name
        p[0].add_child(Node("OpenParen", p[3])) # "("
        p[0].add_child(Node("ParameterList", p[4])) #parameter list
        p[0].add_child(Node("CloseParen", p[5])) # ")"
        p[0].add_child(Node("OpenBrace", p[6])) # "{"
        p[0].add_child(Node("StatementList", p[7])) #statement list
        p[0].add_child(Node("CloseBrace", p[8])) # "}"
 
    def p_var_declaration(self, p):
        '''var_declaration : T_Int T_IDENTIFIER ";"
                       | T_Float T_IDENTIFIER ";"
                       | T_String T_IDENTIFIER ";"
                       | T_BoolConstant T_IDENTIFIER ";"
                       | T_Int T_IDENTIFIER "=" T_Int ";"
                       | T_Int T_IDENTIFIER "=" T_Int "." T_Int ";"
                       | T_Float T_IDENTIFIER "=" T_Float "." T_Int ";"
                       | T_Float T_IDENTIFIER "=" T_Float ";"'''
        if len(p) == 8: #float declaration with decimals
            p[0] = Node("VariableDeclaration")
            p[0].add_child(Node("Type", p[1])) #T_Int or T_Float
            p[0].add_child(Node("Identifier", p[2])) #variable name
            p[0].add_child(Node("Assignment", p[3])) # "="
            p[0].add_child(Node("Value", p[4])) #T_Int or T_Float
            p[0].add_child(Node("Decimal", p[5])) #"."
            p[0].add_child(Node("Fraction", p[6])) #T_Int
            p[0].add_child(Node("SemiColon", p[7])) #";"
        elif len(p) == 5: #int declaration
            p[0] = Node("VariableDeclaration")
            p[0].add_child(Node("Type", p[1])) #T_Int or T_Float
            p[0].add_child(Node("Identifier", p[2])) #variable name
            p[0].add_child(Node("Assignment", p[3])) # "="
            p[0].add_child(Node("Value", p[4])) #T_Int or T_Float
        elif len(p) == 4: #variable declaration without assignment
            p[0] = Node("VariableDeclaration")
            p[0].add_child(Node("Type", p[1]))
            p[0].add_child(Node("Identifier", p[2]))
            p[0].add_child(Node("SemiColon", p[3]))
  
   
    def p_assignment(self, p):
        '''assignment : T_IDENTIFIER "=" expression ";"
                      | T_IDENTIFIER "=" T_IDENTIFIER "-" expression ";"
                      | T_IDENTIFIER "=" T_Int "." T_Int ";"
                      | T_IDENTIFIER "=" T_Float "." T_Float ";"
                      | T_IDENTIFIER "=" function_call ";"'''
        if len(p) == 6: #float with decimals
            p[0] = Node("Assignment")
            p[0].add_child(Node("Identifier", p[1]))
            p[0].add_child(Node("Equal", p[2]))
            p[0].add_child(Node("Value", p[3]))
            p[0].add_child(Node("Decimal", p[4]))
            p[0].add_child(Node("Fraction", p[5]))
            p[0].add_child(Node("SemiColon", p[6]))
        elif len(p) == 5: #int assignment
            p[0] = Node("Assignment")
            p[0].add_child(Node("Identifier", p[1]))
            p[0].add_child(Node("Equal", p[2]))
            p[0].add_child(Node("Value", p[3]))
            p[0].add_child(Node("SemiColon", p[4]))
        elif len(p) == 7: #int assignment with subtraction
            p[0] = Node("Assignment")
            p[0].add_child(Node("Identifier", p[1]))
            p[0].add_child(Node("Equal", p[2]))
            p[0].add_child(Node("Value", p[3]))
            p[0].add_child(Node("Subtraction", p[4]))
            p[0].add_child(Node("Expression", p[5]))
            p[0].add_child(Node("SemiColon", p[6]))
        elif len(p) == 4: #function call assignment
            p[0] = Node("Assignment")
            p[0].add_child(Node("Identifier", p[1]))
            p[0].add_child(Node("Equal", p[2]))
            p[0].add_child(Node("FunctionCall", p[3]))
            p[0].add_child(Node("SemiColon", p[4]))
            
    
    


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
                return
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
                    return
            else:
                 print(f"*** Error line {line}.")
                 print(f"{self.input.splitlines()[p.lineno - 1]}")
                 print(" " * (col - 1) + "^" * error_len) #this line is giving me trouble for bad4.decaf ^^^
                 print("*** Syntax error")
                 return           
        while True:
            tok = self.parser.token()
            if not tok or tok.type == ";":
                break
            
        self.parser.restart()

    def parse(self):
        return self.parser.parse(self.input, lexer=self.lexer.lexer)


class Node:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        self.children = []
    def add_child(self, child):
        self.children.append(child)

def format_tree(node, level=0):
    if node is None:
        return []
    
    
    lines = []
    indent = " " * level
    lines.append(f"{indent}{node.type}: {node.value}")

    for child in node.children:
        lines.extend(format_tree(child, level + 1))
    return lines

def write_parser_output(root_node):
    with open("parser_output.out", "w") as f:
        lines =  format_tree(root_node)
        f.write("\n".join(lines))
        # for child in node.children:
        #     write_parser_output(child, depth + 1
    
def main(): 
    if (len(sys.argv) > 1):
        with open(sys.argv[1], 'r') as file:
            file_content = file.read()
    else:
        print("Error no arguments provided!  Usage: python parser.py <filename>")
        exit(1)
    
    parser = myParser(file_content)
    result = parser.parse()
    if result is None:
        print("failed")
    else:
        
        write_parser_output(result)
        print(result)




if __name__ == '__main__':
    main()
