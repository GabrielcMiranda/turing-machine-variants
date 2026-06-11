# Plano — Projeto Final Teoria da Computabilidade (AV2)

## Contexto

Trabalho em grupo (3 integrantes) da disciplina Teoria da Computabilidade / CESUPA.
Pela lauda, equipe de **até 4 integrantes** deve escolher **exatamente 2 máquinas/modelos**
e entregar **exatamente 2 implementações** (1 bem elaborada por modelo). Os dois modelos
escolhidos são:

1. **λ-Cálculo → Combinadores SKI** — implementação em **Python**.
2. **MT Não Determinística → reconhecer números compostos em unário** — em **JFLAP (.jff)**.

Os dois resolvem problemas claramente distintos (eliminação de abstração lambda vs.
reconhecimento de linguagem `{1ⁿ : n = a·b, a,b ≥ 2}`), satisfazendo a regra de "problemas
diferentes". Repositório está vazio (greenfield); este plano cobre estrutura, as duas
implementações, divisão para 3 pessoas e os entregáveis exigidos pela lauda (README, slides,
rastreamento, uso_ia, referências).

> Observação: o prazo fica por conta do grupo (não é restrição deste plano).

---

## Estrutura do repositório (Seção 9 da lauda)

```
/
├── README.md                      # turma, integrantes, modelos, problemas, como rodar, deps, exemplos
├── uso_ia.md                      # declaração de uso de IA (obrigatório mesmo se "não usou")
├── referencias.md                 # Diverio & Menezes, Menezes, slides da disciplina, doc JFLAP
├── implementacoes/
│   ├── lambda-ski/                # Python
│   │   ├── ski.py                 # núcleo: termos, parser, redutor SKI
│   │   ├── abstracao.py           # eliminação de abstração lambda (bracket abstraction)
│   │   ├── demo.py                # exemplos: I=SKK, booleanos, etc. (CLI)
│   │   └── test_ski.py            # testes automatizados
│   └── mtnd-compostos/            # JFLAP
│       └── compostos.jff          # MT não determinística (1 fita)
├── testes/                        # rastreamento de execução
│   ├── lambda-ski/                # traços passo a passo (>= 7 passos) + casos
│   └── mtnd-compostos/            # tabela: entrada, esperado, obtido, ramo aceitante
└── slides/                        # PDF/PPTX ou link
```

---

## Implementação 1 — Combinadores SKI (Python)

### Objetivo conceitual
Mostrar que **toda função lambda pode ser expressa só com S e K** (I é dispensável,
pois `I = SKK`). É a "história" forte na arguição: *eliminação de variáveis*.

### Regras de redução (núcleo do redutor)
- `I x        → x`
- `K x y      → x`
- `S x y z    → x z (y z)`

Estratégia de redução: **ordem normal** (mais externo à esquerda primeiro), com limite de
passos para evitar loop infinito (ex.: `S I I (S I I)` não normaliza).

### Componentes
- **`ski.py`**
  - Representação de termos: átomos `S`, `K`, `I` e variáveis livres (`x`, `y`, ...);
    aplicação `App(esq, dir)` associativa à esquerda.
  - **Parser** de string → termo (ex.: `"S K K x"`, parênteses, associatividade à esquerda).
  - **Redutor** passo a passo: cada passo retorna o termo reduzido + qual regra aplicou,
    para gerar o traço.
- **`abstracao.py`** — algoritmo de *bracket abstraction* `T[λx.E]` → termo SKI:
  - `T[x] = x`
  - `T[λx.x] = I`
  - `T[λx.E] = K (T[E])`  se `x` não ocorre em `E`
  - `T[λx.(E F)] = S (T[λx.E]) (T[λx.F])`
  - Converte um termo lambda em combinadores puros (a demonstração da eliminação).
- **`demo.py`** — exemplos documentados (CLI que imprime cada passo):
  - `I = SKK`: reduzir `S K K x → K x (K x) → x` (mostra que SKK age como identidade).
  - Booleanos de Church em SK: `TRUE = K`, `FALSE = K I` (= `S K`), e reduzir `TRUE a b → a`.
  - Pelo menos **um exemplo com ≥ 7 passos de redução** (requisito da Seção 7).
- **`test_ski.py`** — testes que verificam: `SKKx ⇒ x`, `Kxy ⇒ x`, `Sxyz ⇒ xz(yz)`,
  conversão lambda→SKI, e um termo que não normaliza (corta no limite de passos).

### Por que não é trivial (para a análise técnica)
Sistema Turing-completo sem variáveis nem ambiente de nomes; a substituição "desaparece"
dentro das regras de S e K. Limitação observada: termos que não normalizam (necessidade do
limite de passos) — ilustra indecidibilidade da parada.

---

## Implementação 2 — MT Não Determinística: compostos em unário (JFLAP)

### Linguagem
`L = { 1ⁿ : n = a·b, com a ≥ 2 e b ≥ 2 }` (números **compostos** em unário).
Entrada `1ⁿ`. **Aceita** se composto; **rejeita** se primo, 0 ou 1.

### Ideia (uso essencial do não determinismo)
A MT **"adivinha" o fator `a`** e depois **verifica deterministicamente** que `n` é múltiplo
de `a` com quociente `≥ 2`. É a razão de existir o não determinismo — defende-se sozinho.

