import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Mando de Campo - Brasileirão", page_icon="⚽", layout="wide")

# Título do Dashboard
st.title("⚽ O Peso do Mando de Campo no Brasileirão (2003-2023)")
st.markdown("Um mergulho analítico para descobrir se jogar em casa realmente faz diferença.")

# Carregando os dados
# Carregando os dados dinamicamente
@st.cache_data 
def carregar_dados(time_filtro):
    conexao = sqlite3.connect('brasileirao.db')
    
    # Se escolher Geral, faz a pesquisa clássica (todos os times)
    if time_filtro == "Geral (Todos os Times)":
        query = """
        SELECT 
            SUBSTR(data, -4) as Ano,
            COUNT(CASE WHEN vencedor = 'Mandante' THEN 1 END) * 100.0 / COUNT(*) as Taxa_Vitoria_Mandante
        FROM partidas
        GROUP BY Ano
        ORDER BY Ano
        """
        df = pd.read_sql(query, conexao)
        
    # Se escolher um time, injeta um WHERE para filtrar só os jogos daquele mandante
    else:
        query = """
        SELECT 
            SUBSTR(data, -4) as Ano,
            COUNT(CASE WHEN vencedor = 'Mandante' THEN 1 END) * 100.0 / COUNT(*) as Taxa_Vitoria_Mandante
        FROM partidas
        WHERE mandante = ?
        GROUP BY Ano
        ORDER BY Ano
        """
        # O 'params' protege nosso banco e injeta o nome do time no lugar da interrogação (?)
        df = pd.read_sql(query, conexao, params=(time_filtro,))
        
    conexao.close()
    df['Taxa_Vitoria_Mandante'] = df['Taxa_Vitoria_Mandante'].round(1)
    return df

# Criando 3 colunas para destacar nossos grandes achados
col1, col2, col3 = st.columns(3)

with col1:
    st.info("📉 **Efeito Pandemia**\n\nA queda brusca na média da liga (2020-2021).")
    with st.expander("A Média vs. O Seu Time"):
        st.write("Sem o '12º jogador', a taxa de vitória dos mandantes no Brasileirão despencou de **50%** para quase **43%**. Mas lembre-se: as médias escondem realidades individuais. Será que o **seu time** também sofreu essa queda ou remou contra a maré na pandemia? Use o filtro abaixo para descobrir!")

with col2:
    st.success("🏆 **Pico de 2008**\n\nO 'Efeito Manada' liderado pelo Cruzeiro.")
    with st.expander("A Média vs. O Seu Time"):
        st.write("Em 2008, o Cruzeiro ganhou **15 jogos** em casa. Como outros times também foram implacáveis, a média da liga disparou. Curiosidade: em 2014, o Cruzeiro repetiu a façanha (15 vitórias), mas como o resto da liga foi mediano, o gráfico geral nem se moveu. Um time excelente não muda a média sozinho!")

with col3:
    st.warning("⚠️ **Anomalia de 2017**\n\nO visitante letal que derrubou a estatística.")
    with st.expander("A Média vs. O Seu Time"):
        st.write("A média histórica de um visitante é vencer **4.7 jogos**. O Corinthians de 2017 venceu incríveis **9 jogos** fora de casa (quase o dobro!). Ao dominar como visitante, ele 'roubou' os pontos dos donos da casa, puxando o gráfico geral dos mandantes para baixo.")

st.divider()

# --- NOVO: FILTRO DE TIMES COM MAPEAMENTO ---
st.subheader("🔎 Análise Individual por Clube")

# Dicionário: A chave é o que aparece na tela (bonito), o valor é o que o banco entende
mapa_times = {
    "Geral (Todos os Times)": "Geral (Todos os Times)",
    "Flamengo": "Flamengo",
    "Corinthians": "Corinthians",
    "São Paulo": "Sao Paulo",  # <-- A nossa tradução mágica aqui!
    "Palmeiras": "Palmeiras",
    "Cruzeiro": "Cruzeiro"
}

# O Streamlit extrai e mostra apenas os nomes bonitos (as chaves do dicionário)
time_selecionado = st.selectbox(
    "Selecione um time para ver o desempenho dele:", 
    list(mapa_times.keys())
)

# Descobrimos qual é o nome "feio" correspondente e enviamos ele para a função do banco
nome_para_banco = mapa_times[time_selecionado]
df_grafico = carregar_dados(nome_para_banco)

st.divider()

# Plotando o Gráfico Interativo
st.subheader("Evolução Histórica: Vitórias dos Mandantes (%)")

# Criando o gráfico interativo com Plotly
fig = px.line(
    df_grafico, 
    x='Ano', 
    y='Taxa_Vitoria_Mandante', 
    markers=True,
    labels={'Ano': '', 'Taxa_Vitoria_Mandante': 'Vitórias (%)'}
)

# 1. Movimento e Estilo: Suavizando a linha (Spline)
fig.update_traces(
    line=dict(width=4, shape='spline'), 
    marker=dict(size=8, symbol="circle-dot")
)

# 2. Interatividade JS e Limpeza Visual
fig.update_layout(
    hovermode="x unified",
    xaxis=dict(
        rangeslider=dict(visible=False), # Removemos a barra inferior!
        showgrid=False,
        dtick=1, # Força o eixo a mostrar ano a ano
        range=['2003', '2023'] # Trava o gráfico para não ir até 2025
    ),
    yaxis=dict(showgrid=True, gridcolor='rgba(200, 200, 200, 0.2)'),
    plot_bgcolor="rgba(0,0,0,0)", 
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=30, l=0, r=0, b=0)
)

# Adicionando a faixa vermelha da pandemia
fig.add_vrect(
    x0="2020", x1="2021", 
    fillcolor="red", opacity=0.15, 
    line_width=0, 
    annotation_text="Pandemia", 
    annotation_position="top left"
)

# Renderizando no Streamlit
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("👨‍💻 *Projeto desenvolvido por Luan Bins.*")