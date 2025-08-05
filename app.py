import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from algoritmo import buscar_permutas_diretas, buscar_triangulacoes
from mapa import mostrar_mapa_triangulacoes
import plotly.graph_objects as go

from mapa import mostrar_mapa_triangulacoes
from mapa import mostrar_mapa_triangulacoes, mostrar_mapa_casais



# Função para carregar e limpar dados
@st.cache_data
def carregar_dados():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "credenciais.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open("Permuta - Magistratura Estadual").sheet1
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])

    # Limpar dados vazios e espaços
    for coluna in ["Destino 1", "Destino 2", "Destino 3"]:
        df[coluna] = df[coluna].apply(lambda x: x.strip() if x.strip() != "" else None)
    df["Nome"] = df["Nome"].str.strip()
    df["Origem"] = df["Origem"].str.strip()
    return df

# Interface Streamlit
st.title("🔄 Permuta entre Juízes – Consulta de Casais e Triangulações")

# Login simples
usuarios = {"admin": "1234"}
usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")
if usuarios.get(usuario) != senha:
    st.warning("Acesso restrito. Digite usuário e senha válidos.")
    st.stop()

# Carregar dados
df = carregar_dados()
st.success("✅ Dados carregados com sucesso.")

# Mostrar tabela de base
with st.expander("🔍 Ver base de dados"):
    st.dataframe(df)

# Botões de ação
st.subheader("🔎 Consultas disponíveis:")

if st.button("🔁 Buscar Permutas Diretas (Casais)"):
    casais = buscar_permutas_diretas(df)
    if casais:
        st.success(f"🎯 {len(casais)} permuta(s) direta(s) encontrada(s):")
        st.dataframe(pd.DataFrame(casais))

        # Mapa de permutas diretas
        st.subheader("🌐 Visualização no Mapa:")
        fig = mostrar_mapa_casais(casais)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("⚠️ Não há nenhuma permuta direta possível no momento.")


if st.button("🔺 Buscar Triangulações"):
    triangulos = buscar_triangulacoes(df)
    if triangulos:
        st.success(f"🔺 {len(triangulos)} triangulação(ões) possível(is):")
        st.dataframe(pd.DataFrame(triangulos))

        # Mapa
        st.subheader("🌐 Visualização no Mapa:")
        fig = mostrar_mapa_triangulacoes(triangulos)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("⚠️ Não há triangulações possíveis a partir dos dados.")