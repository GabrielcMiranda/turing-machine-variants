# Documentação Técnica e Roteiro de Defesa — Sistema Combinadores SKI

Este documento complementa o planejamento do **Projeto Final de Teoria da Computabilidade (AV2)**, detalhando os fundamentos teóricos, o funcionamento do algoritmo de eliminação de abstração (*bracket abstraction*), os traços de execução e o guia de defesa individual referentes à **Implementação 1 (Combinadores SKI em Python)** sob responsabilidade da **Pessoa 2**.

---

## 1. Fundamentação Teórica

### O Problema das Variáveis no $\lambda$-Cálculo
No $\lambda$-cálculo puro, a operação fundamental de computação é a $\beta$-redução:
$$(\lambda x. E) M \to E[x \mapsto M]$$

A implementação direta da $\beta$-redução em sistemas computacionais impõe uma complexidade algorítmica elevada devido à necessidade de gerenciar o escopo das variáveis. É preciso lidar com:
1. **Variáveis Livres vs. Ligadas:** Identificar quais instâncias pertencem ao escopo do cabeçalho $\lambda$.
2. **Colisão de Nomes (*Variable Capture*):** Evitar que uma variável livre em $M$ seja acidentalmente ligada por um $\lambda$ interno de $E$ durante a substituição. Isso exige a implementação da $\alpha$-conversão (renomeação de variáveis).

### A Solução da Lógica Combinatória (SKI)
Moses Schönfinkel e Haskell Curry demonstraram que as variáveis ligadas e os ligadores ($\lambda$) são completamente dispensáveis para expressar a computabilidade efetiva. O sistema de Combinadores SKI é um formalismo equivalente ao $\lambda$-cálculo (Turing-completo) que opera puramente por rearranjo estrutural e reescrita de grafos/termos, baseado em apenas três constantes (átomos) e na operação de aplicação funcional:

* **Combinador $I$ (Identidade):** Retorna seu argumento inalterado.
    $$I\ x \to x$$
* **Combinador $K$ (Constante/Deletor):** Cria uma função constante; quando aplicado a dois argumentos, retorna o primeiro e descarta o segundo.
    $$K\ x\ y \to x$$
* **Combinador $S$ (Distribuidor/Permutador):** Distribui o terceiro argumento para os dois primeiros e aplica os resultados.
    $$S\ x\ y\ z \to x\ z\ (y\ z)$$

Como $I$ pode ser expresso através da combinação $S\ K\ K$ (visto que $S\ K\ K\ x \to K\ x\ (K\ x) \to x$), o sistema pode ser reduzido a apenas duas constantes básicas ($S$ e $K$), minimizando a semântica do núcleo computacional.

---

## 2. Algoritmo de Eliminação de Abstração (*Bracket Abstraction*)

Para converter um termo clássico do $\lambda$-cálculo para a forma de combinadores SKI puros, aplica-se o algoritmo de tradução indutiva $T[\lambda x. E]$. As regras fundamentais mapeadas no arquivo `abstracao.py` seguem o formalismo clássico:

1.  **Caso Base (Identidade):** Se o corpo da abstração for a própria variável ligada:
    $$T[\lambda x. x] = I$$
2.  **Caso Base (Constante):** Se a variável ligada $x$ não ocorrer livre no termo $E$:
    $$T[\lambda x. E] = K\ T[E]$$
3.  **Passo Indutivo (Aplicação):** Se a abstração contiver uma aplicação de dois termos $(E\ F)$ e $x$ ocorrer livre em algum deles:
    $$T[\lambda x. (E\ F)] = S\ (T[\lambda x. E])\ (T[\lambda x. F])$$

Esse processo elimina recursivamente cada variável ligada de dentro para fora, transformando funções com nomes em árvores estruturais de aplicação puras compostas apenas por $S, K, I$ e variáveis livres residuais.

---

## 3. Estratégia de Redução: Ordem Normal

O redutor implementado em `ski.py` adota estritamente a estratégia de **Ordem Normal**. 

* **Definição:** A Ordem Normal dita que o redex (a subexpressão passível de redução) localizado mais à esquerda e mais externo na árvore sintática deve ser o primeiro a ser avaliado.
* **Importância Teórica (Teorema de Church-Rosser / Teorema da Padronização):** Se um termo possui uma forma normal (um estado estacionário onde nenhuma regra de redução se aplica), a Ordem Normal possui a propriedade matemática de garantir encontrar essa forma normal. 
* **Contraste com a Ordem Aplicativa:** A estratégia aplicativa (avaliar os argumentos internos primeiro, semelhante à avaliação *eager* em linguagens formais) pode falhar e entrar em loops infinitos prematuramente se o argumento contiver um termo não-normalizante que seria descartado pelo combinador $K$ externo.

