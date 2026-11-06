# 🏳️‍🌈 Cinclu - Cidade Inclusiva

> Assistente de terminal, escrito em Python, que orienta pessoas LGBTQIA+ sobre **saúde, direitos, documentos e denúncia**, sempre com **fonte oficial**, **data de verificação** e **sem coletar dados pessoais**.

⚠️ **Aviso:** este assistente **NÃO é um canal oficial**. Ele reúne orientações de fontes oficiais, mas não substitui atendimento jurídico, médico ou psicológico.

---

## 👥 Integrantes

| Nome | RM |
|---|---|
| Enzo Posterlli Strinta | 570035 |
| Giovanna Tristão Lopes | 572552 |
| Leonardo Robert Maulicino | 570329 |

---

## 🎯 Público e problema escolhidos

**Público atendido:** pessoas LGBTQIA+ (e quem convive com elas) que precisam de orientação prática.

**Problema:** quem precisa denunciar uma violência, mudar o nome nos documentos, saber como acessar PrEP/PEP ou procurar apoio emocional encontra a informação espalhada, em linguagem técnica e misturada com sites que parecem oficiais e não são. Em temas sensíveis como esses, a pessoa muitas vezes tem medo de se expor e desiste de procurar ajuda.

**Solução:** o Cinclu responde dúvidas em texto livre ou por navegação em categorias, usando **apenas** uma base de conhecimento verificada. Ele nunca pede nome, CPF, telefone ou e-mail, e recusa mensagens que contenham esses dados.

---

## 🌍 ODS relacionados

| ODS | Como o projeto se relaciona |
|---|---|
| **ODS 3 – Saúde e Bem-Estar** 💙 | Orienta sobre PrEP, PEP, teste de HIV, saúde de pessoas trans no SUS e apoio emocional (CVV 188). |
| **ODS 10 – Redução das Desigualdades** ⚖️ | Informa direitos que reduzem a exclusão: retificação de nome e gênero, nome social, casamento e denúncia de discriminação. |
| **ODS 11 – Cidades e Comunidades Sustentáveis** 🏙️ | Ajuda a tornar a cidade mais inclusiva e segura, ao facilitar o acesso a serviços públicos e canais de denúncia. |

---

## ✨ Funcionalidades

- 📚 Carrega a base de conhecimento de um arquivo **JSON**.
- 🧱 Sistema organizado em **3 classes** com atributos e métodos (`Orientacao`, `BaseConhecimento`, `Assistente`).
- 🔎 **Busca com pontuação** em texto livre, com nível de confiança (ALTA/MÉDIA) ou "não encontrei".
- 🗂️ **Navegação por categorias**, com "0 para voltar" em todas as telas.
- 🛡️ **Entradas inválidas** tratadas e **dados pessoais bloqueados** (não são registrados).
- 💬 **Acolhimento emocional:** mensagens com sinais de sofrimento mostram o contato do CVV, e o texto digitado **não é gravado**.
- 📝 **Histórico** em `data/historico.json`, **indicadores** e **exportação para CSV**.
- 🔐 Toda resposta mostra **fonte**, **data de verificação** e o aviso de que o assistente não é canal oficial.
- 🧯 Arquivos JSON ausentes ou corrompidos **não travam** o programa.

---

## 📁 Estrutura do repositório

```
citizen-assist-ai/
├── README.md
├── main.py                  # ponto de entrada
├── orientacao.py            # classe Orientacao
├── base_conhecimento.py     # classe BaseConhecimento (normalizar, pontuar, buscar)
├── assistente.py            # classe Assistente (atendimento, histórico, indicadores, CSV)
└── data/
    ├── base_conhecimento.json   # 11 orientações verificadas
    ├── historico.json           # atendimentos registrados
    ├── atendimentos.csv         # gerado pela opção 4 do menu
    └── avaliacoes.json          # notas de facilidade de uso (1 a 5), gerado ao sair
```

---

## ▶️ Como executar

Requisitos: **Python 3.8 ou superior**. Não há bibliotecas externas.
Baixe **todos** os arquivos e a pasta. Depois execute **main.py**.

**Atenção:** para melhor experiência no Cinclu não altere nomes de arquivos ou pastas

Menu principal:

```
1. Digitar minha dúvida
2. Navegar por categorias
3. Ver indicadores
4. Exportar atendimentos para CSV
0. Sair   (pede uma nota de facilidade de 1 a 5)
```

---

## 🧩 Classes e composição

```
Assistente
 └── base: BaseConhecimento
      └── orientacoes: [Orientacao, Orientacao, Orientacao, ...]
```

| Classe | O que representa | Atributos | Métodos principais |
|---|---|---|---|
| `Orientacao` | Um registro do JSON | id, categoria, titulo, palavras_chave, resposta, documentos, onde, fonte, verificado_em | `exibir()` |
| `BaseConhecimento` | O conjunto de todas as orientações | caminho, orientacoes | `carregar()`, `categorias()`, `por_categoria()`, `pontuar()`, `buscar()` |
| `Assistente` | Quem conversa com o cidadão | nome, base, historico | `perguntar()`, `navegar()`, `registrar()`, `indicadores()`, `exportar_csv()` |

