---
marp: true
title: λ-Cálculo → Combinadores SKI
paginate: true
---

<!--
Slides da Pessoa 2 (parte do SKI no seminário conjunto).
Renderizar com Marp (VS Code: extensão "Marp for VS Code" -> Export to PPTX/PDF),
ou copiar o conteúdo para o Google Slides. ~4-5 min desta parte.
-->

# λ-Cálculo → Combinadores **SKI**

## Computar **sem variáveis**

Toda função do λ-cálculo pode ser expressa só com `S` e `K`

Teoria da Computabilidade — AV2
Implementação em **Python** (`implementacoes/lambda-ski/`)

---

# O problema — variáveis são caras

No λ-cálculo, computar é fazer **β-redução**:

$$(\lambda x.\,E)\,M \;\to\; E[x := M]$$

Implementar isso exige gerenciar **escopo de variáveis**:

- distinguir variáveis **livres** de **ligadas**;
- evitar **captura de nomes** (uma variável livre em `M` ser presa por um `λ` interno);
- portanto implementar **α-conversão** (renomear variáveis).

> Muita "burocracia de nomes" antes de computar qualquer coisa.

---

# A solução — Lógica Combinatória (Schönfinkel, Curry)

Variáveis e ligadores (`λ`) são **dispensáveis**. Tudo se faz com 3 combinadores e
**aplicação**:

| Combinador | Regra | Papel |
|------------|-------|-------|
| `I` | `I x → x` | identidade |
| `K` | `K x y → x` | constante (guarda o 1º, descarta o 2º) |
| `S` | `S x y z → x z (y z)` | distribuidor (duplica e distribui o argumento) |

Sistema **Turing-completo**, equivalente ao λ-cálculo — mas **sem nomes**.

---

# O `I` é dispensável: `I = S K K`

Basta `S` e `K`. Verificação por redução:

```
S K K x   ====> [S x y z -> x z (y z)]
K x (K x) ====> [K x y -> x]
x
```

`S K K x →* x` — comporta-se **exatamente** como a identidade.

> Logo o núcleo do sistema pode ser apenas **`S` e `K`** (2 constantes).

---

# Eliminação de abstração (*bracket abstraction*)

Algoritmo `T[λx.E]` que **traduz** um λ-termo para SKI puro:

- `T[λx. x]        = I`
- `T[λx. E]        = K E`                  (se `x` **não** ocorre em `E`)
- `T[λx. (E F)]    = S (T[λx.E]) (T[λx.F])`

Exemplos (verificados em `abstracao.py`):

| `T[λx. x]` | `T[λx. y]` | `T[λx. (x y)]` |
|---|---|---|
| `I` | `K y` | `S I (K y)` |

A complexidade de nomes some **em tempo de tradução**.

---

# Estratégia de redução: **ordem normal**

- Reduz sempre o redex **mais externo à esquerda** primeiro.
- **Teorema de Church-Rosser / padronização:** se o termo tem forma normal,
  a ordem normal **garante** encontrá-la.
- Contraste com ordem aplicativa (*eager*): pode entrar em loop num argumento que
  o `K` ia **descartar**.

> No código: `step_reduction` (um passo + regra) e `reduce_ski` (até a forma normal ou `max_steps`).

---

# Demonstração — traço de **7 passos**

Numeral de Church **2** = `S (S (K S) K) (S K K) = S B I` → "aplicar `f` duas vezes":

```
S (S (K S) K) (S K K) f x   ==> [S]
S (K S) K f (S K K f) x     ==> [S]
K S f (K f) (S K K f) x     ==> [K]
S (K f) (S K K f) x         ==> [S]
K f x (S K K f x)           ==> [K]
f (S K K f x)               ==> [S]
f (K f (K f) x)             ==> [K]
=> f (f x)
```

Reproduzível: `python implementacoes/lambda-ski/demo.py`

---

# Análise técnica

- **O que computa:** reescrita pura de termos por casamento de padrão — sem ambiente
  de nomes, sem tabela de símbolos.
- **Por que não é trivial:** é Turing-completo; a substituição "desaparece" dentro das
  regras de `S` e `K`.
- **Limitação observada:** herda o **Problema da Parada**. `Ω = S I I (S I I)` se
  auto-replica e **não normaliza** → daí o limite `max_steps`.
- **Relação com computabilidade:** SKI ≡ λ-cálculo ≡ Máquina de Turing (Church-Turing).

---

# Resumo

- 3 combinadores (`S`, `K`, `I`) — e `I = S K K`, então bastam **`S` e `K`**.
- *Bracket abstraction* elimina variáveis: λ-termo → SKI puro.
- Redução em **ordem normal** (Church-Rosser).
- Turing-completo **sem nomes**; ilustra o Problema da Parada (`Ω`).
- Evidências: `ski.py`, `abstracao.py`, `demo.py`, `test_ski.py` (4/4), rastreamento.

**Obrigado!**
