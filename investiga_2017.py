import pandas as pd
import sqlite3

conexao = sqlite3.connect('brasileirao.db')

# 1. Buscando o melhor visitante de 2017 de forma dinâmica
query_2017 = """
SELECT 
    visitante as time, 
    COUNT(*) as vitorias_fora
FROM partidas
WHERE vencedor = 'Visitante' 
  AND data LIKE '%2017'
GROUP BY visitante
ORDER BY vitorias_fora DESC
LIMIT 1
"""
df_2017 = pd.read_sql(query_2017, conexao)
melhor_time_2017 = df_2017.iloc[0]['time']
vitorias_2017 = df_2017.iloc[0]['vitorias_fora']


# 2. Calculando a média histórica com CTE (Baseline)
query_media = """
WITH VitoriasFora AS (
    SELECT 
        SUBSTR(data, -4) as ano,
        visitante as time, 
        COUNT(*) as qtd_vitorias
    FROM partidas
    WHERE vencedor = 'Visitante'
    GROUP BY ano, visitante
)
SELECT ROUND(AVG(qtd_vitorias), 1) as media_historica
FROM VitoriasFora
"""
df_media = pd.read_sql(query_media, conexao)
media_historica = df_media.iloc[0]['media_historica']


# 3. Imprimindo a comparação
print("\n--- A PROVA REAL: ANOMALIA DE 2017 ---")
print(f"Média histórica de vitórias como visitante (por time/ano): {media_historica}")
print(f"Vitórias do {melhor_time_2017} em 2017: {vitorias_2017}")

# Calculando quantas vezes a mais o time venceu
proporcao = vitorias_2017 / media_historica
print(f"\nConclusão: O {melhor_time_2017} venceu {proporcao:.1f} vezes mais do que a média normal de um visitante!")

conexao.close()