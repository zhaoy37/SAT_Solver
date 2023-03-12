"""
Author: Yiqi (Nick) Zhao

The purpose of this file is to create the parser
for user input. following the BNF listed below.

BNF for user input parsing:

<formula> := literal | <formula> and <formula>
            | <formula> or <formula> | not <formula> |
            (<formula>)

The output of the program should be some abstract syntax tree (AST) for the logic.

Acknowledgement: Some parts of the codes
come from the PLY documentation: https://www.dabeaz.com/ply/ply.html#ply_nn4

I also refered to this table:
https://tool.oschina.net/uploads/apidocs/jquery/regexp.html
and this tool:
https://regex101.com/

I also used some class materials from CS 3276 Provided
by professor Kevin Leach: Please see https://www.youtube.com/watch?v=xfjCWRmDj3Q&t=1176s

This work may partially overlap with my work in CS 8395, another class at Vanderbilt.
"""
import ply.lex as lex
import ply.yacc as yacc

"""
Build the lexer.
"""
# List of token names:
tokens = (
    "AND",
    "OR",
    "NOT",
    "LPAREN",
    "RPAREN",
    "LITERAL",
    "TRUE",
    "FALSE"
)

# Regex definitions for the tokens.
t_AND = r'and'
t_OR = r'or'
t_NOT = r'not'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LITERAL = r'x[0-9]+'
t_TRUE = r'True'
t_FALSE = r'False'

# Define t_error.
def t_error(t):
    print("Lexical error is detected when tokenizing the logic.")
    exit()
    t.lexer.skip(1)

# Define t_ignore.
t_ignore = ' \t'

# Build the lexer.
lexer = lex.lex()

"""
Build the parser.
"""

# Set precendence:
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT')
)

def p_formula_literal(p):
    'formula : LITERAL'
    p[0] = p[1]

def p_formula_and(p):
    'formula : formula AND formula'
    p[0] = ["and", p[1], p[3]]

def p_formula_or(p):
    'formula : formula OR formula'
    p[0] = ["or", p[1], p[3]]

def p_formula_not(p):
    'formula : NOT formula'
    p[0] = ["not", p[2]]

def p_formula_formula_par(p):
    'formula : LPAREN formula RPAREN'
    p[0] = p[2]

def p_formula_true(p):
    'formula : TRUE'
    p[0] = p[1]

def p_formula_false(p):
    'formula : FALSE'
    p[0] = p[1]

def p_error(p):
    print("Syntactic error is detected when parsing the logic.")
    exit()

def parse_logic(logic):
    parser = yacc.yacc()
    lexer.input(logic)
    ast = yacc.parse(lexer = lexer)
    return ast