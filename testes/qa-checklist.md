# QA final — checklist da entrega (Pessoa 3)

Relatório de verificação de ponta a ponta, mapeado à lauda (Seções 7, 12 e 16). Gerado após
dry-run de reprodutibilidade a partir da raiz do repositório.

## 1. Dry-run de reprodutibilidade ("seguir só o README")

Todos os comandos do README foram executados a partir da raiz e conferidos:

| Comando | Resultado | Status |
|---------|-----------|--------|
| `python implementacoes/lambda-ski/test_ski.py` | `Ran 4 tests ... OK` | ✅ 4/4 |
| `python implementacoes/lambda-ski/demo.py` | exemplo 3 (Church 2) = **7 passos** → `f (f x)` | ✅ |
| `python testes/lambda-ski/rastreamento.py` | `TODOS OS CASOS BATEM` + 3 conversões `[OK]` | ✅ |
| `python testes/mtnd-compostos/rastreamento.py` | tabela + traços + árvore do `1⁶` impressos | ✅ |
| `python implementacoes/mtnd-compostos/_verifica.py` | `TODOS OS CASOS PASSARAM` (18 casos) | ✅ |

> **MTND no JFLAP:** o arquivo `compostos.jff` não pôde ser aberto neste ambiente (GUI/Java). A
> evidência reproduzível é dada pelo oráculo Python (`_verifica.py` + `rastreamento.py`), que usa
> a mesma relação δ. Na apresentação, abrir o `.jff` no JFLAP (Multiple Run / Step Run).

## 2. Verificação estrutural

- **Links internos do README:** 9/9 resolvem para arquivos existentes. ✅
- **Higiene do Git:** nenhum `__pycache__`, `.pyc` ou `.html` rastreado (`.gitignore` ativo). ✅
- **Árvore do README:** reflete o repositório real. ✅

## 3. Checklist da lauda — Seção 16

| Item | Status | Evidência / observação |
|------|--------|------------------------|
| Tema, turma e integrantes identificados | ⚠️ | integrantes e tema OK; **turma é placeholder** |
| Link do repo no Classroom, acessível | ⚠️ | ação humana (fora do repo); **URL placeholder no README** |
| GitHub com README, slides, implementações, testes, rastreamentos, referências, uso_ia | ✅ | todos presentes |
| Equipe ≤ 4 escolheu exatamente 2 modelos distintos | ✅ | SKI + MTND |
| Implementação própria, bem elaborada e reproduzível por modelo | ✅ | dry-run verde |
| Cada implementação resolve problema diferente | ✅ | redução de termos × reconhecimento de linguagem |
| Cada máquina > 8 estados (quando aplicável) | ✅ | MTND: 12 estados |
| Testes, rastreamento e interpretação por implementação | ✅ | `testes/lambda-ski/`, `testes/mtnd-compostos/` |
| `.jff` e/ou códigos entregues corretamente | ✅ | `compostos.jff` + Python |
| README permite executar os exemplos | ✅ | confirmado no dry-run |
| Referências citadas | ✅ | `referencias.md` |
| Uso de IA declarado | ✅ | `uso_ia.md` |
| Todos conseguem explicar teoria/impl/resultados | ⚠️ | ação humana; roteiros prontos (`slides/roteiro-*.md`) |

## 4. Requisitos de complexidade — Seção 7

| Requisito | Exigido | Entregue | Status |
|-----------|---------|----------|--------|
| MTND — estados | > 8 | 12 | ✅ |
| MTND — transições relevantes | ≥ 10 | 24 | ✅ |
| λ-Cálculo — passos de redução | ≥ 7 | 7 (numeral de Church 2) | ✅ |
| Testes por implementação (aceito/rejeitado/fronteira) | ≥ 3 | SKI: 5 casos · MTND: 18 casos | ✅ |

## 5. Rubrica — Seção 12 (2,0 pts)

| Critério | Peso | Situação |
|----------|------|----------|
| 1. Domínio conceitual e arguição | 0,45 | Material pronto (docs + roteiros); ⚠️ depende do preparo individual |
| 2. Formalização dos modelos | 0,30 | ✅ `formalizacao.md`, `documentacao_ski.md` |
| 3. Implementações e funcionamento | 0,35 | ✅ dry-run verde |
| 4. Complexidade, originalidade e testes | 0,30 | ✅ 12/24, 7 passos, problemas distintos, testes |
| 5. Seminário, organização e participação | 0,20 | ✅ deck + divisão de fala; ⚠️ ensaiar tempo |
| 6. GitHub, entrega, documentação, rastreabilidade | 0,40 | ✅ estrutura/reprodutibilidade; ⚠️ entrega no Classroom |

## 6. Pendências que dependem da equipe (ação humana)

1. **Turma** — preencher em `README.md` (linha 6) e `slides/apresentacao.md` (capa).
2. **URL do GitHub** — preencher em `README.md` e entregar o link no Google Classroom.
3. **`testes/mtnd-compostos/arvore-1^6.png`** — print da árvore de ramos do `1⁶` no JFLAP
   (mencionado no `rastreamento.md` e no roteiro da MTND; ainda **não existe**). Evidência visual.
4. **Deck em PDF/PPTX** — exportar `slides/apresentacao.md` (Marp → PDF/PPTX) e versionar no repo
   ou disponibilizar link identificável.
5. **Referências complementares** — confirmar em `referencias.md` quais foram de fato consultadas.
6. **Ensaio do seminário** — cronometrar 12–15 min e revisão cruzada (cada um sabe as duas máquinas).

## 7. Conclusão

A entrega está **tecnicamente completa e reproduzível**: as duas implementações rodam do zero
seguindo o README, os requisitos de complexidade e de rastreamento da lauda estão atendidos, e a
documentação/estrutura cobre todos os itens obrigatórios. Restam apenas pendências de
preenchimento (turma, URL), uma evidência visual opcional (print da árvore) e o preparo
presencial (export do deck + ensaio).
