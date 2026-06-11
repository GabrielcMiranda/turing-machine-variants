# MTND — Compostos em unário · Tabela de transição

**Linguagem:** `L = { 1ⁿ : n = a·b, com a ≥ 2 e b ≥ 2 }` (números compostos em unário).
**Modelo:** Máquina de Turing **Não Determinística**, 1 fita.
**Aceitação:** por existência de ramo que para no estado final `qa`.

## Alfabetos
- Entrada: `Σ = {1}`
- Fita: `Γ = {1, A, B, C, D, ⊔}` (`⊔` = branco)

## Símbolos auxiliares (significado)
- `1` — célula ainda não processada da entrada.
- `A` — célula do **gabarito** do divisor `a` (bloco fixo à esquerda).
- `B` — `1` já **consumido** (cruzado) durante a verificação.
- `C` — marca do `A` **corrente** dentro de um passe (temporária).
- `D` — `A` já **usado** no passe corrente (temporária; restaurada para `A` ao fim do passe).

## Estados (12 — requisito “> 8 estados”)
| Estado | Papel |
|--------|-------|
| `q0` | inicial — lê o 1º `1`, força 1ª conversão |
| `q1` | força a 2ª conversão (garante `a ≥ 2`) |
| `q2` | **não determinístico**: continuar convertendo `A` OU parar (adivinha `a`) |
| `q3` | rebobina à esquerda até o início após adivinhar `a` |
| `q4` | início do passe — torna o `A` mais à esquerda o corrente (`C`) |
| `q5` | procura o próximo `1` à direita e o consome (`1→B`) |
| `q6` | volta à esquerda até o `C` corrente |
| `q7` | avança ao próximo `A` (novo corrente) ou detecta fim do passe |
| `q8` | vai ao extremo esquerdo para restaurar o gabarito |
| `q9` | restaura `D→A` e detecta se sobrou `1` (senão, aceita) |
| `q10`| rebobina para iniciar novo passe |
| `qa` | **final (aceitação)** |

## Tabela de transição δ (formato: estado, lê → escreve, move, vai-para)
Movimentos: `R` direita, `L` esquerda, `S` parado. `⊔` = branco.

### Fase 1 — adivinhar `a` (a ≥ 2)
| # | Estado | Lê | Escreve | Move | Próximo |
|---|--------|----|---------|------|---------|
| 1 | q0 | 1 | A | R | q1 |
| 2 | q1 | 1 | A | R | q2 |
| 3 | q2 | 1 | A | R | q2 | ← (não det.) continua convertendo |
| 4 | q2 | 1 | 1 | L | q3 | ← (não det.) para de converter |

> Em q0/q1, se ler `⊔` (entrada vazia ou `n=1`) **não há transição** → rejeita.
> Em q2, ler `⊔` (todos viraram `A`, `a=n`) → sem transição → rejeita (`b=1`).

### Rebobinar após adivinhar
| # | Estado | Lê | Escreve | Move | Próximo |
|---|--------|----|---------|------|---------|
| 5 | q3 | A | A | L | q3 |
| 6 | q3 | ⊔ | ⊔ | R | q4 |

### Fase 2 — verificar `n = a·b` com `b ≥ 2`
| # | Estado | Lê | Escreve | Move | Próximo |
|---|--------|----|---------|------|---------|
| 7  | q4 | A | C | R | q5 | torna o `A` corrente |
| 8  | q5 | A | A | R | q5 | pula gabarito à direita do `C` |
| 9  | q5 | B | B | R | q5 | pula `1`s já consumidos |
| 10 | q5 | 1 | B | L | q6 | consome um `1` |
| 11 | q6 | B | B | L | q6 | volta passando `B`s |
| 12 | q6 | A | A | L | q6 | volta passando `A`s |
| 13 | q6 | C | D | R | q7 | marca corrente como usado |
| 14 | q7 | A | C | R | q5 | próximo `A` vira corrente |
| 15 | q7 | B | B | L | q8 | fim do passe (gabarito esgotado) |

> Em q5, ler `⊔` (faltou `1` para completar o bloco) → sem transição → rejeita o ramo.

### Fim do passe — restaurar gabarito e decidir
| # | Estado | Lê | Escreve | Move | Próximo |
|---|--------|----|---------|------|---------|
| 16 | q8 | D | D | L | q8 | vai ao extremo esquerdo |
| 17 | q8 | ⊔ | ⊔ | R | q9 |
| 18 | q9 | D | A | R | q9 | restaura gabarito |
| 19 | q9 | B | B | R | q9 | pula consumidos |
| 20 | q9 | 1 | 1 | L | q10 | sobrou `1` → novo passe |
| 21 | q9 | ⊔ | ⊔ | S | qa | **nada sobrou → ACEITA** |
| 22 | q10 | B | B | L | q10 | rebobina |
| 23 | q10 | A | A | L | q10 | rebobina |
| 24 | q10 | ⊔ | ⊔ | R | q4 | volta ao início do gabarito → novo passe |

**Total: 24 transições** (requisito “≥ 10 transições relevantes”).

## Ideia em uma frase
O não determinismo em **q2 adivinha o fator `a`** (cada escolha é um ramo da árvore);
a Fase 2 verifica **deterministicamente** que os `1`s restantes se dividem em blocos exatos
de tamanho `a`, exigindo pelo menos um bloco (`b ≥ 2`). Basta **um ramo** fechar para aceitar.
