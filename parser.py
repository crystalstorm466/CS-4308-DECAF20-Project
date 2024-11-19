import re
import sys
import ply.lex as lex
import ply.yacc as yacc
from scanner import MyLexer


precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQ', 'NEQ'),
        ('left', 'LT', 'LEQ', 'GT', 'GEQ'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULT', 'DIV', 'MOD'),
        ('left', 'LEFTSHIFT', 'RIGHTSHIFT'),
        ('right', 'NOT'),
    )
start = 'program'

#yeah this works -LT
class myParser(object): 
    tokens = MyLexer.tokens
    def __init__(self, input_data):
        self.input = input_data
        self.lexer = MyLexer(input_data)
        self.lexer.build()
        self.parser = yacc.yacc(module=self, write_tables=False)
    

    def p_program(self, p):
        '''program : statement_list'''
        root = Node("Program")
        root.add_child(p[1])
        p[0] = root

    def p_statement_list(self, p):
        '''statement_list : statement_list statement
                          | statement'''
        if len(p) == 3:
            if p[1] and isinstance(p[1], Node) and p[1].type == "StmtList":
                p[1].add_child(p[2])
                p[0] = p[1]
            else:
                node = Node("StmtList")
                node.add_child(p[1])
                node.add_child(p[2])
                p[0] = node
        else:
            node = Node("StmtList")
            node.add_child(p[1])
            p[0] = node



    def p_statement(self, p):
        '''statement : var_declaration
                     | function_declaration 
                     | assignment ";"
                     | expression ";"
                     | function_call ";"
                     | T_Return expression ";"
                     | T_While
                     | if
                     | if_else_statement
                     | for_loop
                     | switch 
                     | print
                     | while
                     | return
                     | type'''
        p[0] = p[1]  # Pass the node from child rules


    def p_var_declaration(self, p):
        '''var_declaration : type T_IDENTIFIER ";"
                           | type T_IDENTIFIER "=" expression ";" '''
        node = Node("VarDecl")
        node.add_child(Node("Type", p[1]))
        node.add_child(Node("Identifier", p[2]))
        if len(p) > 4:
            assign_node = Node("AssignExpr")
            assign_node.add_child(Node("FieldAccess", p[2]))
            assign_node.add_child(Node("Operator", "="))
            assign_node.add_child(p[4])
            node.add_child(assign_node)
        p[0] = node

        # if len(p) == 5:
        #     assign_node = Node("AssignExpr")
        #     assign_node.add_child(Node("FieldAccess", Node("Identifier", p[2])))
        #     assign_node.add_child(Node("Operator", "="))
        #     assign_node.add_child(p[4])
        #     node.add_child(assign_node)
        # if len(p) == 8: #float declaration with decimals
        #     p[0].add_child(Node("Type", p[1])) #T_Int or T_Float
        #     p[0].add_child(Node("Identifier", p[2])) #variable name
        #     p[0].add_child(Node("Assignment", p[3])) # "="
        #     p[0].add_child(Node("Value", p[4])) #T_Int or T_Float
        #     p[0].add_child(Node("Decimal", p[5])) #"."
        #     p[0].add_child(Node("Fraction", p[6])) #T_Int
        #     p[0].add_child(Node("";"", p[7])) #";"
        # elif len(p) == 5: #int declaration
        #     p[0].add_child(Node("Type", p[1])) #T_Int or T_Float
        #     p[0].add_child(Node("Identifier", p[2])) #variable name
        #     p[0].add_child(Node("Assignment", p[3])) # "="
        #     p[0].add_child(Node("Value", p[4])) #T_Int or T_Float
        # elif len(p) == 4: #variable declaration without assignment
        #     p[0].add_child(Node("Type", p[1]))
        #     p[0].add_child(Node("Identifier", p[2]))
        #     p[0].add_child(Node("";"", p[3]))




    def p_assignment(self, p):
        '''assignment : T_IDENTIFIER "=" expression'''
        node = Node("AssignExpr", lineno=p.lineno(2))
        field_access = Node("FieldAccess", lineno=p.lineno(1))
        field_access.add_child(Node("Identifier", p[1], lineno=p.lineno(1)))
        node.add_child(field_access)
        node.add_child(Node("Operator", p[2], p.lineno(2)))
        node.add_child(p[3])
        p[0] = node
        
        # if len(p) == 6: #float with decimals
        #     p[0].add_child(Node("Identifier", p[1]))
        #     p[0].add_child(Node("Equal", p[2]))
        #     p[0].add_child(Node("Value", p[3]))
        #     p[0].add_child(Node("Decimal", p[4]))
        #     p[0].add_child(Node("Fraction", p[5]))
        #     p[0].add_child(Node("";"", p[6]))
        # elif len(p) == 5: #int assignment
        #     p[0] = Node("Assignment")
        #     p[0].add_child(Node("Identifier", p[1]))
        #     p[0].add_child(Node("Equal", p[2]))
        #     p[0].add_child(Node("Value", p[3]))
        #     p[0].add_child(Node("";"", p[4]))
        # elif len(p) == 7: #int assignment with subtraction
        #     p[0] = Node("Assignment")
        #     p[0].add_child(Node("Identifier", p[1]))
        #     p[0].add_child(Node("Equal", p[2]))
        #     p[0].add_child(Node("Value", p[3]))
        #     p[0].add_child(Node("Subtraction", p[4]))
        #     p[0].add_child(Node("Expression", p[5]))
        #     p[0].add_child(Node("";"", p[6]))
        # elif len(p) == 4: #function call assignment
        #     p[0] = Node("Assignment")
        #     p[0].add_child(Node("Identifier", p[1]))
        #     p[0].add_child(Node("Equal", p[2]))
        #     p[0].add_child(Node("FunctionCall", p[3]))
        #     p[0].add_child(Node("";"", p[4]))
        # return p[0]

    def p_expression(self, p):
        '''expression : expression "+" expression
                  | expression "-" expression
                  | expression "*" expression
                  | expression "/" expression
                  | expression T_LessThan expression
                  | expression T_GreaterThan expression
                  | expression T_LessEqual expression
                  | expression T_GreaterEqual expression
                  | expression T_LogicalAnd expression
                  | expression T_LogicalOr expression
                  | expression T_NotEquals expression
                  | expression T_Equals expression
                  | "!" expression
                  | T_Not expression
                  | T_IDENTIFIER
                  | T_BoolConstant
                  | T_IntConstant
                  | T_STRINGCONSTANT
                  | function_call
                  | "(" expression ")"'''
        if len(p) == 4:  # Binary operation
            if p[1] == '(':
                p[0] = p[2]
            else:     
                node = Node("BinaryExpr", p[2], lineno=p.lineno(2))
                node.add_child(p[1])  # Left operand
                node.add_child(Node("Operator", p[2]))  # Right operand
                node.add_child(p[3])
                p[0] = node
        elif len(p) == 3:  # Unary operation (!)
            node = Node("UnaryExpr", p[1], lineno=p.lineno(1))
            node.add_child(Node("Operator", p[2]))
            node.add_child(p[2])  # Operand
            p[0] = node
        elif len(p) == 2:  # Single term
           p[0] = Node("Literal", p[1], lineno=p.lineno(1))
        elif len(p) == 4 and p[2] in ["<", ">", "<=", ">=", "==", "!="]:  # Comparison operation
            node = Node("RelationalExpr", p[2], lineno=p.lineno(2))
            node.add_child(p[1])  # Left operand
            node.add_child(p[3])
            p[0] = node
        else:  # Parenthesized expression
            p[0] = p[2]

    
    def p_function_declaration(self, p):
        '''function_declaration : type T_IDENTIFIER '(' parameter_list ')' '{' statement_list '}'
                                | type T_IDENTIFIER '(' ')' '{' statement_list '}'
                                | type T_IDENTIFIER '(' expression_list ')' '{' '}' '''
        node = Node("FnDecl")
        node.add_child(Node("Type", p[1]))
        node.add_child(Node("Identifier", p[2]))
        if len(p) > 8:
            node.add_child(Node("Parameters", p[4]))
        body = Node("Body")
        body.add_child(p[len(p) - 2])
        node.add_child(body)
        p[0] = node

    
    def p_type(self, p):
        '''type : T_Int
            | T_String
            | T_Void
            | T_BoolType
            | T_BoolConstant
            | T_Bool'''
        p[0] = Node("Type", p[1])

    def p_term(self, p):
        '''term : factor
                | term "*" factor
                | term "/" factor
                | term "+" factor
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
        else:
            p[0] = p[1]


    def p_factor(self, p):
        '''factor : T_IntConstant
                  | T_FloatConstant
                  | T_BoolConstant
                  | T_IDENTIFIER'''
        p[0] = Node("Literal", p[1])
        return p[0]

    def p_parameter(self, p):
        '''parameter : type T_IDENTIFIER'''
        node = Node("Parameter")
        node.add_child(Node("Type", p[1]))
        node.add_child(Node("Identifier", p[2]))
        p[0] = node   
        
          
    def p_parameter_list(self, p):
        '''parameter_list : type T_IDENTIFIER
                      | parameter_list ',' type T_IDENTIFIER
                      | parameter
                      | type T_IDENTIFIER ',' type T_IDENTIFIER
                      | parameter ',' parameter_list
                      | empty '''
        if len(p) == 3:  # type T_IDENTIFIER
            node = Node("Parameter")
            node.add_child(Node("Type", p[1]))
            node.add_child(Node("Identifier", p[2]))
            p[0] = node
        elif len(p) == 5:  # parameter_list ',' type T_IDENTIFIER
            p[1].add_child(Node("Type", p[3]))
            p[1].add_child(Node("Identifier", p[4]))
            p[0] = p[1]
        elif len(p) == 2:  # parameter
            p[0] = p[1]
        elif len(p) == 4:  # parameter ',' parameter_list
            p[1].add_child(p[3])
            p[0] = p[1]
        else:
            p[0] = None #empty



    def p_function_call(self, p):
        '''function_call : T_IDENTIFIER "(" expression_list ")"
                         | T_IDENTIFIER "(" ")"
                         | T_IDENTIFIER "(" parameter_list ")" '''
        node = Node("FunctionCall", p[1], p.lineno(1))
        if p[3] is not None:
            
            args_node = Node("(args)", None, p.lineno(2))
            args_node.add_child(p[3])
            node.add_child(args_node)
        p[0] = node

    def p_expression_list(self, p):
        '''expression_list : expression
                | expression "," expression_list
                | empty'''
        if len(p) == 2:
            node = Node("ExprList")
            node.add_child(p[1])
            p[0] = node
        elif len(p) == 4:
            node = Node("ExprList")
            node.add_child(p[1])
            node.add_child(p[3])
            p[0] = node
    

    def p_print(self, p):
        '''print : T_Print "(" expression ")" ";"
                 | T_Print "(" expression_list ")" ";" 
                 | T_Print "(" parameter_list ")" ";"'''
        node = Node("PrintStmt", lineno=p.lineno(1))
        if len(p) == 2:
            node.add_child(p[1])
        else:
            node.add_child(p[1])
            node.add_child(p[3])
        p[0] = node


    # def p_T_IDENTIFIER(self, p):
    #     '''x   : T_IDENTIFIER "(" ")" ";" 
    #              | T_IDENTIFIER "(" expression_list ")" ";"
    #              | T_IDENTIFIER "(" T_IDENTIFIER ")" ";"'''
    #     if len(p) == 6:
    #         p[0] = Node("Identifier", p[1])
    #         p[0].add_child(Node("OpenParen", [p[2]])) # "("  
    #         p[0].add_child(Node("expression_list", p[3])) # expression_list
    #         p[0].add_childNode("CloseParen", [p[4]]) # ")"
    #         p[0].add_child(Node("";"", p[5])) # ";"
    #       #  p[0] = f"{p[1]}({p[3]})"
    #     else:
    #         p[0] = Node("Identifier", p[1])
    #         p[0].add_child(Node("OpenParen", [p[2]])) # "("
    #         p[0].add_child(Node("CloseParen", [p[3]])) # ")"
    #         p[0].add_child(Node("";"", [p[4]])) # ";"
    #         #p[0] = f"{p[1]}()"

    def p_T_If(self, p):
        '''if : T_If "(" expression ")" statement
              | T_If "(" expression ")" "{" statement_list "}"'''        
        node = Node("IfStmt", lineno=p.lineno(1)) #T_If
       
        #test
        test = Node("(test)", None, p.lineno(3))
        test.add_child(p[3])
        node.add_child(test)

        #then
        then = Node("(then)", None, p.lineno(5))
        then.add_child(p[5]) #then
        node.add_child(then)

        #else (if present)
        if len(p) == 7:
            else_node = Node("(else)", None, p.lineno(6))
            else_node.add_child(p[7])
            node.add_child(else_node)

        p[0] = node  
        
    def p_if_else_statement(self, p):
        '''if_else_statement : T_If "(" expression ")" "{" statement_list "}" T_Else "{" statement_list "}"
                             | T_If "(" expression ")" statement T_Else statement'''
        node = Node("IfElse")
    
        # If-else with blocks
        if len(p) == 10:
            node.add_child(Node("Condition", p[3]))  # condition
            node.add_child(Node("IfBody", p[6]))     # then block
            node.add_child(Node("ElseBody", p[9]))   # else block

        # If-else with single statements
        elif len(p) == 6:
            node.add_child(Node("Condition", p[2]))  # condition
            node.add_child(Node("IfBody", p[3]))     # then block (single statement)
            node.add_child(Node("ElseBody", p[5]))   # else block (single statement)
    
        p[0] = node

    
    def p_T_Switch(self, p):
        '''switch : T_Switch "(" expression ")" "{" switch_body "}"'''
        node = Node("SwitchStatement")
        node.add_child(Node("Keyword", "switch"))
        node.add_child(Node("Condition", p[3]))
        node.add_child(p[6])
        p[0] = node

    def p_switch_body(self, p):
        '''switch_body : case_list
                       | case_list default_case'''
                    
        node = Node("SwitchBody")
        node.add_child(p[1])
        if len(p) == "3":
            node.add_child(p[2])
        p[0] = node

    def p_case_list(self, p):
        '''case_list : case
                     | case_list case'''
        if len(p) == 2:
            node = Node("CaseList")
            node.add_child(p[1])  
            p[0] = node
        else:
            p[1].add_child(p[2])
            p[0] = p[1]

    def p_case(self, p):
        '''case : T_CaseKeyword T_IntConstant ":" statement_list'''
        node = Node("Case")
        node.add_child(Node("Value", p[2])) #Case value
        node.add_child(p[4])
        p[0] = node
    def p_default_case(self, p):
        '''default_case : T_DefaultKeyword ":" statement_list'''
        node = Node("DefaultCase")
        node.add_child(p[3])
        p[0] = node
    def p_T_While(self, p):
        '''while : T_While "(" expression ")" "{" statement_list "}"'''
        node = Node("WhileStatement")
        node.add_child(Node("Keyword", "while"))
        node.add_child(Node("Condition", p[3]))

        body_node = Node("Body")
        body_node.add_child(p[6])
        node.add_child(body_node)
        p[0] = node
        # if len(p) == 8:
        #     p[0] = Node("WhileStatement", p[1])
        #     p[0].add_child(Node("OpenParen", [p[2]]))
        #     p[0].add_child(Node("expression", p[3]))
        #     p[0].add_child(Node("CloseParen", p[4]))
        #     p[0].add_child(Node("OpenBrace", p[5]))
        #     p[0].add_child(Node("statement_list", p[6]))
        #     p[0].add_child(Node("CloseBrace", p[7]))
        # return p[0]

    def p_for_loop(self, p):
        '''for_loop : T_For "(" assignment ";" expression ";" assignment ")" "{" statement_list "}"
                    | T_For "(" assignment ";" expression ";" assignment ")" statement'''

        node = Node("ForStmt", lineno=p.lineno(1))

        # Initialization
        init_node = Node("(init)", None, p.lineno(3))
        init_node.add_child(p[3])  # Assignment for initialization
        node.add_child(init_node)

        # Test condition
        test_node = Node("(test)", None, p.lineno(5))
        test_node.add_child(p[5])  # Relational expression
        node.add_child(test_node)

        # Step
        step_node = Node("(step)", None, p.lineno(7))
        step_node.add_child(p[7])  # Assignment for step
        node.add_child(step_node)

        # Body
        node.add_child(p[9])  # Body of the loop
        p[0] = node 
    def p_empty(self, p):
        'empty :'
        p[0] = None

    def p_return(self, p):
        '''return : T_Return expression ";" '''
        node = Node("ReturnStmt", lineno=p.lineno(1))
        node.add_child(p[2])
        p[0] = node

