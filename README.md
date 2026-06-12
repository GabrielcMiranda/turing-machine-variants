# Projeto Final — Teoria da Computabilidade (AV2)

**Disciplina:** Teoria da Computabilidade
**Professor:** Daniel Leal Souza
**Semestre:** 01/2026
**Turma:** `<preencher: CC5MA ou CC5NA>`
**Tema:** Máquinas Universais, Turing e λ-Cálculo

**Integrantes:**

| Nome | Papel principal |
|------|-----------------|
| Carlos Eduardo Cardoso Silva | Máquina de Turing Não Determinística (JFLAP) |
| Gabriel Costa de Miranda | Combinadores SKI (Python) |
| João Ricardo Silva de Almeida | Integração, documentação e defesa |

> A arguição é **individual**: todos os integrantes sabem explicar as **duas** implementações.

---

## 1. Visão geral

Este repositório contém a entrega da AV2, que exige a escolha de **dois modelos de computação
distintos** e **uma implementação bem elaborada para cada um**, resolvendo **problemas
diferentes**. Os dois modelos escolhidos foram:

| # | Modelo (Seção 3 da lauda) | Problema resolvido | Ferramenta |
|---|---------------------------|--------------------|------------|
| 1 | **λ-Cálculo → Combinadores SKI** (opção 7) | Eliminação de variáveis: traduzir λ-termos para `S`/`K`/`I` e reduzir termos puros (Turing-completude sem variáveis) | **Python** |
| 2 | **MT Não Determinística** (opção 4) | Reconhecer **números compostos em unário**: `L = { 1ⁿ : n = a·b, a ≥ 2, b ≥ 2 }` | **JFLAP** |

Os problemas são claramente distintos — uma **transformação/redução de termos** e um
**reconhecimento de linguagem** — satisfazendo a exigência de "problemas diferentes".

---

## 2. Estrutura do repositório

```
turing-machine-variants/
├── README.md                       # este arquivo
├── PLANO.md                        # plano de desenvolvimento do grupo
├── referencias.md                  # bibliografia consultada
├── uso_ia.md                       # declaração de uso de IA
├── lauda projeto final.pdf         # enunciado oficial da atividade
├── implementacoes/
│   ├── lambda-ski/                 # Implementação 1 (Python)
│   │   ├── ski.py                  # termos, parser e redutor SKI (ordem normal)
│   │   ├── abstracao.py            # eliminação de abstração (bracket abstraction)
│   │   ├── demo.py                 # CLI: imprime traços passo a passo
│   │   ├── test_ski.py             # testes automatizados (unittest)
│   │   └── documentacao_ski.md     # fundamentação teórica + roteiro de defesa
│   └── mtnd-compostos/             # Implementação 2 (JFLAP)
│       ├── compostos.jff           # MT não determinística (1 fita)
│       ├── formalizacao.md         # 7-upla, δ, prova de correção
│       ├── tabela-transicoes.md    # tabela de transição comentada
│       └── _verifica.py            # oráculo Python (simula a MTND por BFS)
├── testes/
│   └── mtnd-compostos/
│       ├── rastreamento.md         # tabela de testes + traços passo a passo
│       └── rastreamento.py         # reproduz a tabela e os traços
└── slides/
    ├── mtnd-compostos.md           # slides da MTND (Marp)
    └── roteiro-mtnd.md             # roteiro de fala da MTND
```

---

## 3. Pré-requisitos

- **Python 3.8+** — apenas biblioteca padrão (`unittest`, `collections`). Não há dependências
  externas para instalar.
- **JFLAP 7.0+** — para abrir e simular o arquivo `.jff`. Requer **Java (JRE 8+)** instalado.
  Download em <https://www.jflap.org>.

Clonar o repositório:

```bash
git clone <URL do repositório>
cd turing-machine-variants
```

---

## 4. Como rodar — Implementação 1: Combinadores SKI (Python)

Os comandos abaixo assumem que você está na raiz do repositório.

### 4.1 Testes automatizados

```bash
python implementacoes/lambda-ski/test_ski.py
```

Saída esperada (4 testes, todos passando):

```
....
----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK
```

### 4.2 Demonstração com traços passo a passo

```bash
python implementacoes/lambda-ski/demo.py
```

A demo reduz quatro termos em **ordem normal** (redex mais externo à esquerda primeiro),
imprimindo cada passo e a regra aplicada. Exemplos da saída:

**`I = S K K` (mostra que `SKK` age como identidade):**