---

## 📚 Base de conhecimento

Arquivo `data/base_conhecimento.json`: lista de dicionários, um por orientação, com os campos `id`, `categoria`, `titulo`, `palavras_chave`, `resposta`, `documentos`, `onde`, `fonte` e `verificado_em`.

São **11 orientações**, **4 categorias** e de 9 a 18 palavras-chave por orientação.

| ID | Categoria | Orientação |
|---|---|---|
| 1 | Denúncia e Proteção | Denunciar violência ou discriminação (Disque 100) |
| 2 | Denúncia e Proteção | LGBTfobia é crime? Como registrar uma ocorrência |
| 3 | Documentos e Direitos | Mudar nome e gênero nos documentos (retificação em cartório) |
| 4 | Documentos e Direitos | Usar o nome social em órgãos públicos federais |
| 5 | Documentos e Direitos | Usar o nome social na Justiça |
| 6 | Documentos e Direitos | Casamento e união estável entre pessoas do mesmo sexo |
| 7 | Saúde | PrEP: prevenção ao HIV antes da exposição |
| 8 | Saúde | PEP: atendimento de urgência após risco de HIV |
| 9 | Saúde | Fazer teste de HIV e autoteste |
| 10 | Saúde | Saúde de pessoas trans no SUS (Processo Transexualizador) |
| 11 | Apoio Emocional | Apoio emocional gratuito 24 horas (CVV 188) |

📌 O assistente só responde com o que está na base. Quando a equipe não foi encontrada uma lista oficial de documentos, o campo diz isso (por exemplo, "confirme na unidade de saúde").

---

## 🧮 Regra de pontuação usada

### 1. Normalização
Pergunta, palavras-chave e título são comparados **em minúsculas, sem acentos e sem pontuação** (`normalizar()`).

### 2. Pontos

| Regra | Resultado |
|---|---|
| Palavra-chave da orientação que aparece na pergunta | **+3 pontos** |
| Palavra da pergunta (4 letras ou mais) que aparece no título | **+1 ponto** |
| Melhor orientação com **6 pontos ou mais** | Confiança **ALTA** |
| Melhor orientação com **3 a 5 pontos** | Confiança **MÉDIA** |
| Nenhuma orientação com 3 pontos | "Não encontrei": sugere outras palavras e mostra as categorias |

`buscar()` devolve uma **lista de tuplas** `(pontos, orientacao)`, da maior para a menor pontuação. O assistente mostra a melhor orientação e **até duas alternativas**.

### 3. Exemplo real
Pergunta: **"Como denunciar homofobia?"**

| Item | Pontos |
|---|---|
| palavra-chave `denunciar` | +3 |
| palavra-chave `homofobia` | +3 |
| "denunciar" aparece no título da orientação 1 | +1 |
| **Total** | **7 → confiança ALTA** |

### 4. Ajustes
- **Palavras ignoradas no título:** palavras comuns com 4 ou mais letras, como *como*, *para*, *quero*, *posso* (lista `IGNORAR_NO_TITULO`), **não** valem o +1 do título. Sem isso, "Como conseguir PrEP?" ganhava ponto à toa em orientações sem relação, por causa do "Como" no título.
- **Sem pontos repetidos:** se uma palavra aparece duas vezes na pergunta, ela conta uma vez só.
- **Pontuação extra removida:** além da pontuação sugerida, a normalização também remove aspas, barra e o sinal `+` (para "LGBTQIA+").

---

## 🛡️ Regras de atendimento

- **Navegação:** categorias e orientações numeradas, com "0 para voltar" em todas as telas.
- **Entradas inválidas:** opção fora da faixa, letras, resposta vazia e s/n inválido repetem a pergunta e nunca encerram o programa.
- **Dados pessoais:** o assistente nunca pede nome, CPF, telefone ou e-mail. Mensagem com **8 ou mais dígitos** ou com **@** é recusada e **não é registrada**.
- **Transparência:** toda resposta mostra fonte, data de verificação e o aviso "este assistente NÃO é um canal oficial".
- **Arquivos:** base ausente ou corrompida mostra um aviso e encerra com mensagem clara; histórico ou avaliações corrompidos viram uma lista vazia.
- **Cuidado emocional:** mensagens com sinais de sofrimento recebem uma mensagem de acolhimento e o contato do CVV. O texto **não é gravado** no histórico.

---

## 📊 Histórico, indicadores e CSV

Cada atendimento é salvo em `data/historico.json` com: `data`, `origem` (pergunta ou categoria), `pergunta`, `id_orientacao`, `encontrou`, `ajudou`, `tentativas` e `tempo_segundos`.

**Definição de atendimento:** começa quando a pessoa abre o campo de dúvida e termina quando ela diz que a orientação ajudou, desiste (0) ou decide não reescrever. Cada pergunta digitada conta como uma tentativa. O tempo é medido com `time.time()` até o momento em que a orientação é encontrada.