# ____________________________________________________________________________

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
            print(f"*** Syntax error at line {line}, column {col}: {p.value if hasattr(p, 'value') else 'Unexpected token'}")
            while True:
                        tok = self.parser.token()
                        if not tok or tok.type == ";":
                            break

            error_line = self.input.splitlines()[line - 1]

            # if (hasattr(p, 'value') and isinstance(p.value, str)):
            #     error_len = len(p.value)
            # else:
            #         error_len = 1
           
            # # if p.type == "T_ELSE":
            # #     print(f"*** Error line {line}")
            # #     print(f"{error_line}")
            # #     print(f" " * (col - 1) + "^" * error_len)
            # #     print(f"*** Syntax error")
            # #     return p #change this     
            # # elif p.type == 'T_IntConstant':
            # #         max = 3
            # #         invalid_seqeuence = self.input[col - 1:]
            # #         for char in invalid_seqeuence:
            # #             if char.isalnum or char in ['.', '_']:
            # #                 error_len += 1
            # #                 if error_len > max:
            # #                     error_len = max #so it wont spam 
            # #                     break
            # #             else:
            # #                 break
                    
            # print(f"*** Error line {line}")
            # print(f"{error_line}")
            # print(f" " * (col - 1) + "^" * error_len )
            # print(f"*** Syntax error")
        else:
             print("*** Syntax error at EOF")    
        
            
        self.parser.restart()

    def parse(self):
        self.lexer.build
        root = self.parser.parse(self.input, lexer=self.lexer.lexer)
        return root

