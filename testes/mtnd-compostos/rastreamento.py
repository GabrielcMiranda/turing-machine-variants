"""Rastreamento reprodutivel da MTND de compostos (mesma delta de compostos.jff).
Gera: (1) tabela de resultados, (2) arvore de ramos do 1^6, (3) traco passo a passo.
Uso: python rastreamento.py
"""
from collections import deque

BLANK = "_"

delta = {}
def add(s, r, w, m, t):
    delta.setdefault((s, r), []).append((w, m, t))

# Fase 1 (unico ponto nao deterministico: q2 lendo 1)
add("q0", "1", "A", "R", "q1")
add("q1", "1", "A", "R", "q2")
add("q2", "1", "A", "R", "q2")   # continua marcando
add("q2", "1", "1", "L", "q3")   # para
# Rebobinar
add("q3", "A", "A", "L", "q3"); add("q3", BLANK, BLANK, "R", "q4")
# Fase 2
add("q4", "A", "C", "R", "q5")
add("q5", "A", "A", "R", "q5"); add("q5", "B", "B", "R", "q5"); add("q5", "1", "B", "L", "q6")
add("q6", "B", "B", "L", "q6"); add("q6", "A", "A", "L", "q6"); add("q6", "C", "D", "R", "q7")
add("q7", "A", "C", "R", "q5"); add("q7", "B", "B", "L", "q8")
add("q8", "D", "D", "L", "q8"); add("q8", BLANK, BLANK, "R", "q9")
add("q9", "D", "A", "R", "q9"); add("q9", "B", "B", "R", "q9")
add("q9", "1", "1", "L", "q10"); add("q9", BLANK, BLANK, "S", "qa")
add("q10", "B", "B", "L", "q10"); add("q10", "A", "A", "L", "q10"); add("q10", BLANK, BLANK, "R", "q4")

ACCEPT = "qa"
MAX = 500000

def rd(t, p): return t.get(p, BLANK)

# ---------- (1) aceitacao por BFS (qualquer ramo) ----------
def aceita(n):
    t0 = frozenset({i: "1" for i in range(n)}.items())
    start = ("q0", 0, t0)
    fila = deque([start]); vistos = {start}; steps = 0
    while fila:
        steps += 1
        if steps > MAX: return None
        est, pos, tfs = fila.popleft()
        if est == ACCEPT: return True
        t = dict(tfs); sym = rd(t, pos)
        for (w, m, nx) in delta.get((est, sym), []):
            nt = dict(t)
            if w == BLANK: nt.pop(pos, None)
            else: nt[pos] = w
            np = pos + (1 if m == "R" else -1 if m == "L" else 0)
            c = (nx, np, frozenset(nt.items()))
            if c not in vistos: vistos.add(c); fila.append(c)
    return False

# ---------- run determinístico fixando o palpite a (escolha em q2) ----------
def render(t, pos, lo, hi):
    cels = []
    for i in range(lo, hi + 1):
        s = t.get(i, BLANK)
        cels.append(f"[{s}]" if i == pos else f" {s} ")
    return "".join(cels)

def run_fixando_a(n, a, trace=False):
    """Roda deterministicamente escolhendo, em q2, parar quando ja houver 'a' marcas A."""
    t = {i: "1" for i in range(n)}; pos = 0; est = "q0"; steps = 0
    passos = []
    while True:
        sym = rd(t, pos)
        if est == "q2" and sym == "1":
            mov = ("A", "R", "q2") if pos < a else ("1", "L", "q3")
        else:
            opts = delta.get((est, sym), [])
            if not opts:
                if trace: passos.append((steps, est, render(t, pos, min(t, default=0)-1, max(t, default=0)+1), "PARA (rejeita)"))
                return ("aceita" if est == ACCEPT else "rejeita"), passos
            mov = opts[0]
        if trace:
            lo = min(min(t, default=0), pos) - 1; hi = max(max(t, default=0), pos) + 1
            passos.append((steps, est, render(t, pos, lo, hi), f"le {sym} -> escreve {mov[0]}, {mov[1]}"))
        if est == ACCEPT:
            return "aceita", passos
        w, m, nx = mov
        if w == BLANK: t.pop(pos, None)
        else: t[pos] = w
        pos += (1 if m == "R" else -1 if m == "L" else 0)
        est = nx; steps += 1
        if est == ACCEPT:
            if trace:
                lo = min(min(t, default=0), pos) - 1; hi = max(max(t, default=0), pos) + 1
                passos.append((steps, est, render(t, pos, lo, hi), "ACEITA"))
            return "aceita", passos
        if steps > MAX: return "estouro", passos

if __name__ == "__main__":
    print("=" * 70)
    print("(1) TABELA DE RESULTADOS")
    print("=" * 70)
    casos = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 15, 25, 49]
    esperado = lambda n: any(n % a == 0 and n // a >= 2 for a in range(2, n))
    print(f"{'n':>3} | {'1^n':<12} | {'esperado':<8} | {'obtido':<8} | classe")
    print("-" * 60)
    for n in casos:
        esp = "aceita" if esperado(n) else "rejeita"
        obt = "aceita" if aceita(n) else "rejeita"
        cls = "composto" if esperado(n) else ("primo" if n >= 2 else "fronteira")
        flag = "" if esp == obt else "  <<< DIVERGE"
        print(f"{n:>3} | {'1'*n if n else '(vazio)':<12} | {esp:<8} | {obt:<8} | {cls}{flag}")

    print()
    print("=" * 70)
    print("(2) ARVORE DE RAMOS PARA 1^6  (nao determinismo em q2 = palpite de a)")
    print("=" * 70)
    print("raiz: q0 sobre 1^6")
    for a in range(2, 7):
        res, _ = run_fixando_a(6, a)
        b = 6 // a if a != 0 and 6 % a == 0 else None
        nota = f"6 = {a} x {b}" if (b and 6 % a == 0 and b >= 2) else f"{a} nao divide 6 com b>=2"
        marca = "ACEITA" if res == "aceita" else "rejeita"
        print(f"  +-- palpite a={a}: {marca:8} ({nota})")
    print("  => existe ramo aceitante (a=2 e a=3) -> 1^6 ACEITA")

    print()
    print("=" * 70)
    print("(3) TRACO PASSO A PASSO - RAMO ACEITANTE 1^6 com a=3")
    print("=" * 70)
    _, passos = run_fixando_a(6, 3, trace=True)
    for (s, est, fita, obs) in passos:
        print(f"{s:>3} | {est:<4} | {fita:<30} | {obs}")

    print()
    print("=" * 70)
    print("(4) TRACO DE RAMO QUE REJEITA - 1^6 com a=4 (4 nao divide 6)")
    print("=" * 70)
    _, passos = run_fixando_a(6, 4, trace=True)
    for (s, est, fita, obs) in passos:
        print(f"{s:>3} | {est:<4} | {fita:<30} | {obs}")