### Construção (MT de 1 fita; alfabeto de fita `{1, A, B, _}`)
**Fase 1 — adivinhar `a` (não determinístico):**
- Converte as primeiras células `1 → A`. Força **≥ 2** conversões (a ≥ 2).
- A partir da 2ª, há **transição não determinística**: "continuar convertendo" OU "parar".
  Resultado: `A^a 1^(n-a)` com `a ≥ 2`. Cada valor de `a` é um ramo da árvore.

**Fase 2 — verificar `n = a·b` com `b ≥ 2` (determinístico):**
- Cruza o restante `1^(n-a)` em **blocos de tamanho `a`**, usando o bloco `A` como gabarito:
  para cada `A`, anda à direita até o próximo `1` e marca `1 → B`; volta. Um "passe" completo
  cruza um bloco de `a` uns.
- Se faltar `1` no meio de um passe → **rejeita esse ramo**.
- Exige **pelo menos um passe completo** (garante `b ≥ 2`, pois o bloco `A` já é a 1ª cópia).
- Ao terminar um passe, se ainda há `1` → repete; se não há mais `1` → **aceita**.
- Se logo após a Fase 1 não sobra nenhum `1` (`n = a`) → rejeita (não é composto por esse fator).

### Critério de aceitação
Aceitação por **existência de ramo aceitante** (semântica padrão da MTND). JFLAP explora os
ramos; basta um chegar ao estado de aceitação.

### Requisitos de complexidade (Seção 7)
A construção tem **> 8 estados** (guess-A, garantir a≥2, retorno à esquerda, ativar A, buscar
próximo 1, marcar/voltar, fim-de-passe, detectar 1 restante, aceitar, rejeitar) e **≥ 10
transições relevantes**. Conferir contagem ao montar o `.jff`.

### Casos de teste (≥ 3, com aceitos / rejeitados / fronteira)
- `1⁶` (6 = 2·3) → **aceita** (ramo a=2 ou a=3).
- `1⁹` (9 = 3·3) → **aceita**.
- `1⁴` (4 = 2·2) → **aceita** (fronteira: menor composto par).
- `1⁵`, `1⁷` (primos) → **rejeita** (nenhum ramo fecha).
- `1¹`, vazio → **rejeita** (fronteira).

> Nota técnica para a arguição: validar no JFLAP se o simulador de MT explora não
> determinismo como esperado; se a árvore ficar pesada, restringir o teste a `n` pequeno e
> mostrar a árvore de ramos para `1⁶`.

---

## Divisão para 3 pessoas

Como há **2 implementações** e **3 pessoas**, a 3ª pessoa assume a carga de
**integração + documentação + defesa** (pesada na rubrica: GitHub/doc 0,40 + seminário 0,20),
e todos fazem **revisão cruzada** porque a arguição é individual (0,45) — cada um precisa saber
explicar as duas máquinas.

**Pessoa 1 — Dona da MTND (JFLAP)**
- Projeta a tabela de transição e monta `compostos.jff` (conferir > 8 estados / ≥ 10 transições).
- Formalização da MTND: estados, alfabetos, relação δ, aceitação por ramo.
- Rastreamento dos casos de teste (tabela entrada/esperado/obtido + print da árvore p/ `1⁶`).
- Slides + roteiro de teoria da MTND (não determinismo, árvore de computação).

**Pessoa 2 — Dona do SKI (Python)**
- `ski.py` (termos, parser, redutor) + `abstracao.py` (lambda→SKI) + `demo.py` + `test_ski.py`.
- Formalização do λ-cálculo/SKI: sintaxe, regras de S/K/I, eliminação de abstração.
- Rastreamento: traço com ≥ 7 passos + casos (I=SKK, booleanos, termo não-normalizante).
- Slides + roteiro de teoria do SKI (Turing-completude sem variáveis).

**Pessoa 3 — Integração / Documentação / Defesa**
- Estrutura do repo, `README.md` (turma, integrantes, modelos, problemas, como rodar, deps,
  exemplos), `referencias.md`, `uso_ia.md`.
- Monta o deck de slides final (junta os roteiros de P1 e P2) e cronometra 12–15 min.
- QA: roda os dois projetos do zero seguindo o README, revisa os rastreamentos.
- Roteiro de teoria transversal: Hipótese de Church-Turing, determinismo × não determinismo,
  relação λ-cálculo ↔ combinadores.
- **Revisão cruzada:** garante que P1 sabe explicar o SKI e P2 sabe explicar a MTND.

---

## Verificação (como testar de ponta a ponta)

- **SKI:** `python implementacoes/lambda-ski/test_ski.py` (ou `pytest`) — todos passam;
  `python implementacoes/lambda-ski/demo.py` imprime os traços passo a passo.
- **MTND:** abrir `compostos.jff` no JFLAP, rodar "Multiple Run" com a lista de casos de teste;
  conferir aceita/rejeita conforme a tabela; gerar print da árvore de `1⁶`.
- **Repro (Pessoa 3):** clonar do zero, seguir só o README, e confirmar que os dois exemplos
  rodam — requisito de auditabilidade da lauda.

## Checklist final (mapeado à rubrica, Seção 12/16)
- [ ] 2 modelos distintos, 2 implementações, problemas diferentes.
- [ ] MTND com > 8 estados e ≥ 10 transições.
- [ ] λ-cálculo com ≥ 7 passos de redução (ou avaliador funcional — aqui temos os dois).
- [ ] ≥ 3 testes por implementação (aceito / rejeitado / fronteira) com rastreamento.
- [ ] README executável, referências citadas, `uso_ia` presente.
- [ ] Slides 12–15 min, participação identificável dos 3.
- [ ] Todos sabem explicar as duas máquinas (arguição individual).
