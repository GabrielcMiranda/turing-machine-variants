# implementacoes/lambda-ski/ski.py

class Term:
    def __str__(self):
        raise NotImplementedError

class Var(Term):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def __eq__(self, other):
        return isinstance(other, Var) and self.name == other.name

class Comb(Term):
    def __init__(self, kind):
        self.kind = kind  # 'S', 'K', ou 'I'
    def __str__(self):
        return self.kind
    def __eq__(self, other):
        return isinstance(other, Comb) and self.kind == other.kind

class App(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        # Simplifica a visualização omitindo parênteses desnecessários à esquerda
        l_str = str(self.left)
        r_str = f"({self.right})" if isinstance(self.right, App) else str(self.right)
        if isinstance(self.left, App):
            return f"{l_str} {r_str}"
        return f"({l_str} {r_str})"
    def __eq__(self, other):
        return isinstance(other, App) and self.left == other.left and self.right == other.right

def parse_ski(s: str) -> Term:
    """Parser simples de strings para Termos SKI com associatividade à esquerda e parênteses."""
    tokens = s.replace('(', ' ( ').replace(')', ' ) ').split()
    
    def parse_expr(index):
        nodes = []
        while index < len(tokens):
            token = tokens[index]
            if token == '(':
                sub_term, index = parse_expr(index + 1)
                nodes.append(sub_term)
            elif token == ')':
                return build_left_assoc(nodes), index + 1
            elif token in ('S', 'K', 'I'):
                nodes.append(Comb(token))
                index += 1
            else:
                nodes.append(Var(token))
                index += 1
        return build_left_assoc(nodes), index

    def build_left_assoc(nodes):
        if not nodes:
            raise ValueError("Expressão vazia ou inválida.")
        acc = nodes[0]
        for node in nodes[1:]:
            acc = App(acc, node)
        return acc

    term, _ = parse_expr(0)
    return term

def step_reduction(term: Term):
    """Executa UM passo de redução em ordem normal (mais externa à esquerda).
    Retorna uma tupla (novo_termo, reduziu, regra_aplicada)."""
    
    # 1. Caso Base: Átomos não reduzem isoladamente
    if isinstance(term, (Var, Comb)):
        return term, False, ""

    # 2. Se for uma Aplicação, tenta reduzir a estrutura como um todo (regras principais)
    if isinstance(term, App):
        # Padrão I x -> x
        if isinstance(term.left, Comb) and term.left.kind == 'I':
            return term.right, True, "I x -> x"
        
        # Padrão K x y -> x
        if isinstance(term.left, App) and isinstance(term.left.left, Comb) and term.left.left.kind == 'K':
            x = term.left.right
            return x, True, "K x y -> x"
            
        # Padrão S x y z -> x z (y z)
        if isinstance(term.left, App) and isinstance(term.left.left, App) and isinstance(term.left.left.left, Comb) and term.left.left.left.kind == 'S':
            x = term.left.left.right
            y = term.left.right
            z = term.right
            return App(App(x, z), App(y, z)), True, "S x y z -> x z (y z)"

    # 3. Se nenhuma regra principal se aplica no topo, busca na subárvore Esquerda (Ordem Normal)
    new_left, reduced, rule = step_reduction(term.left)
    if reduced:
        return App(new_left, term.right), True, rule

    # 4. Por fim, busca na subárvore Direita
    new_right, reduced, rule = step_reduction(term.right)
    if reduced:
        return App(term.left, new_right), True, rule

    return term, False, ""

def reduce_ski(term: Term, max_steps=100):
    """Reduz o termo até a forma normal ou até atingir o limite max_steps."""
    steps = []
    current = term
    for _ in range(max_steps):
        next_term, reduced, rule = step_reduction(current)
        if not reduced:
            break
        steps.append((str(current), rule))
        current = next_term
    return current, steps