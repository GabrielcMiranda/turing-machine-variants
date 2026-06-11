# Roteiro de apresentação — Pessoa 1 (MTND compostos)

Parte da MTND no seminário conjunto. Alvo: **~4 a 5 minutos** de fala + participação na
demonstração. Tempo total da equipe: 12–15 min (recomendação da lauda: 3' teoria, 6' demo,
3' análise, 3' arguição). Falar com calma; cada slide ≈ 30–45 s.

## Fala por slide

**Slide 1 — Abertura (20 s)**
> "Nossa segunda implementação é uma Máquina de Turing **não determinística** que reconhece
> números **compostos** escritos em unário. A linguagem é `L = {1ⁿ : n = a·b, com a e b ≥ 2}`."

**Slide 2 — O problema (40 s)**
> "A entrada é o número `n` em unário, ou seja, `n` tracinhos. A máquina aceita se `n` é
> composto e rejeita se for primo, zero ou um. Por exemplo, `1111` (que é 4 = 2×2) é aceito;
> `11111` (5, primo) é rejeitado."

**Slide 3 — Por que não determinística (45 s) — PONTO ALTO**
> "A pergunta que a máquina responde é: *existe* um fator `a` de `n`? Perguntas do tipo
> 'existe' são exatamente a motivação do não determinismo. Em vez de testar fator por fator,
> a máquina **adivinha** o fator `a`. Cada palpite vira um ramo da árvore de computação, e
> ela aceita se **algum** ramo encontra a fatoração."

**Slide 4 — Definição formal (45 s)**
> "Formalmente é a 7-upla `M = (Q, Σ, Γ, δ, q₀, ⊔, F)`. São 12 estados, entrada só com `1`,
> e a fita usa símbolos auxiliares A, B, C, D. O que torna a máquina **não determinística** é
> que `δ` é uma *relação*: no estado `q₂`, lendo `1`, há **duas** transições possíveis — ou
> continua marcando, ou para. No total são 24 transições."

**Slide 5 — Como funciona (60 s)**
> "São duas fases. Na **Fase 1**, a máquina marca os primeiros `1`s como `A` — esse é o
> gabarito do divisor `a`. Ela força pelo menos dois, e em `q₂` decide de forma não
> determinística quando parar. Na **Fase 2**, que é determinística, ela usa esse bloco `A`
> como molde e vai cruzando os `1`s restantes em blocos de tamanho `a`, marcando cada `1` como
> `B`. Se faltar um `1` no meio de um bloco, o ramo morre. Se os `1`s acabarem exatamente, ela
> aceita — porque aí `n` é múltiplo de `a` com quociente pelo menos 2."

**Slide 6 — Árvore do 1⁶ (45 s)**
> "Para `1⁶`, os ramos são os palpites `a = 2, 3, 4, 5, 6`. Os ramos `a=2` e `a=3` aceitam,
> porque 6 = 2×3. Os outros morrem: 4 e 5 não dividem 6, e `a=6` daria quociente 1. Como
> **um** ramo aceita, a entrada é aceita. Se fosse um primo como `1⁵`, nenhum ramo fecharia."

**Slide 7 — Demonstração (transição p/ a demo, 30 s)**
> "No JFLAP a gente roda o Multiple Run com vários casos, e o Step Run para mostrar a árvore
> de ramos do `1⁶`. Temos também um script Python que reproduz a tabela e os traços." (mostrar)

**Slide 8 — Análise (50 s)**
> "Sobre computabilidade: provamos que existe ramo aceitante se e somente se `n` é composto,
> então `L(M)` é exatamente `L`. Por Church–Turing, essa MTND tem uma MT **determinística**
> equivalente — o não determinismo não dá mais poder, só deixa a descrição mais simples. E `L`
> é **decidível**, porque todo ramo sempre para. A limitação é de custo: o número de ramos
> cresce com `n`, então simular tudo deterministicamente fica caro."

**Slide 9 — Resumo (20 s)** — fechar e passar para arguição.

## Perguntas prováveis na arguição (e respostas curtas)

- **"Onde está o não determinismo?"**
  Só em `q₂` lendo `1`: duas transições (continuar marcando ou parar). Cada escolha fixa um `a`.

- **"Como garante que `b ≥ 2` (não aceita `n` primo dizendo n = n×1)?"**
  O bloco `A` é a 1ª cópia de `a`; exigimos consumir os `1`s restantes em **≥ 1 bloco** completo.
  Se `a = n`, não sobra `1` para um 2º bloco e o ramo não aceita.

- **"E se a entrada for vazia ou `1`?"**
  `q₀` lendo branco (vazio) ou `q₁` lendo branco (`n=1`) não têm transição → rejeita.

- **"Por que precisa dos símbolos C e D?"**
  `C` marca qual `A` do gabarito está "ativo" no momento; `D` marca os já usados no passe, e são
  restaurados para `A` no fim de cada passe (gabarito reutilizável).

- **"Isso seria diferente numa MT determinística?"**
  Mesma linguagem reconhecida (equivalência). A MTD teria que iterar/testar fatores
  explicitamente; a MTND expressa o "existe fator" diretamente, adivinhando.

- **"Quantos estados/transições?"** 12 estados, 24 transições (acima do mínimo da lauda).

- **"Como a fita evolui num caso aceito?"**
  Mostrar o traço de `1⁶`, a=3 (`rastreamento.md`): `AAA|111` → consome 3 uns (`b=2`) → aceita.

## Checklist da Pessoa 1 antes do seminário
- [ ] `compostos.jff` abre e roda no JFLAP da máquina da apresentação.
- [ ] Print da árvore do `1⁶` salvo em `testes/mtnd-compostos/arvore-1^6.png`.
- [ ] Saber explicar Fase 1 × Fase 2 sem ler o slide.
- [ ] Saber responder as 7 perguntas acima.
- [ ] (Revisão cruzada) saber explicar o SKI da Pessoa 2 em 1 minuto.