```
--- 1. Identidade como SKK (SKK x) ---
Expressão Inicial: S K K x
  Passo 01: S K K x       ====> [S x y z -> x z (y z)]
  Passo 02: K x (K x)     ====> [K x y -> x]
Forma Normal Final: x
```

**Numeral de Church 2 (`S B I = S (S (K S) K) (S K K)`) aplicado a `f x` — traço de 7 passos:**

```
--- 3. Numeral de Church 2 aplicado a f x (>= 7 passos) ---
Expressão Inicial: S (S (K S) K) (S K K) f x
  Passo 01: S (S (K S) K) (S K K) f x   ====> [S x y z -> x z (y z)]
  Passo 02: S (K S) K f (S K K f) x     ====> [S x y z -> x z (y z)]
  Passo 03: K S f (K f) (S K K f) x     ====> [K x y -> x]
  Passo 04: S (K f) (S K K f) x         ====> [S x y z -> x z (y z)]
  Passo 05: K f x (S K K f x)           ====> [K x y -> x]
  Passo 06: f (S K K f x)               ====> [S x y z -> x z (y z)]
  Passo 07: f (K f (K f) x)             ====> [K x y -> x]
Forma Normal Final: f (f x)
Total de passos: 7
```

O quarto exemplo (`Ω = S I I (S I I)`) **não normaliza** e ilustra o Problema da Parada: a
redução é cortada pelo limite `max_steps`.

> Fundamentação teórica completa, regras de `S`/`K`/`I`, o algoritmo de *bracket abstraction*
> e o roteiro de defesa estão em [`implementacoes/lambda-ski/documentacao_ski.md`](implementacoes/lambda-ski/documentacao_ski.md).

---

## 5. Como rodar — Implementação 2: MTND de compostos em unário (JFLAP)

### 5.1 No JFLAP (demonstração principal)

1. Abrir o JFLAP e carregar [`implementacoes/mtnd-compostos/compostos.jff`](implementacoes/mtnd-compostos/compostos.jff).
2. **Input → Multiple Run**: testar vários `1ⁿ` de uma vez (ver tabela abaixo).
3. **Input → Step Run** (ou a árvore de não determinismo) com `1⁶` para visualizar os ramos
   `a = 2…6` — o não determinismo está em `q₂` (adivinhar o fator `a`).

A entrada é o número `n` em unário (`n` repetições de `1`). A máquina **aceita** se `n` é
composto e **rejeita** se for primo, `0` ou `1`.

| Entrada | n | Resultado |
|---------|---|-----------|
| `1111` | 4 = 2×2 | ✅ aceita |
| `111111` | 6 = 2×3 | ✅ aceita |
| `111111111` | 9 = 3×3 | ✅ aceita |
| `11111` | 5 (primo) | ❌ rejeita |
| `1111111` | 7 (primo) | ❌ rejeita |
| `1` | 1 | ❌ rejeita |
| (vazio) | 0 | ❌ rejeita |

### 5.2 Oráculo Python (evidência reproduzível, sem JFLAP)

Reproduz a mesma relação de transição δ por busca em largura na árvore de computação:

```bash
python testes/mtnd-compostos/rastreamento.py   # tabela de testes + traços passo a passo + árvore do 1⁶
python implementacoes/mtnd-compostos/_verifica.py   # valida 18 casos (aceitos/rejeitados/fronteira)
```

> A formalização (7-upla, relação δ, prova de correção e relação com computabilidade) está em
> [`implementacoes/mtnd-compostos/formalizacao.md`](implementacoes/mtnd-compostos/formalizacao.md);
> a tabela de transição comentada em
> [`implementacoes/mtnd-compostos/tabela-transicoes.md`](implementacoes/mtnd-compostos/tabela-transicoes.md).

---

## 6. Testes e rastreamento de execução

- **SKI:** `test_ski.py` (regras `S`/`K`/`I`, `SKK ⇒ I`, bracket abstraction, termo não
  normalizante) + traços em `demo.py` e em `documentacao_ski.md`.
- **MTND:** [`testes/mtnd-compostos/rastreamento.md`](testes/mtnd-compostos/rastreamento.md)
  — tabela entrada/esperado/obtido, árvore de ramos do `1⁶` e traço passo a passo de 41 passos
  de um ramo aceitante; reprodutível por `rastreamento.py` e validado por `_verifica.py`.

---

## 7. Documentação adicional

- **Referências consultadas:** [`referencias.md`](referencias.md)
- **Declaração de uso de IA:** [`uso_ia.md`](uso_ia.md)
- **Slides da apresentação:** pasta [`slides/`](slides/)
