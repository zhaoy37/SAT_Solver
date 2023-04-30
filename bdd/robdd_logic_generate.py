"""
Authors: Ziyan An
References: 

Implementations for generating random logics for robdd.
"""

import random 



def generate_productions(n: int = 1):
    productions = {
        "Expr": ["AndExpr", "OrExpr", "NotVar", "Var"],
        "AndExpr": ["(Expr and Expr)"],
        "OrExpr": ["(Expr or Expr)"],
        "Var": [f"x{i}" for i in range(n)],
        "NotVar": [f"(not x{i})" for i in range(n)]
    }
    return productions


def generate_formula(symbol, n: int = 1):
    if symbol not in generate_productions(n):
        return symbol
    production = random.choice(generate_productions(n)[symbol])
    while production in ["NotVar", "Var"]:  ## unary expressions not allowed
        production = random.choice(generate_productions(n)[symbol])
    tokens = production.split()
    return " ".join([generate_formula(t, n) for t in tokens])


def random_logic_gen(n: int = 1, components: int = 3):
    if components == 1:
        formula = generate_formula("Expr", n)
        tokens = formula.split() 
        for idx,t in enumerate(tokens):
            if 'Expr' in t:
                choice = random.choices(["NotVar", "Var"], weights = [0.2, 0.8], k=1)[0]
                sub_formula = random.choice(generate_productions(n)[choice])
                tokens[idx] = t.replace('Expr', sub_formula)
        return " ".join([t for t in tokens])
    
    else:
        formula = generate_formula("Expr", n)
        tokens = formula.split()
        for idx,t in enumerate(tokens):
            if 'Expr' in t:
                sub_formula = random_logic_gen(n, components-1)
                tokens[idx] = t.replace('Expr', sub_formula)
        return " ".join([t for t in tokens])



# print(random_logic_gen(n=3, components=2))