import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from streamlit_image_select import image_select
from PIL import Image

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

# --- PRIMEIRA LINHA DE INSIGHTS ---
col1, col2 = st.columns(2)

with col1:
    st.info("📉 **Efeito Pandemia**\n\nA média isolada contra a queda geral.")
    with st.expander("A Média vs. O Seu Time"):
        st.write("Sem público (2020-2021), a média de vitórias dos mandantes no campeonato caiu de **50%** para **43%**. Mas será que o seu time acompanhou essa queda geral ou conseguiu transformar o estádio vazio em uma fortaleza? Use o filtro abaixo para comparar os números absolutos!")

with col2:
    st.success("🏆 **O Efeito Manada**\n\nCruzeiro: 2008 vs. 2014.")
    with st.expander("A Média vs. O Seu Time"):
        st.write("O Cruzeiro venceu **15 jogos** em casa em 2008 e em 2014 (quase 80% de aproveitamento). Em 2008, o gráfico nacional subiu porque outros times também foram bem. Em 2014, o Cruzeiro brilhou sozinho, e a média da liga ficou estagnada. Um time isolado não move a média.")

# --- SEGUNDA LINHA DE INSIGHTS ---
col3, col4 = st.columns(2)

with col3:
    st.warning("⚠️ **O Outlier Solitário**\n\nO caso do São Paulo em 2012.")
    with st.expander("A Média vs. O Seu Time"):
        st.write("Em 2012, a média nacional de vitórias dos mandantes foi muito baixa, beirando os **40%**. Parece que ninguém ganhou em casa naquele ano. Mas ao filtrar o **São Paulo**, vemos que ele venceu **quase 80%** dos jogos como mandante. A média escondeu essa realidade individual.")

with col4:
    st.error("🦅 **O Visitante Letal**\n\nA anomalia do Corinthians em 2017.")
    with st.expander("A Média vs. O Seu Time"):
        st.write("A média histórica de vitórias de um time visitante no Brasileirão é de **4.7 jogos** por ano. Em 2017, o Corinthians venceu incríveis **9 jogos** fora de casa. Ao roubar tantos pontos dos donos da casa, ele ajudou a puxar o gráfico geral de vitórias dos mandantes para baixo.")

st.divider()

# --- NOVO: FILTRO DE TIMES COM ESCUDOS CLICÁVEIS ---
st.subheader("🔎 Análise Individual por Clube")

# Nossos nomes visuais na tela
times_nomes = ["Geral", "Flamengo", "Corinthians", "São Paulo", "Palmeiras", "Cruzeiro"]

# Nossos arquivos locais originais
caminhos_imagens = [
    "img/cbf.png",
    "img/flamengo.png",
    "img/corinthians.png",
    "img/saopaulo.png",
    "img/palmeiras.png",
    "img/cruzeiro.png"
]

# --- NOVA MÁGICA: Processando e Salvando as imagens ---
def adicionar_margem(caminho):
    img = Image.open(caminho).convert("RGBA")
    largura, altura = img.size
    margem = 60 # 60 pixels de borda transparente
    
    # Cria a nova "tela" transparente e cola o escudo
    nova_img = Image.new("RGBA", (largura + margem*2, altura + margem*2), (0, 0, 0, 0))
    nova_img.paste(img, (margem, margem), img)
    
    # Gera um novo nome de arquivo (ex: "img/cbf_formatado.png")
    novo_caminho = caminho.replace(".png", "_formatado.png")
    
    # Salva a imagem fisicamente na sua pasta img
    nova_img.save(novo_caminho, format="PNG")
    
    return novo_caminho # Devolvemos apenas o texto do caminho!

# Aplicamos a função (isso vai criar 6 novos arquivos na sua pasta img)
caminhos_com_borda = [adicionar_margem(caminho) for caminho in caminhos_imagens]

# Passamos os CAMINHOS (textos) para a galeria, evitando o erro de JPEG
indice_selecionado = image_select(
    label="Selecione um escudo para analisar o time:",
    images=caminhos_com_borda, 
    captions=times_nomes,
    return_value="index" 
)

# Descobrimos qual time foi clicado com base no número da posição
time_escolhido_tela = times_nomes[indice_selecionado]

# O nosso famoso dicionário tradutor (com um ajuste para o 'Geral')
mapa_times = {
    "Geral": "Geral (Todos os Times)",
    "Flamengo": "Flamengo",
    "Corinthians": "Corinthians",
    "São Paulo": "Sao Paulo",
    "Palmeiras": "Palmeiras",
    "Cruzeiro": "Cruzeiro"
}

# Traduzimos e enviamos para o banco de dados
nome_para_banco = mapa_times[time_escolhido_tela]
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