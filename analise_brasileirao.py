import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Conectando ao banco e trazendo os dados via SQL
conexao = sqlite3.connect('brasileirao.db')
query = "SELECT data, vencedor FROM partidas"
df = pd.read_sql(query, conexao)
conexao.close()

# 2. Tratamento de Datas
# Converte a string 'dd/mm/yyyy' para o formato de data do Pandas e extrai apenas o ano
df['ano'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce').dt.year

# Removemos qualquer linha que por acaso tenha ficado sem ano válido
df = df.dropna(subset=['ano'])
df['ano'] = df['ano'].astype(int)

# 3. Calculando a taxa de vitória do mandante por ano
jogos_por_ano = df.groupby('ano').size()
vitorias_mandante = df[df['vencedor'] == 'Mandante'].groupby('ano').size()

# (Vitórias / Total de Jogos) * 100 para ter a porcentagem
taxa_vitoria_casa = (vitorias_mandante / jogos_por_ano) * 100

# Preparando a tabela final para o gráfico
df_grafico = taxa_vitoria_casa.reset_index(name='taxa_vitoria')

# 4. Desenhando o Gráfico Profissional
plt.figure(figsize=(14, 6))
sns.set_theme(style="whitegrid")

# Linha principal de tendência
sns.lineplot(data=df_grafico, x='ano', y='taxa_vitoria', marker='o', color='#1f77b4', linewidth=2.5)

# Destacando o período da pandemia (2020 e 2021) com uma faixa vermelha
plt.axvspan(2020, 2021, color='red', alpha=0.15, label='Pandemia (Sem Público)')

# Personalizando títulos e eixos para o Data Storytelling
plt.title('A Torcida Faz Falta? Taxa de Vitória dos Mandantes no Brasileirão (2003-2023)', fontsize=16, pad=15)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Vitórias do Mandante (%)', fontsize=12)
plt.xticks(df_grafico['ano'], rotation=45)
plt.ylim(35, 60) # Eixo Y fixado entre 35% e 60% para não distorcer a visualização

plt.legend()
plt.tight_layout()

# 5. Salvando a imagem na pasta para o seu LinkedIn!
plt.savefig('grafico_efeito_pandemia.png', dpi=300)
print("Análise concluída com sucesso! Gráfico salvo na pasta.")

# Mostrando o gráfico na tela
plt.show()