class Node:
    def __init__(self, type, value=None, lineno=None):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.children = []

    def add_child(self, child):
        if isinstance(child, Node):
            self.children.append(child)
        elif isinstance(child, list):
            self.children.extend(child)
        elif (child, str):
            self.children.append(Node("Literal", child))

    def to_string(self, level=0):
        indent = "\t" * level
        line_info = f"{self.lineno}" if self.lineno else ""
        result = f"{line_info} {indent}{self.type}: {self.value if self.value else ''} \n"
        for child in self.children:
            result += child.to_string(level + 1)
        return result

    def __str__(self):
        return self.to_string()



def format_tree(node, level=0):
    if not node:
        return "None\n"
    
    result =  " " * (level * 4) + f"{node.type}: {node.value if node.value else ''}\n"
    for child in node.children:
        result += format_tree(child, level + 1)
    return result


def write_parser_output(root_node):
    with open("parser_output.out", "w") as f:
        f.write(format_tree(root_node))

def main():
    if len(sys.argv) < 2:
        print("Error: No input file provided!")
        sys.exit(1)

    with open(sys.argv[1], 'r') as file:
        file_content = file.read()

    parser = myParser(file_content)
    result = parser.parse()

    if result:
        print("Parse Tree:")
        print(result)
        write_parser_output(result)
    else:
        print("Parsing failed.")


if __name__ == '__main__':
    main()
