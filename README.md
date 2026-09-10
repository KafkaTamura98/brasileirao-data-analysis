# ⚽ Análise do Mando de Campo no Brasileirão

Um dashboard interativo feito em Python para analisar o histórico de vitórias dos times mandantes no Campeonato Brasileiro. 

O grande objetivo deste projeto é provar, com dados, que **as médias gerais de um campeonato muitas vezes escondem realidades individuais**. Para isso, criei um painel onde é possível comparar o comportamento geral da liga com o desempenho específico de cada clube.

## 📊 Principais Insights da Análise

* **O Outlier de 2012 (São Paulo):** Em 2012, a média de vitórias dos mandantes na liga foi baixíssima (cerca de **40%**). Olhando o gráfico geral, a conclusão seria que jogar em casa não foi vantagem. Mas ao filtrar o **São Paulo**, vemos que o clube teve quase **80% de aproveitamento** em casa.
* **O Efeito Manada (Cruzeiro 2008 vs. 2014):** O Cruzeiro teve o mesmo desempenho absurdo nesses dois anos (**15 vitórias** em casa). Porém, em 2008, o gráfico nacional subiu porque vários outros clubes também foram fortes. Em 2014, o Cruzeiro foi um caso isolado, provando que um time não move a média do campeonato inteiro.
* **Efeito Pandemia:** Sem torcida (2020-2021), a taxa média de vitória dos mandantes despencou de **50%** para **43%**.
* **O Visitante Letal (Corinthians 2017):** A média histórica de vitórias de um time visitante é de 4.7 jogos. O Corinthians de 2017 quebrou essa estatística vencendo 9 jogos fora de casa. Ao roubar tantos pontos dos mandantes, ele ajudou a puxar o gráfico geral daquele ano para baixo, mostrando o impacto de uma anomalia visitante.

## 🛠️ Desafios Técnicos Resolvidos

Durante a construção do projeto, lidei com alguns problemas práticos de engenharia e interface:

1. **Padronização de Dados (Dicionários):** Para melhorar a experiência do usuário, a interface exibe nomes formatados (ex: "São Paulo"). Usei dicionários em Python para mapear e traduzir essas escolhas para o padrão exato que o banco de dados SQL exige (ex: "Sao Paulo"), evitando bugs e consultas vazias.
2. **Processamento de Imagens em Lote:** A biblioteca de galeria do Streamlit cortava as pontas dos escudos por eles terem formatos diferentes. Em vez de editar os arquivos manualmente, usei a biblioteca **Pillow (PIL)** no Python para adicionar uma margem transparente padrão em todas as imagens automaticamente antes de enviá-las para a tela.
3. **Imagens Locais e Licenças:** Para evitar que o painel quebre se links externos mudarem, estruturei uma pasta local de *assets* (`img/`) com escudos quadrados e adicionei os devidos créditos de licença (CC BY-NC 4.0) no rodapé da aplicação.

## 💻 Tecnologias

* **Linguagem & Banco de Dados:** Python, Pandas, SQLite.
* **Interface e Gráficos:** Streamlit, Plotly Express (para interatividade).

> 🖼️ *Escudos providos por PNG Download sob licença CC BY-NC 4.0.*