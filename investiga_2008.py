import pandas as pd
import sqlite3

conexao = sqlite3.connect('brasileirao.db')

# 1. Buscando o melhor mandante de 2008
query_2008 = """
SELECT 
    mandante as time, 
    COUNT(*) as vitorias_casa
FROM partidas
WHERE vencedor = 'Mandante' 
  AND data LIKE '%2008'
GROUP BY mandante
ORDER BY vitorias_casa DESC
LIMIT 1
"""
df_2008 = pd.read_sql(query_2008, conexao)
melhor_time_2008 = df_2008.iloc[0]['time']
vitorias_2008 = df_2008.iloc[0]['vitorias_casa']

# 2. Calculando a média histórica de vitórias em casa com CTE (Baseline)
query_media_casa = """
WITH VitoriasCasa AS (
    SELECT 
        SUBSTR(data, -4) as ano,
        mandante as time, 
        COUNT(*) as qtd_vitorias
    FROM partidas
    WHERE vencedor = 'Mandante'
    GROUP BY ano, mandante
)
SELECT ROUND(AVG(qtd_vitorias), 1) as media_historica
FROM VitoriasCasa
"""
df_media = pd.read_sql(query_media_casa, conexao)
media_historica_casa = df_media.iloc[0]['media_historica']

# 3. Imprimindo a comparação
print("\n--- A PROVA REAL: PICO DE 2008 ---")
print(f"Média histórica de vitórias como mandante (por time/ano): {media_historica_casa}")
print(f"Vitórias do {melhor_time_2008} em 2008: {vitorias_2008}")

proporcao = vitorias_2008 / media_historica_casa
print(f"\nConclusão: O {melhor_time_2008} venceu {proporcao:.1f} vezes mais que a média de um mandante!")

conexao.close()