"""
Author: Yiqi (Nick) Zhao
The purpose of this file is to create the parser
for user input (SMT).

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
    "ATOM",
    "LT",
    "GT",
    "LE",
    "GE",
    "EQ",
    "NQ",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIV",
    "NUM"
)

# Regex definitions for the tokens.
t_AND = r'and'
t_OR = r'or'
t_NOT = r'not'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ATOM = r'y[0-9]+'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'='
t_NQ = r'!='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIV = r'//'
t_NUM = r'[0-9]+'



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

smt_atoms = set()


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

def p_formula_expression_1(p):
    'formula : expression LT expression'
    p[0] = ["lt", p[1], p[3]]

def p_formula_expression_2(p):
    'formula : expression GT expression'
    p[0] = ["gt", p[1], p[3]]

def p_formula_expression_3(p):
    'formula : expression LE expression'
    p[0] = ["le", p[1], p[3]]

def p_formula_expression_4(p):
    'formula : expression GE expression'
    p[0] = ["ge", p[1], p[3]]

def p_formula_expression_5(p):
    'formula : expression EQ expression'
    p[0] = ["eq", p[1], p[3]]

def p_formula_expression_6(p):
    'formula : expression NQ expression'
    p[0] = ["nq", p[1], p[3]]

def p_subexpression_atom(p):
    'subexpression : ATOM'
    smt_atoms.add(p[1])
    p[0] = p[1]

def p_subexpression_num(p):
    'subexpression : NUM'
    p[0] = p[1]

def p_expression_subexpression(p):
    'expression : subexpression'
    p[0] = p[1]

def p_expression_plus(p):
    'expression : subexpression PLUS subexpression'
    p[0] = p[1] + " + " + p[3]

def p_expression_minus(p):
    'expression : subexpression MINUS subexpression'
    p[0] = p[1] + " - " + p[3]

def p_expression_times(p):
    'expression : subexpression TIMES subexpression'
    p[0] = p[1] + " * " + p[3]

def p_expression_divides(p):
    'expression : subexpression DIV subexpression'
    p[0] = p[1] + " // " + p[3]


def p_error(p):
    print("Syntactic error is detected when parsing the logic.")
    exit()


def construct_formatted_smt(ast, sat_encoding, boundary, sat_smt_table):
    if ast[0] not in ["and", "or", "not"]:
        ast_str = ast[1] + " " + ast[0] + " " + ast[2]
        if ast_str not in sat_smt_table:
            sat_atom = "x" + str(boundary[0])
            sat_encoding[sat_atom] = ast
            sat_smt_table[ast_str] = sat_atom
            boundary[0] += 1
        return sat_smt_table[ast_str]
    else:
        if ast[0] in ["and", "or"]:
            return [ast[0], construct_formatted_smt(ast[1], sat_encoding, boundary, sat_smt_table), construct_formatted_smt(ast[2], sat_encoding, boundary, sat_smt_table)]
        else:
            return [ast[0], construct_formatted_smt(ast[1], sat_encoding, boundary, sat_smt_table)]


def parse_smt(logic):
    parser = yacc.yacc()
    lexer.input(logic)
    ast = yacc.parse(lexer = lexer)
    boundary = [0]
    sat_encoding = dict()
    sat_smt_table = dict()
    return construct_formatted_smt(ast, sat_encoding, boundary, sat_smt_table), sat_encoding, list(smt_atoms)


if __name__ == "__main__":
    print(parse_smt("(y1 > y1) and (y1 // y1 <= 3) and not (y1 > y1) or (y1 // y1 <= 3) or y1 < 1"))
