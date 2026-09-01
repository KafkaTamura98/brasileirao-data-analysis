import pandas as pd
import sqlite3

# URL do dataset público atualizado no GitHub
url_dados = "https://raw.githubusercontent.com/adaoduque/Brasileirao_Dataset/master/campeonato-brasileiro-full.csv"

# Lendo o CSV da internet e transformando em um DataFrame (tabela do Pandas)
df_partidas = pd.read_csv(url_dados)

# Exibindo as 5 primeiras linhas no terminal para verificar o carregamento
print("Dados carregados com sucesso! Aqui estão as primeiras linhas:")
print(df_partidas.head());

# --- FASE DE TRANSFORMAÇÃO ---

# 1. Filtrando apenas as colunas que interessam para o nosso problema
colunas_importantes = ['data', 'mandante', 'visitante', 'mandante_Placar', 'visitante_Placar']
df_limpo = df_partidas[colunas_importantes].copy()

# 2. Criando a nossa regra de negócio: Quem ganhou a partida?
def verifica_vencedor(linha):
    if linha['mandante_Placar'] > linha['visitante_Placar']:
        return 'Mandante'
    elif linha['visitante_Placar'] > linha['mandante_Placar']:
        return 'Visitante'
    else:
        return 'Empate'

# Aplicando a regra linha por linha usando a função .apply() do Pandas
df_limpo['vencedor'] = df_limpo.apply(verifica_vencedor, axis=1)

# Exibindo o resultado da nossa transformação
print("\nDados limpos e com a nova coluna 'vencedor':")
print(df_limpo.head())

# --- FASE DE CARGA (LOAD) ---
print("\nIniciando a conexão com o banco de dados...")

# Conectando (ou criando) o banco de dados SQLite local
conexao = sqlite3.connect('brasileirao.db')

# Enviando o DataFrame limpo para o banco de dados
# O parâmetro if_exists='replace' garante que, se rodarmos o script de novo, ele recria a tabela
df_limpo.to_sql('partidas', conexao, if_exists='replace', index=False)

print("Dados salvos com sucesso na tabela 'partidas' do banco 'brasileirao.db'!")

# Fechando a conexão (boa prática de segurança e gestão de memória)
conexao.close()