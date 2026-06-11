# Formalização da MTND — Reconhecimento de compostos em unário

## 1. Problema e linguagem reconhecida

A máquina reconhece a linguagem dos **números compostos representados em unário**:

$$L = \{\, 1^{n} \mid n = a \cdot b,\ a \ge 2,\ b \ge 2 \,\}$$

Equivalente: `1ⁿ ∈ L` se e somente se `n` é composto (`n ≥ 4` e não primo).
Ficam **fora** de `L`: a cadeia vazia (`n = 0`), `1` (`n = 1`) e os primos (`2, 3, 5, 7, 11, …`).

## 2. Definição formal da máquina

A MTND é a 7-upla

$$M = (Q,\ \Sigma,\ \Gamma,\ \delta,\ q_0,\ \sqcup,\ F)$$

onde:

- **Conjunto de estados:**
  $$Q = \{q_0, q_1, q_2, q_3, q_4, q_5, q_6, q_7, q_8, q_9, q_{10}, q_a\},\quad |Q| = 12$$
- **Alfabeto de entrada:** $\Sigma = \{1\}$
- **Alfabeto de fita:** $\Gamma = \{1, A, B, C, D, \sqcup\}$, sendo $\sqcup$ o símbolo branco e $\Sigma \subset \Gamma$.
- **Estado inicial:** $q_0$
- **Símbolo branco:** $\sqcup$
- **Conjunto de estados finais:** $F = \{q_a\}$
- **Relação de transição** (não determinística):
  $$\delta : Q \times \Gamma \;\longrightarrow\; \mathcal{P}\big(Q \times \Gamma \times \{L, R, S\}\big)$$

