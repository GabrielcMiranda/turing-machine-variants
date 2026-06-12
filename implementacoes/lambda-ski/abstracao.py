# implementacoes/lambda-ski/abstracao.py
from ski import Term, Var, Comb, App

def ocorre_em(var_name: str, term: Term) -> bool:
    """Verifica se uma variável ocorre livre no termo."""
    if isinstance(term, Var):
        return term.name == var_name
    if isinstance(term, Comb):
        return False
    if isinstance(term, App):
        return ocorre_em(var_name, term.left) or ocorre_em(var_name, term.right)
    return False

def bracket_abstraction(var_name: str, term: Term) -> Term:
    """Aplica o algoritmo T[λx. E] para eliminação de abstração."""
    # Regra T[λx. x] = I
    if isinstance(term, Var) and term.name == var_name:
        return Comb('I')
    
    # Regra T[λx. E] = K E (se x não ocorre livre em E)
    if not ocorre_em(var_name, term):
        return App(Comb('K'), term)
    
    # Regra T[λx. (E F)] = S (T[λx. E]) (T[λx. F])
    if isinstance(term, App):
        left_abs = bracket_abstraction(var_name, term.left)
        right_abs = bracket_abstraction(var_name, term.right)
        return App(App(Comb('S'), left_abs), right_abs)
        
    raise ValueError("Termo inválido no processo de abstração.")