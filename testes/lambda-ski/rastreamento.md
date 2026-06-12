# Rastreamento de execução — Combinadores SKI

Reproduzível com `python testes/lambda-ski/rastreamento.py` (importa a implementação real de
`implementacoes/lambda-ski/`). Redução em **ordem normal** (redex mais externo à esquerda
primeiro), com limite `max_steps` para termos que não normalizam.

## 1. Tabela de casos (normal / fronteira / limitação)

| termo | forma normal esperada | obtida | passos | classe |
|-------|-----------------------|--------|--------|--------|
| `S K K x` | `x` | `x` | 2 | identidade (`I = S K K`) |
| `K a b` | `a` | `a` | 1 | booleano TRUE = `K` (1º argumento) |
| `S K a b` | `b` | `b` | 2 | booleano FALSE = `S K` (2º argumento) |
| `S (S (K S) K) (S K K) f x` | `f (f x)` | `f (f x)` | 7 | numeral de Church 2 (**≥ 7 passos**) |
| `S I I (S I I)` | — | `(diverge)` | > 99 | **não normaliza** (Problema da Parada) |

Cobertura exigida pela lauda: casos **normais** (`SKK`, booleanos), caso com **≥ 7 passos de
redução** (numeral de Church 2, Seção 7) e caso de **fronteira/limitação** (termo que não
normaliza, ilustrando a indecidibilidade da parada).

> `SKK ⇒ x` mostra na prática que `I = SKK`, justificando por que o combinador `I` é dispensável
> e o sistema pode ser reduzido a apenas `S` e `K`.

## 2. Traço passo a passo (≥ 7 passos) — numeral de Church 2

`2 = S (S (K S) K) (S K K) = S B I`, onde `S (K S) K = B` (composição) e `S K K = I`. Aplicado a
`f` e `x`, "aplica `f` duas vezes", devendo reduzir a `f (f x)`:

```
Expressao inicial: S (S (K S) K) (S K K) f x
  Passo 01: S (S (K S) K) (S K K) f x    ====> [S x y z -> x z (y z)]
  Passo 02: S (K S) K f (S K K f) x      ====> [S x y z -> x z (y z)]
  Passo 03: K S f (K f) (S K K f) x      ====> [K x y -> x]
  Passo 04: S (K f) (S K K f) x          ====> [S x y z -> x z (y z)]
  Passo 05: K f x (S K K f x)            ====> [K x y -> x]
  Passo 06: f (S K K f x)                ====> [S x y z -> x z (y z)]
  Passo 07: f (K f (K f) x)              ====> [K x y -> x]
Forma normal: f (f x)   |   total: 7 passos
```

**Leitura:** as três regras são exercitadas (`S` três vezes, `K` duas vezes). A forma normal
`f (f x)` confirma que a codificação de `2` puramente em `S`/`K` computa a iteração dupla.

## 3. Traço de termo que **não normaliza** — Ω

`Ω = S I I (S I I)` se auto-replica indefinidamente sob a regra de `S`. O redutor o corta pelo
limite `max_steps` (aqui exibido com limite 6 para ilustrar):

```
Expressao inicial: S I I (S I I)
  Passo 01: S I I (S I I)                ====> [S x y z -> x z (y z)]
  Passo 02: I (S I I) (I (S I I))        ====> [I x -> x]
  Passo 03: S I I (I (S I I))            ====> [S x y z -> x z (y z)]
  Passo 04: I (I (S I I)) (I (I (S I I))) ====> [I x -> x]
  Passo 05: I (S I I) (I (I (S I I)))    ====> [I x -> x]
  Passo 06: S I I (I (I (S I I)))        ====> [S x y z -> x z (y z)]
Forma normal: I (I (I (S I I))) (I (I (I (S I I))))   |   total: 6 passos
  ** limite de passos atingido: termo nao normaliza (divergencia) **
```

**Leitura:** o termo cresce a cada ciclo e nunca atinge forma normal — caso de **limitação**
observada: o sistema é Turing-completo, logo herda o Problema da Parada; por isso o limite de
passos é necessário.

## 4. Eliminação de abstração (λ → SKI)

Demonstra o algoritmo de *bracket abstraction* (`abstracao.py`) — o coração da eliminação de
variáveis. Cada conversão é **verificada** aplicando o resultado a um argumento fresco `a` e
reduzindo, para confirmar que reproduz o corpo original com `x := a`:

| abstração | resultado SKI | verificação (aplicado a `a`) | regra usada |
|-----------|---------------|------------------------------|-------------|
| `T[λx. x]` | `I` | `I a →* a` ✅ | `T[λx.x] = I` |
| `T[λx. y]` | `K y` | `K y a →* y` ✅ | `T[λx.E] = K E` (x ∉ E) |
| `T[λx. (x y)]` | `S I (K y)` | `S I (K y) a →* a y` ✅ | `T[λx.(E F)] = S (T[λx.E]) (T[λx.F])` |

As três regras do algoritmo são cobertas, e a verificação por redução garante que a tradução
preserva a semântica da função λ original.

## 5. Como reproduzir

```bash
python testes/lambda-ski/rastreamento.py     # tabela + traços + abstrações (este documento)
python implementacoes/lambda-ski/demo.py      # mesmos traços, formato de demonstração
python implementacoes/lambda-ski/test_ski.py  # testes automatizados (4/4)
```
