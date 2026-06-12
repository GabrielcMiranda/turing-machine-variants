# Roteiro de apresentação — Pessoa 2 (Combinadores SKI)

Parte do SKI no seminário conjunto. Alvo: **~4 a 5 minutos** de fala + participação na
demonstração. Tempo total da equipe: 12–15 min. Falar com calma; cada slide ≈ 30–45 s.

## Fala por slide

**Slide 1 — Abertura (20 s)**
> "Nossa primeira implementação é sobre λ-cálculo, mas com uma virada: mostramos que dá pra
> computar **sem variáveis**, usando só os combinadores `S` e `K`. Implementamos isso em Python."

**Slide 2 — O problema (45 s)**
> "No λ-cálculo, computar é fazer β-redução: substituir o argumento no corpo da função. O
> problema prático é que isso exige gerenciar o **escopo das variáveis** — separar livres de
> ligadas e evitar **captura de nomes**, o que obriga a implementar α-conversão. É muita
> burocracia de nomes antes de computar."

**Slide 3 — A solução SKI (45 s) — PONTO ALTO**
> "Schönfinkel e Curry mostraram que as variáveis são **dispensáveis**. Tudo se faz com três
> combinadores: `I` é a identidade; `K` guarda o primeiro argumento e descarta o segundo; e `S`
> distribui o terceiro argumento para os dois primeiros. É um sistema **Turing-completo**,
> equivalente ao λ-cálculo, mas **sem nomes**."

**Slide 4 — I = SKK (40 s)**
> "Dá até pra eliminar o `I`. Reduzindo `S K K x`: o `S` distribui o `x`, vira `K x (K x)`, e o
> `K` retorna o primeiro, que é `x`. Ou seja, `S K K` se comporta exatamente como a identidade.
> Então o núcleo do sistema é só **`S` e `K`** — duas constantes."

**Slide 5 — Eliminação de abstração (60 s)**
> "Para converter um λ-termo em SKI puro usamos o algoritmo de *bracket abstraction*, com três
> regras: a abstração da própria variável vira `I`; se a variável não aparece no corpo, vira
> `K` aplicado ao corpo; e se o corpo é uma aplicação, vira `S` distribuindo a abstração nas
> duas partes. No código (`abstracao.py`), `T[λx.x]` dá `I`, `T[λx.y]` dá `K y`, e `T[λx.(x y)]`
> dá `S I (K y)`. A complexidade de nomes some na **tradução**."

**Slide 6 — Ordem normal (40 s)**
> "Nosso redutor usa **ordem normal**: sempre o redex mais externo à esquerda primeiro. Pelo
> teorema de Church-Rosser, se o termo tem forma normal, a ordem normal **garante** encontrá-la
> — diferente da ordem aplicativa, que pode travar num argumento que seria descartado."

**Slide 7 — Demonstração (45 s)**
> "Para o traço longo usamos o numeral de Church **2**, que codificado em `S` e `K` é `S B I`.
> Aplicado a `f` e `x`, ele reduz em **7 passos** para `f (f x)` — ou seja, 'aplique `f` duas
> vezes'. Isso roda com `python demo.py`." (mostrar a saída)

**Slide 8 — Análise (50 s)**
> "Sobre computabilidade: o sistema reescreve termos por puro casamento de padrão, sem ambiente
> de nomes. Não é trivial porque é Turing-completo — e por isso herda o **Problema da Parada**:
> o termo `Ω = S I I (S I I)` se auto-replica e nunca normaliza, daí o limite de passos. SKI,
> λ-cálculo e Máquina de Turing são todos equivalentes (Church-Turing)."

**Slide 9 — Resumo (20 s)** — fechar e passar para a próxima parte.

## Perguntas prováveis na arguição (e respostas curtas)

- **"O que acontece com um termo que não normaliza?"**
  Ele diverge (ex.: `Ω = S I I (S I I)`). O redutor corta no `max_steps` — reflexo direto da
  indecidibilidade do Problema da Parada num sistema Turing-completo.

- **"Por que o `I` é dispensável?"**
  Porque `S K K x →* x`: o `S` duplica o `x`, o `K` descarta a cópia e devolve `x`. Logo
  `S K K` faz o papel da identidade.

- **"Qual a vantagem do SKI sobre implementar o λ-cálculo direto?"**
  Toda a complexidade de escopo/α-conversão é resolvida **na tradução** (bracket abstraction).
  O motor de execução fica simples: só casamento de padrão estrutural, sem tabela de símbolos.

- **"O que é ordem normal e por que vocês a escolheram?"**
  Reduzir o redex mais externo à esquerda primeiro. Por Church-Rosser, garante achar a forma
  normal quando ela existe; a ordem aplicativa pode divergir desnecessariamente.

- **"O que cada combinador faz?"**
  `I x → x`; `K x y → x`; `S x y z → x z (y z)`. `S` é o único que duplica/distribui argumento.

- **"Como sei que a tradução λ→SKI está correta?"**
  No rastreamento, cada conversão é **verificada por redução**: aplicamos o resultado a um
  argumento e conferimos que reproduz o corpo original (`T[λx.(x y)] = S I (K y)`, e `S I (K y) a →* a y`).

## Checklist da Pessoa 2 antes do seminário
- [ ] `python implementacoes/lambda-ski/test_ski.py` passa (4/4) na máquina da apresentação.
- [ ] `python implementacoes/lambda-ski/demo.py` mostra o traço de 7 passos.
- [ ] Saber explicar as 3 regras de `S`/`K`/`I` e por que `I = SKK`.
- [ ] Saber explicar *bracket abstraction* (as 3 regras) sem ler o slide.
- [ ] (Revisão cruzada) saber explicar a MTND da Pessoa 1 em 1 minuto.
