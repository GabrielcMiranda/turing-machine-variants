# Rastreamento de execução — MTND compostos em unário

Reproduzível com `python testes/mtnd-compostos/rastreamento.py` (mesma δ de `compostos.jff`).
Convenção da fita: `[x]` marca a posição da cabeça; `_` é o branco (`⊔`).

## 1. Tabela de resultados (aceitos / rejeitados / fronteira)

| n | entrada `1ⁿ` | esperado | obtido | classe |
|---|--------------|----------|--------|--------|
| 0 | (vazio) | rejeita | rejeita | fronteira |
| 1 | `1` | rejeita | rejeita | fronteira |
| 2 | `11` | rejeita | rejeita | primo |
| 3 | `111` | rejeita | rejeita | primo |
| 4 | `1111` | **aceita** | **aceita** | composto (2×2) |
| 5 | `11111` | rejeita | rejeita | primo |
| 6 | `111111` | **aceita** | **aceita** | composto (2×3) |
| 7 | `1111111` | rejeita | rejeita | primo |
| 8 | `11111111` | **aceita** | **aceita** | composto (2×4) |
| 9 | `111111111` | **aceita** | **aceita** | composto (3×3) |
| 11 | `1¹¹` | rejeita | rejeita | primo |
| 12 | `1¹²` | **aceita** | **aceita** | composto (vários) |
| 15 | `1¹⁵` | **aceita** | **aceita** | composto (3×5) |
| 25 | `1²⁵` | **aceita** | **aceita** | composto (5×5) |
| 49 | `1⁴⁹` | **aceita** | **aceita** | composto (7×7) |

Cobertura exigida pela lauda: **aceitos** (4, 6, 8, 9, 12, 15, 25, 49),
**rejeitados** (primos 2, 3, 5, 7, 11) e **fronteira** (`n=0` vazio, `n=1`).
Inclui quadrados perfeitos (25, 49) — caso em que o único par de fatores é `a=b`.

## 2. Árvore de computação para `1⁶` (não determinismo = palpite de `a`)

O único ponto não determinístico é `q₂` lendo `1`. Para `1⁶`, os ramos correspondem aos
palpites `a ∈ {2,3,4,5,6}`. A Fase 2 verifica cada um deterministicamente:

```
raiz: q0 sobre 1^6
  ├── palpite a=2: ACEITA   (6 = 2 × 3)
  ├── palpite a=3: ACEITA   (6 = 3 × 2)
  ├── palpite a=4: rejeita  (4 não divide 6 com b≥2)
  ├── palpite a=5: rejeita  (5 não divide 6 com b≥2)
  └── palpite a=6: rejeita  (b = 1, não há 2º bloco)
  ⇒ existe ramo aceitante (a=2 e a=3) → 1^6 ACEITA
```

> Critério de aceitação: **basta um ramo** alcançar `qₐ`. Aqui dois ramos aceitam.
> No JFLAP, demonstrar com *Step Run* / árvore para `n` pequeno (4, 6, 9).

## 3. Traço passo a passo — ramo **aceitante** `1⁶`, `a=3` (41 passos)

