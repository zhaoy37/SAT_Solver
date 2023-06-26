"""
Author: Yiqi (Nick) Zhao
In this file, I build a calculator for the SMT solver.

Acknowledgement: Some parts of the codes
come from the PLY documentation: https://www.dabeaz.com/ply/ply.html#ply_nn4
I also referred to this table:
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
    "LITERAL",
    "NUM",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIV",
    "LPAREN",
    "RPAREN"
)

# Regex definitions for the tokens.
t_LITERAL = r'[a-wy-zA-WY-Z][a-zA-Z0-9]*'
t_NUM = r'[0-9]+'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIV = r'//'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Define t_error.
def t_error(t):
    raise Exception("Lexical error is detected when tokenizing in the calculator.")
    exit()
    t.lexer.skip(1)

# Define t_ignore.
t_ignore = ' \t'

# Build the lexer.
lexer = lex.lex()


def calculate(formula, assignment):
    """
    Build the parser.
    """

    # Check the type of the formula.
    if type(formula) == int:
        return formula

    # Set precendence:
    precedence = (
        ('left', 'MINUS'),
        ('left', 'PLUS'),
        ('left', 'DIV'),
        ('left', 'TIMES')
    )

    def p_formula_exp(p):
        'formula : exp'
        p[0] = p[1]

    def p_formula_negative(p):
        'formula : MINUS formula'
        p[0] = 0 - p[2]

    def p_formula_formula_times_formula(p):
        'formula : formula TIMES formula'
        p[0] = p[1] * p[3]

    def p_formula_formula_plus_formula(p):
        'formula : formula PLUS formula'
        p[0] = p[1] + p[3]

    def p_formula_formula_minus_formula(p):
        'formula : formula MINUS formula'
        p[0] = p[1] - p[3]

    def p_formula_formula_div_formula(p):
        'formula : formula DIV formula'
        p[0] = p[1] // p[3]

    def p_formula_paren_formula(p):
        'formula : LPAREN formula RPAREN'
        p[0] = p[2]

    def p_exp_num(p):
        'exp : NUM'
        p[0] = int(p[1])

    def p_exp_lit(p):
        'exp : LITERAL'
        p[0] = assignment[p[1]]

    def p_error(p):
        print("Syntactic error is detected when using the calculator.")
        exit()

    parser = yacc.yacc()
    lexer.input(formula)
    result = yacc.parse(lexer = lexer)
    return result