Por ser **não determinística**, $\delta$ é uma **relação**: para um par $(q, x)$ pode haver
**zero, uma ou várias** ternas $(q', y, m)$ possíveis. Quando $\delta(q,x) = \varnothing$, o
ramo **para sem aceitar** (rejeição daquele ramo). $m \in \{L, R, S\}$ indica o movimento da
cabeça (esquerda, direita, parado).

### 2.1 Significado dos símbolos auxiliares de fita

| Símbolo | Significado |
|---------|-------------|
| `1` | célula da entrada ainda não processada |
| `A` | célula do **gabarito** do divisor `a` (bloco fixo à esquerda) |
| `B` | `1` já **consumido** (cruzado) na verificação |
| `C` | `A` **corrente** dentro de um passe (marca temporária) |
| `D` | `A` já **usado** no passe corrente (temporária; restaurada a `A` ao fim do passe) |
| `⊔` | branco |

## 3. A relação de transição δ

A única fonte de **não determinismo** está em $q_2$ lendo `1`:

$$\delta(q_2, 1) = \{\,(q_2,\ A,\ R),\ (q_3,\ 1,\ L)\,\}$$

— "continuar marcando o gabarito" **ou** "parar e fixar o tamanho `a`". Cada decisão gera um
ramo da árvore de computação; em conjunto, esses ramos enumeram **todos os valores possíveis
de `a` com `a ≥ 2`**. Todas as demais transições são determinísticas (conjuntos unitários).

Tabela completa (entradas omitidas de $\delta$ valem $\varnothing$ → parada sem aceitar):

| $q$ | lê | → | escreve | move | vai p/ | comentário |
|-----|----|---|---------|------|--------|-----------|
| $q_0$ | 1 | | A | R | $q_1$ | 1ª marca |
| $q_1$ | 1 | | A | R | $q_2$ | 2ª marca (garante `a ≥ 2`) |
| $q_2$ | 1 | | A | R | $q_2$ | **(nd)** continua marcando |
| $q_2$ | 1 | | 1 | L | $q_3$ | **(nd)** para; `a` fixado |
| $q_3$ | A | | A | L | $q_3$ | rebobina |
| $q_3$ | ⊔ | | ⊔ | R | $q_4$ | início da verificação |
| $q_4$ | A | | C | R | $q_5$ | `A` mais à esquerda vira corrente |
| $q_5$ | A | | A | R | $q_5$ | pula gabarito |
| $q_5$ | B | | B | R | $q_5$ | pula consumidos |
| $q_5$ | 1 | | B | L | $q_6$ | consome um `1` |
| $q_6$ | B | | B | L | $q_6$ | volta |
| $q_6$ | A | | A | L | $q_6$ | volta |
| $q_6$ | C | | D | R | $q_7$ | corrente vira "usado" |
| $q_7$ | A | | C | R | $q_5$ | próximo `A` corrente |
| $q_7$ | B | | B | L | $q_8$ | fim do passe |
| $q_8$ | D | | D | L | $q_8$ | vai ao extremo esquerdo |
| $q_8$ | ⊔ | | ⊔ | R | $q_9$ | |
| $q_9$ | D | | A | R | $q_9$ | restaura gabarito |
| $q_9$ | B | | B | R | $q_9$ | pula consumidos |
| $q_9$ | 1 | | 1 | L | $q_{10}$ | sobrou `1` → novo passe |
| $q_9$ | ⊔ | | ⊔ | S | $q_a$ | **nada sobrou → ACEITA** |
| $q_{10}$ | B | | B | L | $q_{10}$ | rebobina |
| $q_{10}$ | A | | A | L | $q_{10}$ | rebobina |
| $q_{10}$ | ⊔ | | ⊔ | R | $q_4$ | novo passe |

## 4. Critério de aceitação (por ramo existente)

Uma **configuração** é uma terna (estado, conteúdo da fita, posição da cabeça). A configuração
inicial sobre a entrada `w = 1ⁿ` é $(q_0,\ 1^{n},\ 0)$. A relação de passo $\vdash_M$ aplica
**alguma** terna de $\delta$; o fecho reflexivo-transitivo é $\vdash_M^{*}$.

$$w \in L(M) \iff \exists\ \text{computação } (q_0, w, 0) \vdash_M^{*} (q_a, \cdot, \cdot)$$

Isto é, **aceita por existência de pelo menos um ramo** que alcança o estado final $q_a$
(semântica padrão da MT não determinística). A árvore de computação tem ramos que:
- **param sem aceitar** quando $\delta = \varnothing$ (ex.: $q_5$ lendo `⊔` — faltou `1` para
  fechar um bloco; ou $q_2$ lendo `⊔` — todos viraram `A`, sobrou `b = 1`);
- **aceitam** ao atingir $q_a$.

Basta um ramo aceitante para `w ∈ L(M)`.

## 5. Correção (por que reconhece exatamente os compostos)

**Invariante após a Fase 1 (ramo que para em $q_2$ com `a` marcas):** a fita contém
$A^{a}\,1^{\,n-a}$ com $a \ge 2$, e cada valor $2 \le a \le n$ é produzido por **algum** ramo.

**Fase 2 (verificação determinística):** cada *passe* consome exatamente `a` ocorrências de `1`
(uma por célula do gabarito), marcando-as como `B`; ao fim do passe o gabarito é restaurado.
A máquina repete passes até não sobrar `1`.

- Se, ao chegar em $q_9$, **não há mais `1`**, então os `n-a` uns restantes foram consumidos em
  um número inteiro $k \ge 1$ de passes, logo $n - a = k\cdot a$, ou seja
  $n = (k+1)\cdot a$ com $k+1 \ge 2$. Tomando $b = k+1$ temos $n = a\cdot b$, $a,b \ge 2$ →
  **aceita** (corretamente, `n` é composto).
- Se em algum passe falta um `1` para fechar o bloco ($q_5$ lê `⊔`), aquele `a` **não divide**
  `n` → o ramo para sem aceitar.
- Se `a = n` (gabarito consome tudo, nenhum `1` restante já na entrada em $q_2$ ou nenhum passe
  possível), então `b = 1` e o ramo não aceita.

**Conclusão:** existe ramo aceitante $\iff$ existe `a` com $2 \le a$ e `a | n` e `n/a ≥ 2`
$\iff$ `n` é composto. Portanto $L(M) = L$.

## 6. Relação com computabilidade

- **Não determinismo como "adivinhação":** o modelo expressa diretamente "existe um fator `a`?".
  É a motivação clássica do não determinismo — o ramo certo é *adivinhado* e a verificação é
  eficiente e determinística.
- **Equivalência com a MT determinística:** pela tese de Church–Turing e pelo teorema de
  equivalência, toda MTND tem uma MTD que reconhece a mesma linguagem (simulando a árvore de
  computação, p.ex. por busca em largura). O não determinismo **não aumenta o poder de
  reconhecimento** — apenas a *clareza* da descrição. `L` é, portanto, **recursiva (decidível)**:
  a máquina sempre para (todo ramo termina), aceitando ou rejeitando.
- **Limitações observadas:** o modelo decide pertinência, mas o número de ramos cresce com `n`
  (cada `a` candidato é um ramo), o que torna a simulação determinística da árvore custosa —
  ilustra a diferença entre *reconhecibilidade* e *custo* de computação.

## 7. Resumo dos componentes formais

| Componente | Valor |
|------------|-------|
| $Q$ | $\{q_0,\dots,q_{10}, q_a\}$ (12 estados) |
| $\Sigma$ | $\{1\}$ |
| $\Gamma$ | $\{1, A, B, C, D, \sqcup\}$ |
| $q_0$ | $q_0$ |
| $\sqcup$ | branco |
| $F$ | $\{q_a\}$ |
| $\delta$ | 24 transições (1 par não determinístico em $q_2$) |
| aceitação | existência de ramo que atinge $q_a$ |