```
  0 | q0   |  _ [1] 1  1  1  1  1  _        | lê 1 -> escreve A, R
  1 | q1   |  _  A [1] 1  1  1  1  _        | lê 1 -> escreve A, R
  2 | q2   |  _  A  A [1] 1  1  1  _        | lê 1 -> escreve A, R   (continua: a=3)
  3 | q2   |  _  A  A  A [1] 1  1  _        | lê 1 -> escreve 1, L   (PARA de marcar)
  4 | q3   |  _  A  A [A] 1  1  1  _        | lê A -> escreve A, L
  5 | q3   |  _  A [A] A  1  1  1  _        | lê A -> escreve A, L
  6 | q3   |  _ [A] A  A  1  1  1  _        | lê A -> escreve A, L
  7 | q3   |  _ [_] A  A  A  1  1  1  _     | lê _ -> escreve _, R
  8 | q4   |  _ [A] A  A  1  1  1  _        | lê A -> escreve C, R   (gabarito corrente)
  9 | q5   |  _  C [A] A  1  1  1  _        | lê A -> escreve A, R
 10 | q5   |  _  C  A [A] 1  1  1  _        | lê A -> escreve A, R
 11 | q5   |  _  C  A  A [1] 1  1  _        | lê 1 -> escreve B, L   (consome 1º 1)
 12 | q6   |  _  C  A [A] B  1  1  _        | lê A -> escreve A, L
 13 | q6   |  _  C [A] A  B  1  1  _        | lê A -> escreve A, L
 14 | q6   |  _ [C] A  A  B  1  1  _        | lê C -> escreve D, R
 15 | q7   |  _  D [A] A  B  1  1  _        | lê A -> escreve C, R
 16 | q5   |  _  D  C [A] B  1  1  _        | lê A -> escreve A, R
 17 | q5   |  _  D  C  A [B] 1  1  _        | lê B -> escreve B, R
 18 | q5   |  _  D  C  A  B [1] 1  _        | lê 1 -> escreve B, L   (consome 2º 1)
 19 | q6   |  _  D  C  A [B] B  1  _        | lê B -> escreve B, L
 20 | q6   |  _  D  C [A] B  B  1  _        | lê A -> escreve A, L
 21 | q6   |  _  D [C] A  B  B  1  _        | lê C -> escreve D, R
 22 | q7   |  _  D  D [A] B  B  1  _        | lê A -> escreve C, R
 23 | q5   |  _  D  D  C [B] B  1  _        | lê B -> escreve B, R
 24 | q5   |  _  D  D  C  B [B] 1  _        | lê B -> escreve B, R
 25 | q5   |  _  D  D  C  B  B [1] _        | lê 1 -> escreve B, L   (consome 3º 1: bloco completo)
 26 | q6   |  _  D  D  C  B [B] B  _        | lê B -> escreve B, L
 27 | q6   |  _  D  D  C [B] B  B  _        | lê B -> escreve B, L
 28 | q6   |  _  D  D [C] B  B  B  _        | lê C -> escreve D, R
 29 | q7   |  _  D  D  D [B] B  B  _        | lê B -> escreve B, L   (gabarito esgotado: fim do passe)
 30 | q8   |  _  D  D [D] B  B  B  _        | lê D -> escreve D, L
 31 | q8   |  _  D [D] D  B  B  B  _        | lê D -> escreve D, L
 32 | q8   |  _ [D] D  D  B  B  B  _        | lê D -> escreve D, L
 33 | q8   |  _ [_] D  D  D  B  B  B  _     | lê _ -> escreve _, R
 34 | q9   |  _ [D] D  D  B  B  B  _        | lê D -> escreve A, R   (restaura gabarito)
 35 | q9   |  _  A [D] D  B  B  B  _        | lê D -> escreve A, R
 36 | q9   |  _  A  A [D] B  B  B  _        | lê D -> escreve A, R
 37 | q9   |  _  A  A  A [B] B  B  _        | lê B -> escreve B, R
 38 | q9   |  _  A  A  A  B [B] B  _        | lê B -> escreve B, R
 39 | q9   |  _  A  A  A  B  B [B] _        | lê B -> escreve B, R
 40 | q9   |  _  A  A  A  B  B  B [_] _     | lê _ -> escreve _, S   (não sobrou 1)
 41 | qa   |  _  A  A  A  B  B  B [_] _     | ACEITA
```

**Leitura:** `a=3` (gabarito `AAA`), os `6−3 = 3` uns restantes formaram **1 bloco** exato →
`b = 1+1 = 2`, logo `6 = 3×2`. Como `q₉` não encontrou nenhum `1` restante, vai a `qₐ`.

## 4. Traço de ramo que **rejeita** — `1⁶`, `a=4`

```
  ... (Fase 1 marca AAAA, Fase 2 consome o 1º bloco de 4) ...
 28 | q7   |  _  D  D [A] A  B  B  _        | lê A -> escreve C, R
 29 | q5   |  _  D  D  C [A] B  B  _        | lê A -> escreve A, R
 30 | q5   |  _  D  D  C  A [B] B  _        | lê B -> escreve B, R
 31 | q5   |  _  D  D  C  A  B [B] _        | lê B -> escreve B, R
 32 | q5   |  _  D  D  C  A  B  B [_]       | PARA (rejeita: faltou 1 p/ fechar o 2º bloco)
```

**Leitura:** com `a=4`, após consumir 4 uns sobram apenas 2; ao tentar o 2º bloco a cabeça
chega ao branco em `q₅` sem `1` disponível → `δ(q₅,⊔) = ∅` → ramo para **sem aceitar**.
Como nenhum palpite de `a` fecha (ver árvore), se `6` fosse primo a entrada seria rejeitada;
mas `a=2` e `a=3` fecham, então `1⁶` é aceito.

## 5. O que rodar no JFLAP (evidência ao vivo)

1. Abrir `implementacoes/mtnd-compostos/compostos.jff`.
2. *Input → Multiple Run* com a lista da Tabela 1 → conferir Accept/Reject.
3. *Input → Step Run* (ou árvore de não determinismo) com `1⁶` → mostrar os ramos `a=2…6`.
4. Capturar print da árvore e anexar em `testes/mtnd-compostos/` (ex.: `arvore-1^6.png`).
