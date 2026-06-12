# Roteiro de teoria transversal — Pessoa 3 (integração / defesa)

Cobre a abertura teórica e a análise transversal do deck integrado (`apresentacao.md`), além de
preparar a equipe para perguntas que **cruzam os dois modelos**. A arguição é individual: este
roteiro é o "fio condutor" que liga SKI e MTND.

> Divisão de fala: **João Ricardo** apresenta a abertura teórica (Church-Turing) e o
> encerramento; **Yago** apresenta a seção de análise transversal (determinismo × não
> determinismo, λ ↔ combinadores). Ambos usam este roteiro como base.

## Fala por seção do deck integrado

**Capa + Agenda (40 s)**
> "Boa tarde. Nosso trabalho cobre dois modelos de computação — o λ-cálculo via combinadores SKI
> e uma Máquina de Turing não determinística — resolvendo problemas bem diferentes. Vamos da
> teoria à demonstração e fechamos com uma análise que liga os dois."

**Teoria — o que é computar (60 s)**
> "A pergunta de fundo da disciplina é: o que significa um problema ser **computável**? Vários
> formalismos tentaram capturar a noção de algoritmo — Máquina de Turing, λ-cálculo,
> combinadores, funções recursivas, Máquina de Post. A **Hipótese de Church-Turing** diz que
> todos definem **a mesma** classe de funções computáveis. É exatamente o que nossos dois
> modelos ilustram: são muito diferentes na forma, mas equivalentes em poder."

**Transição para os modelos (15 s)**
> "Começamos pelo λ-cálculo, mostrando que dá pra computar até sem variáveis." (passa para Gabriel)

**Análise transversal — determinismo × não determinismo (50 s)**
> "Comparando os dois: a MTND **adivinha** o fator e aceita se algum ramo fecha — mas, por
> Church-Turing, existe uma Máquina de Turing **determinística** equivalente, que simula a
> árvore por busca. Ou seja, o não determinismo **não dá mais poder**, só deixa a descrição mais
> simples. Já o SKI é **determinístico**: a ordem normal define o próximo passo de forma única,
> e por Church-Rosser a forma normal, quando existe, é única."

**Análise transversal — λ ↔ combinadores (40 s)**
> "E os dois modelos se conectam diretamente: λ-cálculo, SKI e Máquina de Turing são todos
> equivalentes. O algoritmo de *bracket abstraction* que mostramos é uma **tradução
> construtiva** de um modelo para o outro — uma prova prática da equivalência. Os limites também
> aparecem nos dois: o SKI herda o **Problema da Parada** (o `Ω` não normaliza), e na MTND a
> linguagem é decidível, mas o número de ramos cresce com `n`, mostrando que **reconhecer** é
> diferente de reconhecer com **custo** baixo."

**Encerramento (30 s)**
> "Em resumo: dois problemas distintos, dois modelos equivalentes à Máquina de Turing, tudo
> reproduzível pelos scripts e pelo arquivo do JFLAP. Obrigado — abrimos para perguntas."

## Perguntas transversais prováveis (e respostas curtas)

- **"O que é a Hipótese de Church-Turing?"**
  A tese de que todos os modelos razoáveis de computação capturam a mesma classe de funções
  computáveis. Não é um teorema demonstrável (envolve a noção *intuitiva* de algoritmo), mas é
  sustentada pela equivalência entre os modelos.

- **"Os dois modelos têm o mesmo poder computacional?"**
  Sim. SKI ≡ λ-cálculo ≡ Máquina de Turing. A MTND também é equivalente a uma MTD. Diferem em
  **conveniência de descrição** e em **custo**, não em poder.

- **"Qual a diferença entre os dois problemas que vocês resolveram?"**
  O SKI faz **transformação/redução de termos** (computa uma função, reescrevendo); a MTND faz
  **reconhecimento de linguagem** (decide pertinência: `n` é composto?). São problemas de
  naturezas distintas — atende à regra de 'problemas diferentes'.

- **"Não determinismo aumenta o poder da Máquina de Turing?"**
  Não. Aumenta (no máximo) a eficiência/clareza da descrição. Toda MTND tem uma MTD equivalente.
  (Diferente da questão P × NP, que é sobre **tempo**, não sobre **o que** é computável.)

- **"Onde aparecem os limites da computação no trabalho?"**
  No SKI, o Problema da Parada: `Ω = S I I (S I I)` nunca normaliza, por isso o limite de passos.
  Na MTND, a explosão de ramos com `n` — a linguagem é decidível, mas simular o não determinismo
  deterministicamente é custoso.

- **"Por que escolher SKI em vez de implementar o λ-cálculo direto?"**
  Porque o SKI evidencia a **eliminação de variáveis**: toda a complexidade de escopo é resolvida
  na tradução, e a execução fica reduzida a reescrita estrutural. É um recorte conceitual mais
  forte do que repetir β-redução com α-conversão.

## Checklist da Pessoa 3 antes do seminário
- [ ] Deck `apresentacao.md` exportado para PDF/PPTX e testado no projetor.
- [ ] Tempo total ensaiado em **12–15 min** (3' teoria, 6' demo, 3' análise).
- [ ] Cada integrante sabe sua seção **e** consegue explicar a do outro (revisão cruzada).
- [ ] Saber explicar Church-Turing, det × não-det e a equivalência λ↔SKI sem ler o slide.
- [ ] Backups das demos (saída do `demo.py` e print da árvore do `1⁶`) prontos caso falhe ao vivo.
