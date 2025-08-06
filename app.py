import streamlit as st
import gspread
import json
import pandas as pd
from algoritmo import buscar_permutas_diretas, buscar_triangulacoes
from mapa import mostrar_mapa_triangulacoes, mostrar_mapa_casais

# ===============================
# Função para carregar dados via st.secrets
# ===============================
@st.cache_data
def carregar_dados():
    # Lê as credenciais direto do secrets.toml
    creds_dict = st.secrets["google_service_account"]

    # Autenticação com gspread
    gc = gspread.service_account_from_dict(creds_dict)
    sheet = gc.open("Permuta - Magistratura Estadual").sheet1
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])

    # Limpar espaços e valores vazios
    for coluna in ["Destino 1", "Destino 2", "Destino 3"]:
        df[coluna] = df[coluna].apply(lambda x: x.strip() if x.strip() != "" else None)
    df["Nome"] = df["Nome"].str.strip()
    df["Origem"] = df["Origem"].str.strip()
    return df


# ===============================
# Interface
# ===============================
st.markdown(
    """
    <h1 style='text-align: center; color: #2c3e50;'>
    🔄 Permuta entre Juízes – Consulta Personalizada
    </h1>
    """,
    unsafe_allow_html=True
)

# Login simples
usuarios = {"admin": "1234"}
usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")
if usuarios.get(usuario) != senha:
    st.warning("Acesso restrito. Digite usuário e senha válidos.")
    st.stop()

# Carregar dados
df = carregar_dados()

# ===============================
# Seleção de origem e destino
# ===============================
st.markdown(
    "<h3 style='color: #34495e;'>🔍 Escolha seus critérios</h3>",
    unsafe_allow_html=True
)
col1, col2 = st.columns(2)
with col1:
    origem_user = st.selectbox("📍 Sua Origem", sorted(df["Origem"].dropna().unique()))
with col2:
    destino_user = st.selectbox(
        "🎯 Seu Destino Preferencial",
        sorted(set(df["Destino 1"].dropna()) |
               set(df["Destino 2"].dropna()) |
               set(df["Destino 3"].dropna()))
    )

# ===============================
# 🔎 Consulta personalizada
# ===============================
if st.button("🔍 Buscar Permutas e Triangulações para meu caso"):
    casais_filtrados = buscar_permutas_diretas(df, origem_user, destino_user)
    triangulos_filtrados = buscar_triangulacoes(df, origem_user, destino_user)

    if casais_filtrados:
        st.success(f"🎯 {len(casais_filtrados)} permuta(s) direta(s) encontrada(s) para seu caso:")
        st.dataframe(pd.DataFrame(casais_filtrados))
        st.subheader("🌐 Visualização no Mapa (Casais):")
        fig_casais = mostrar_mapa_casais(casais_filtrados)
        st.plotly_chart(fig_casais, use_container_width=True)
    else:
        st.info("⚠️ Nenhuma permuta direta encontrada para sua origem e destino.")

    if triangulos_filtrados:
        st.success(f"🔺 {len(triangulos_filtrados)} triangulação(ões) possível(is) para seu caso:")
        st.dataframe(pd.DataFrame(triangulos_filtrados))
        st.subheader("🌐 Visualização no Mapa (Triangulações):")
        fig_triang = mostrar_mapa_triangulacoes(triangulos_filtrados)
        st.plotly_chart(fig_triang, use_container_width=True)
    else:
        st.info("⚠️ Nenhuma triangulação encontrada para sua origem e destino.")

# ===============================
# Base completa (opcional)
# ===============================
with st.expander("📂 Ver base de dados completa"):
    st.dataframe(df)
