"""Simulador de MTND para validar a tabela de transicao de compostos.jff.
Explora a arvore de computacao (BFS) e aceita se ALGUM ramo para em qa.
Uso: python _verifica.py
"""
from collections import deque

BLANK = "_"  # representa o branco

# delta: (estado, lido) -> lista de (escreve, move, proximo)
delta = {}
def add(s, r, w, m, t):
    delta.setdefault((s, r), []).append((w, m, t))

# Fase 1
add("q0", "1", "A", "R", "q1")
add("q1", "1", "A", "R", "q2")
add("q2", "1", "A", "R", "q2")   # nao det. continua
add("q2", "1", "1", "L", "q3")   # nao det. para
# Rebobinar
add("q3", "A", "A", "L", "q3")
add("q3", BLANK, BLANK, "R", "q4")
# Fase 2
add("q4", "A", "C", "R", "q5")
add("q5", "A", "A", "R", "q5")
add("q5", "B", "B", "R", "q5")
add("q5", "1", "B", "L", "q6")
add("q6", "B", "B", "L", "q6")
add("q6", "A", "A", "L", "q6")
add("q6", "C", "D", "R", "q7")
add("q7", "A", "C", "R", "q5")
add("q7", "B", "B", "L", "q8")
# Fim do passe
add("q8", "D", "D", "L", "q8")
add("q8", BLANK, BLANK, "R", "q9")
add("q9", "D", "A", "R", "q9")
add("q9", "B", "B", "R", "q9")
add("q9", "1", "1", "L", "q10")
add("q9", BLANK, BLANK, "S", "qa")
add("q10", "B", "B", "L", "q10")
add("q10", "A", "A", "L", "q10")
add("q10", BLANK, BLANK, "R", "q4")

ACCEPT = "qa"
MAX_STEPS = 200000  # corte de seguranca

def read(tape, pos):
    return tape.get(pos, BLANK)

def aceita(n):
    # configuracao: (estado, pos, tape-frozenset)  -> usamos dict copiado
    tape0 = {i: "1" for i in range(n)}
    start = ("q0", 0, frozenset(tape0.items()))
    fila = deque([start])
    vistos = set([start])
    steps = 0
    while fila:
        steps += 1
        if steps > MAX_STEPS:
            return False, "estouro"
        estado, pos, tfs = fila.popleft()
        if estado == ACCEPT:
            return True, "ramo aceitante"
        tape = dict(tfs)
        sym = read(tape, pos)
        for (w, m, t) in delta.get((estado, sym), []):
            nt = dict(tape)
            if w == BLANK:
                nt.pop(pos, None)
            else:
                nt[pos] = w
            npos = pos + (1 if m == "R" else -1 if m == "L" else 0)
            conf = (t, npos, frozenset(nt.items()))
            if conf not in vistos:
                vistos.add(conf)
                fila.append(conf)
    return False, "todos os ramos pararam sem aceitar"

if __name__ == "__main__":
    casos = {
        0: False, 1: False, 2: False, 3: False, 4: True, 5: False,
        6: True, 7: False, 8: True, 9: True, 10: True, 11: False,
        12: True, 13: False, 15: True, 25: True, 17: False, 49: True,
    }
    ok = True
    for n in sorted(casos):
        esperado = casos[n]
        obtido, motivo = aceita(n)
        marca = "OK " if obtido == esperado else "ERRO"
        if obtido != esperado:
            ok = False
        print(f"{marca} n={n:>2}  esperado={'aceita' if esperado else 'rejeita':7} "
              f"obtido={'aceita' if obtido else 'rejeita':7} ({motivo})")
    print("\nTODOS OS CASOS PASSARAM" if ok else "\nHA DIVERGENCIAS")
