---
marp: true
title: MT Não Determinística — Compostos em unário
paginate: true
---

<!--
Slides da Pessoa 1 (parte da MTND no seminário conjunto).
Renderizar com Marp (VS Code: extensão "Marp for VS Code" -> Export to PPTX/PDF),
ou copiar o conteúdo para o Google Slides. ~4-5 min desta parte.
-->

# MT Não Determinística
## Reconhecendo números **compostos** em unário

`L = { 1ⁿ : n = a·b, com a ≥ 2 e b ≥ 2 }`

Teoria da Computabilidade — AV2
Implementação em JFLAP (`compostos.jff`)

---

# O problema

- Entrada: um número `n` escrito em **unário** → `1ⁿ` (ex.: `6 = 111111`).
- **Aceitar** se `n` é **composto** (`n = a·b`, com `a, b ≥ 2`).
- **Rejeitar** se `n` é primo, ou `n = 0`, ou `n = 1`.

| Entrada | n | Resultado |
|---------|---|-----------|
| `1111` | 4 = 2×2 | ✅ aceita |
| `111111` | 6 = 2×3 | ✅ aceita |
| `11111` | 5 (primo) | ❌ rejeita |
| `1` | 1 | ❌ rejeita |

---

# Por que NÃO determinística?

> "**Existe** um fator `a` de `n` com `2 ≤ a` e quociente `≥ 2`?"

- Perguntas do tipo **"existe..."** são a motivação clássica do não determinismo.
- A máquina **adivinha** o fator `a` (não precisa testar um por um no código).
- Cada palpite de `a` é um **ramo** da árvore de computação.
- **Aceita se algum ramo** encontra uma fatoração válida.

É literalmente a razão de existir o não determinismo.

---

# Definição formal

$$M = (Q, \Sigma, \Gamma, \delta, q_0, \sqcup, F)$$

- **Estados:** `Q = {q₀,…,q₁₀, qₐ}` → **12 estados**
- **Entrada:** `Σ = {1}`
- **Fita:** `Γ = {1, A, B, C, D, ⊔}`
- **Final:** `F = {qₐ}`
- **δ é uma _relação_** (não função): em `q₂` lendo `1` há **duas** saídas
  $$\delta(q_2, 1) = \{(q_2, A, R),\ (q_3, 1, L)\}$$
- **24 transições** no total.

---

# Como funciona — duas fases

**Fase 1 — adivinhar `a` (não determinística)**
- Marca os primeiros `1`s como `A` (gabarito do divisor).
- Força `a ≥ 2`; em `q₂` decide *não deterministicamente* parar de marcar.
- Resultado de um ramo: `Aᵃ 1ⁿ⁻ᵃ`.

**Fase 2 — verificar (determinística)**
- Usa o bloco `A` como **gabarito** e cruza os `1`s restantes em **blocos de tamanho `a`**.
- Cada `1` consumido vira `B`. Exige ≥ 1 bloco completo (garante `b ≥ 2`).
- Sobrou `1` no meio do bloco → ramo **para sem aceitar**.
- Zerou os `1`s exatamente → **aceita**.

---

# Árvore de computação — `1⁶`

```
raiz: q0 sobre 111111
 ├── a=2 → ACEITA  (6 = 2×3)
 ├── a=3 → ACEITA  (6 = 3×2)
 ├── a=4 → rejeita (4 ∤ 6)
 ├── a=5 → rejeita (5 ∤ 6)
 └── a=6 → rejeita (b = 1)
```

**Basta um ramo aceitante** → `1⁶` é aceita.
(Um primo como `1⁵` fecha *nenhum* ramo → rejeita.)

---

# Demonstração (JFLAP)

1. Abrir `compostos.jff`.
2. **Multiple Run**: `1⁴, 1⁶, 1⁸, 1⁹` (aceita) · `1⁵, 1⁷, 1¹¹, 1` (rejeita).
3. **Step Run / árvore** com `1⁶` → mostrar os ramos `a = 2…6`.
4. Traço completo (41 passos do ramo `a=3`) no relatório.

> Oráculo independente: `python rastreamento.py` reproduz tabela + traços.

---

# Análise técnica

- **Correção:** existe ramo aceitante ⟺ existe `a ≥ 2` com `a | n` e `n/a ≥ 2` ⟺ `n` composto.
  Portanto `L(M) = L`.
- **Equivalência com a MTD:** por Church–Turing, há uma MTD equivalente (simula a árvore por
  busca). O não determinismo **não aumenta o poder** — só simplifica a descrição.
- **`L` é decidível:** todo ramo sempre para (aceitando ou não).
- **Limitação:** o nº de ramos cresce com `n` → simular a árvore de forma determinística é
  custoso. Ilustra *reconhecibilidade* ≠ *custo*.

---

# Resumo

- MTND de **12 estados / 24 transições** que reconhece **compostos em unário**.
- Não determinismo = **adivinhar o fator**; verificação determinística por blocos.
- Aceitação **por ramo existente**; equivalente a uma MTD (mais custosa).
- Evidências: `compostos.jff`, tabela de testes, traços passo a passo, árvore do `1⁶`.

**Obrigado!**
