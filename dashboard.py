import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração da página
st.set_page_config(page_title="Mando de Campo - Brasileirão", page_icon="⚽", layout="wide")

# Título do Dashboard
st.title("⚽ O Peso do Mando de Campo no Brasileirão (2003-2023)")
st.markdown("Um mergulho analítico para descobrir se jogar em casa realmente faz diferença.")

# Carregando os dados
@st.cache_data # Isso faz o site carregar mais rápido!
def carregar_dados():
    conexao = sqlite3.connect('brasileirao.db')
    
    # Query para o gráfico principal
    query = """
    SELECT 
        SUBSTR(data, -4) as Ano,
        COUNT(CASE WHEN vencedor = 'Mandante' THEN 1 END) * 100.0 / COUNT(*) as Taxa_Vitoria_Mandante
    FROM partidas
    GROUP BY Ano
    ORDER BY Ano
    """
    df = pd.read_sql(query, conexao)
    conexao.close()
    return df

df_grafico = carregar_dados()

# Criando 3 colunas para destacar nossos grandes achados
# Criando 3 colunas para destacar nossos grandes achados
col1, col2, col3 = st.columns(3)

with col1:
    st.info("📉 **Efeito Pandemia**\n\nQueda brusca (2020-2021).")
    with st.expander("Ver detalhes matemáticos"):
        st.write("Durante a pandemia, com estádios vazios, a taxa de vitória dos mandantes despencou de uma média histórica de **50%** para quase **43%**. A ausência do '12º jogador' afetou diretamente os resultados!")

with col2:
    st.success("🏆 **Pico de 2008**\n\nCruzeiro com 15 vitórias.")
    with st.expander("Ver detalhes matemáticos"):
        st.write("A média histórica de vitórias em casa é de **9.6**. O Cruzeiro de 2008 cravou **15 vitórias** em 19 jogos, vencendo **1.5x mais** que o normal e puxando a média nacional do ano para o alto.")

with col3:
    st.warning("⚠️ **Anomalia de 2017**\n\nCorinthians letal fora.")
    with st.expander("Ver detalhes matemáticos"):
        st.write("A média histórica de um visitante é de apenas **4.7 vitórias**. O Corinthians de 2017 venceu **9 jogos** fora de casa (**1.9x mais!**), derrubando a estatística geral dos mandantes naquele campeonato.")

st.divider()

# Plotando o Gráfico Interativo
st.subheader("Evolução Histórica: Vitórias dos Mandantes (%)")

fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=df_grafico, x='Ano', y='Taxa_Vitoria_Mandante', marker='o', ax=ax, linewidth=2.5)

# Destacando a pandemia no gráfico
ax.axvspan('2020', '2021', color='red', alpha=0.15, label='Pandemia (Sem Público)')

plt.xticks(rotation=45)
plt.ylabel('Vitórias do Mandante (%)')
plt.xlabel('Ano')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# Renderizando o gráfico na tela do Streamlit
st.pyplot(fig)

st.markdown("---")
st.markdown("👨‍💻 *Projeto desenvolvido por Luan Bins.*")