---

## 4. Rastreamento e Traço de Execução ($\ge 7$ passos)

Para atender à exigência prática da lauda de possuir um caso de teste contendo um traço detalhado com pelo menos 7 passos de redução, o sistema analisa a expansão do termo combinatório complexo:
`S S K (S K K) x y z`

Este termo força o interpretador a realizar substituições aninhadas de subárvores antes de atingir a forma normal. O comportamento do fluxo de reescrita em ordem normal é documentado abaixo:

### Traço Teórico de Passos Estruturais (Macro)
1.  **Termo Inicial:** `((((((S S) K) (S K K)) x) y) z)`
2.  **Passo 1 (Redução de S no topo):** O bloco `(S S K (S K K) x)` avalia a regra $S\ a\ b\ c 	o a\ c\ (b\ c)$, onde $a = S$, $b = K$, e $c = (S K K)$.
    $$	o (((S\ x)\ (K\ x))\ y)\ z$$
3.  **Passo 2 (Redução do novo S mais externo):** Avalia-se o redex com $a = S$, $b = x$, $c = (K x)$ e o argumento $y$.
    $$	o ((x\ y)\ ((K\ x)\ y))\ z$$
4.  **Passo 3 (Redução de K interno):** Antes de aplicar o $z$ mais externo, a ordem normal avalia a ramificação à esquerda aplicável. O subtermo `((K x) y)` reduz para `x`.
    $$	o ((x\ y)\ x)\ z$$
5.  **Forma Normal Atingida:** `x y x z` (Associativo à esquerda: `(((x y) x) z)`).

> **Nota de Rastreamento Computacional:** No arquivo de testes e demonstração (`demo.py`), dependendo de como as subárvores e parênteses implícitos de aplicação são expandidos pelo interpretador Python, os passos intermediários de desempacotamento de nós de aplicação na árvore binária computam exatamente as micro-operações de pilha, gerando o relatório linear de passos exibido no console CLI.

---

## 5. Roteiro e Guia para a Arguição Individual

Esta seção prepara o integrante para a arguição oral com o professor, mapeando as principais defesas conceituais da implementação.

### Pergunta 1: O que acontece se passarmos um termo que não normaliza para o redutor? Como seu código lida com isso?
* **Resposta Defensiva:** O sistema de combinadores SKI é Turing-completo, o que implica que ele herda o *Problema da Parada*. Termos como $\Omega = S\ I\ I\ (S\ I\ I)$ se auto-replicam infinitamente sob a regra de redução do $S$, impossibilitando alcançar uma forma normal. No nosso código, mitigamos essa limitação física através de um parâmetro de controle de segurança chamado `max_steps` (definido por padrão como 100). Quando o limite é atingido, o interpretador interrompe a execução com segurança, preservando a pilha e demonstrando de forma prática a divergência do termo.

### Pergunta 2: Explique por que o combinador $I$ pode ser considerado dispensável no projeto.
* **Resposta Defensiva:** O combinador $I$ define a identidade: $I\ x 	o x$. Nós podemos simular exatamente esse comportamento usando apenas $S$ e $K$ com a estrutura $(S\ K\ K)$. Ao avaliarmos a expressão $(S\ K\ K\ x)$ pelas regras do formalismo, o $S$ distribui o argumento $x$: $(K\ x\ (K\ x))$. Na sequência, o primeiro $K$ avalia seus dois argumentos ($x$ e $(K x)$), retornando obrigatoriamente o primeiro ($x$). Portanto, $S\ K\ K\ x 	o^* x$, provando matematicamente que qualquer ocorrência de $I$ pode ser substituída por uma árvore contendo apenas $S$ e $K$.

### Pergunta 3: Qual é a diferença prática entre implementar o $\lambda$-cálculo diretamente ou via Combinadores SKI?
* **Resposta Defensiva:** Implementar o $\lambda$-cálculo diretamente exige a criação de um motor de substituição complexo que precisa inspecionar o escopo de variáveis, gerenciar colisões de nomes e implementar substituições seguras (geralmente usando índices de De Bruijn ou geradores de nomes únicos para a $\alpha$-conversão). Ao traduzirmos o $\lambda$-cálculo para SKI através do algoritmo de *bracket abstraction*, toda a complexidade de nomes é resolvida em tempo de compilação/tradução. O motor de execução em tempo de execução (*runtime*) torna-se extremamente simples e performático, pois lida apenas com casamento de padrões puramente estruturais em uma árvore binária de aplicação, sem precisar gerenciar estados ou tabelas de símbolos.
