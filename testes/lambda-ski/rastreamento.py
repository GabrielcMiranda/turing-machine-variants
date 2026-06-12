"""Rastreamento de execucao — Combinadores SKI.

Reproduz, a partir da implementacao real (`ski.py` / `abstracao.py`), a tabela de
casos de teste, os tracos passo a passo (incluindo um traco de >= 7 passos) e os
exemplos de eliminacao de abstracao (lambda -> SKI).

Uso: python testes/lambda-ski/rastreamento.py
"""
import os
import sys

# Importa a implementacao real (sem duplicar logica).
IMPL = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",
                                    "implementacoes", "lambda-ski"))
sys.path.insert(0, IMPL)

from ski import parse_ski, reduce_ski, Var, Comb, App  # noqa: E402
from abstracao import bracket_abstraction              # noqa: E402

LIMITE_DIVERGENCIA = 100  # passos antes de declarar que o termo nao normaliza


def reduz(expr, max_steps=LIMITE_DIVERGENCIA):
    final, hist = reduce_ski(parse_ski(expr), max_steps)
    diverge = len(hist) >= max_steps
    return str(final), hist, diverge


# (expressao, forma normal esperada, classe)
CASOS = [
    ("S K K x",                      "x",        "identidade (I = S K K)"),
    ("K a b",                        "a",        "booleano TRUE = K (1o argumento)"),
    ("S K a b",                      "b",        "booleano FALSE = S K (2o argumento)"),
    ("S (S (K S) K) (S K K) f x",    "f (f x)",  "numeral de Church 2 (>= 7 passos)"),
    ("S I I (S I I)",                "(diverge)", "nao normaliza (Problema da Parada)"),
]

# Exemplos de eliminacao de abstracao: (nome, var, corpo como Term)
ABSTRACOES = [
    ("T[λx. x]",     "x", Var("x")),
    ("T[λx. y]",     "x", Var("y")),
    ("T[λx. (x y)]", "x", App(Var("x"), Var("y"))),
]


def secao(titulo):
    print("\n" + "=" * 70)
    print(titulo)
    print("=" * 70)


def tabela_casos():
    secao("(1) TABELA DE CASOS DE REDUCAO")
    print(f"{'termo':<32} {'esperado':<10} {'obtido':<10} passos  classe")
    print("-" * 92)
    ok = True
    for expr, esperado, classe in CASOS:
        obtido, hist, diverge = reduz(expr)
        if diverge:
            obtido_str = "(diverge)"
            passos = f">{LIMITE_DIVERGENCIA - 1}"
            bate = (esperado == "(diverge)")
        else:
            obtido_str = obtido
            passos = str(len(hist))
            bate = (obtido == esperado)
        ok = ok and bate
        marca = "" if bate else "  <-- DIVERGENCIA"
        print(f"{expr:<32} {esperado:<10} {obtido_str:<10} {passos:>5}   {classe}{marca}")
    print("\nTODOS OS CASOS BATEM" if ok else "\nHA DIVERGENCIAS")


def imprime_traco(expr, max_steps=LIMITE_DIVERGENCIA):
    final, hist = reduce_ski(parse_ski(expr), max_steps)
    print(f"Expressao inicial: {expr}")
    for i, (t, regra) in enumerate(hist, 1):
        print(f"  Passo {i:02d}: {t:<28} ====> [{regra}]")
    print(f"Forma normal: {final}   |   total: {len(hist)} passos")
    if len(hist) >= max_steps:
        print("  ** limite de passos atingido: termo nao normaliza (divergencia) **")


def traco_7_passos():
    secao("(2) TRACO PASSO A PASSO (>= 7 PASSOS) — NUMERAL DE CHURCH 2")
    print("2 = S (S (K S) K) (S K K) = S B I  (aplicar f duas vezes -> f (f x))\n")
    imprime_traco("S (S (K S) K) (S K K) f x")


def traco_divergente():
    secao("(3) TRACO DE TERMO QUE NAO NORMALIZA — OMEGA")
    print("Omega = S I I (S I I) se auto-replica; cortado pelo limite max_steps.\n")
    imprime_traco("S I I (S I I)", max_steps=6)


def abstracoes():
    secao("(4) ELIMINACAO DE ABSTRACAO (lambda -> SKI)")
    print("Cada conversao usa abstracao.py; o resultado e verificado por reducao.\n")
    for nome, var, corpo in ABSTRACOES:
        ski_term = bracket_abstraction(var, corpo)
        print(f"{nome}  =  {ski_term}")
        # Verificacao: aplicar o resultado a um argumento fresco 'a' deve
        # reproduzir o corpo com x := a.
        teste = App(ski_term, Var("a"))
        final, _ = reduce_ski(teste)
        corpo_sub = str(corpo).replace(var, "a")
        bate = "OK" if str(final) == corpo_sub else "DIVERGE"
        print(f"   verificacao: ({ski_term}) a  ->*  {final}   (esperado {corpo_sub}) [{bate}]\n")


if __name__ == "__main__":
    tabela_casos()
    traco_7_passos()
    traco_divergente()
    abstracoes()
