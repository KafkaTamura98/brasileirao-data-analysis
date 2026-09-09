# ⚽ O Peso do Mando de Campo no Brasileirão (2003-2023)

Este é um projeto ponta a ponta de **Engenharia e Análise de Dados** focado em investigar matematicamente o peso da torcida e do mando de campo na era dos pontos corridos do Campeonato Brasileiro. 

O objetivo principal foi responder a perguntas reais com dados empíricos: a vantagem de jogar em casa é um mito? A ausência de público na pandemia alterou a estatística? Quem foram os visitantes mais mortais da história?

## 📊 Principais Descobertas (Insights)

Através da ingestão de mais de duas décadas de dados e análises com SQL e Python, descobrimos que:

1. **O Efeito Pandemia (2020-2021):** Historicamente, os mandantes vencem cerca de 50% dos jogos. Durante a pandemia de Covid-19 (com estádios vazios), a taxa de vitória dos mandantes despencou drasticamente, provando matematicamente que a torcida atua como o "12º jogador".
2. **A Anomalia de 2017:** Identificamos uma queda brusca de vitórias de mandantes em 2017. Usando consultas SQL avançadas (CTEs), descobrimos que a média histórica de um time jogando fora de casa é de apenas **4.7 vitórias** por campeonato. O Corinthians de 2017 conseguiu **9 vitórias**, vencendo **1.9x mais** que o normal e distorcendo a curva do campeonato.

## 🏗️ Arquitetura e Pipeline de Dados (ETL)

O projeto foi estruturado simulando um pipeline clássico de dados:

* **Extração (Extract):** Consumo automatizado de uma base de dados pública com o histórico completo de partidas via Python.
* **Transformação (Transform):** Limpeza dos dados, remoção de colunas irrelevantes e aplicação de regras de negócio (criação da coluna `vencedor` baseada nos placares) utilizando **Pandas**.
* **Carga (Load):** Criação e inserção dos dados limpos em um banco de dados relacional **SQLite** (`brasileirao.db`).
* **Análise (Analisys/EDA):** Consumo do banco de dados utilizando consultas **SQL** e renderização do *Data Storytelling* visual com **Matplotlib** e **Seaborn**.

## 💻 Tecnologias Utilizadas

* **Linguagem:** Python
* **Manipulação de Dados:** Pandas
* **Banco de Dados:** SQLite (SQL Padrão)
* **Visualização:** Seaborn e Matplotlib
* **Versionamento:** Git e GitHub