**Indicadores exibidos (opção 3):**

- ✅ Resposta encontrada (%)
- 👍 Taxa de acerto: ajudou (%)
- ⏱️ Tempo médio para encontrar
- 🔁 Tentativas por atendimento
- ⭐ Facilidade de uso (1 a 5), média das notas dadas ao sair
- ❓ Lista de dúvidas sem solução

**Exportação (opção 4):** os atendimentos vão para `data/atendimentos.csv` com `csv.DictWriter`.

---

## 🔗 Integrações com outras disciplinas

Nesta versão **não há integrações** com outras disciplinas da GS.

---

## 🧪 Resultado do teste com usuários

> 📝 **A PREENCHER depois dos testes.** Mínimo exigido: 3 pessoas de fora da equipe e 10 atendimentos. Não registrar nomes nem dados dessas pessoas.

| Item | Resultado |
|---|---|
| Pessoas que testaram | _preencher_ |
| Total de atendimentos | _preencher_ |
| Resposta encontrada (%) | _preencher_ |
| Taxa de acerto: ajudou (%) | _preencher_ |
| Tempo médio para encontrar | _preencher_ |
| Tentativas por atendimento | _preencher_ |
| Facilidade de uso (1 a 5) | _preencher_ |

**Dúvidas sem solução:**
- _preencher com a lista que o programa mostra na opção 3_

**Melhoria feita a partir do teste:**
- _preencher (exemplo: nova palavra-chave adicionada à orientação X porque a pergunta "..." não era encontrada)_

---

## 📖 Fontes consultadas

Todas as orientações foram conferidas nas fontes abaixo. Data de verificação registrada na base: **2026-11-06**.

| Assunto | Fonte |
|---|---|
| Disque 100 | https://www.gov.br/mdh/pt-br/acesso-a-informacao/disque-100 |
| LGBTfobia como crime (STF, ADO 26 e MI 4733) | https://portal.stf.jus.br/noticias/vernoticiadetalhe.asp?idconteudo=414010 |
| Retificação de nome e gênero (CNJ) | https://www.cnj.jus.br/cnj-servico-como-fazer-a-troca-de-nome-e-genero-em-cartorios/ |
| Nome social na administração federal (Decreto 8.727/2016) | https://www2.camara.leg.br/legin/fed/decret/2016/decreto-8727-28-abril-2016-782951-norma-pe.html |
| Nome social na Justiça (Resolução CNJ 270/2018) | https://atos.cnj.jus.br/files/compilado14054320250612684adeb7131f0.pdf |
| Casamento entre pessoas do mesmo sexo (Resolução CNJ 175/2013) | https://atos.cnj.jus.br/atos/detalhar/1754 |
| PrEP (Ministério da Saúde) | https://www.gov.br/saude/pt-br/assuntos/pcdt/p/profilaxia-pre-exposicao-prep-oral-a-infeccao-pelo-hiv |
| PEP e teste de HIV (Ministério da Saúde) | https://www.gov.br/saude/pt-br/campanhas-da-saude/2022/hiv-aids/acesse-as-pecas/flyer.pdf |
| Processo Transexualizador (Portaria GM/MS 2.803/2013) | https://bvsms.saude.gov.br/bvs/saudelegis/gm/2013/prt2803_19_11_2013.html |
| Apoio emocional (CVV 188) | https://cvv.org.br |

---

## 🚧 Limitações

- 🔤 **Busca por regras:** o assistente entende apenas as palavras-chave cadastradas. Erros de digitação (como "prepp"), gírias e sinônimos não cadastrados podem resultar em "não encontrei". A solução é ampliar as palavras-chave a partir dos testes.
- 📦 **Cobertura pequena:** são 11 orientações. Assuntos como educação, trabalho, doação de sangue, violência doméstica e adoção ainda não estão na base.
- 🗺️ **Informação nacional:** a base traz regras federais. Serviços locais (delegacias especializadas, ambulatórios trans de cada cidade, defensorias) variam por região e **não** estão cadastrados.
- 📄 **Documentos genéricos:** em alguns casos não encontramos lista oficial de documentos. O campo orienta a confirmar no serviço, em vez de inventar.
- 🕒 **Informação pode mudar:** leis, portarias e serviços mudam. Cada resposta mostra a data em que a equipe conferiu, e a base precisa ser revisada periodicamente.
- ⚖️ **Não é aconselhamento profissional:** o assistente não faz diagnóstico, não dá parecer jurídico e não substitui atendimento de saúde.
- 💻 **Só terminal e só português:** não há interface gráfica nem outros idiomas.
- 🆘 **Detecção de sofrimento é simples:** é feita por trechos de texto e pode não reconhecer todas as formas de pedir ajuda. O assistente **não substitui** um serviço de emergência.

---

## 🎥 Vídeo técnico

🔗 **Link (YouTube, não listado):** _preencher_

---

💜 *Cinclu: informação confiável para uma cidade mais inclusiva.*
