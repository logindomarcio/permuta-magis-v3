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
    creds_dict = json.loads(st.secrets["google_service_account"])
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
        sorted(set(df["Destino 1"].dropna()) | set(df["Destino 2"].dropna()) | set(df["Destino 3"].dropna()))
    )

# ===============================
# Botão para buscar
# ===============================
if st.button("🔎 Buscar Permutas e Triangulações para meu caso"):
    # Permutas diretas
    casais_todos = buscar_permutas_diretas(df)
    casais_filtrados = [
        c for c in casais_todos
        if (c["A"] == origem_user and c["B→"] == destino_user) or
           (c["B"] == origem_user and c["A→"] == destino_user)
    ]

    triang_todos = buscar_triangulacoes(df)
    triang_filtrados = [
        t for t in triang_todos
        if t["A"] == origem_user and t["C→"] == destino_user
    ]

    # Resultados permutas diretas
    st.markdown("<h4 style='color: #27ae60;'>🔁 Permutas Diretas Encontradas</h4>", unsafe_allow_html=True)
    if casais_filtrados:
        st.success(f"{len(casais_filtrados)} permuta(s) direta(s) encontrada(s).")
        st.dataframe(pd.DataFrame(casais_filtrados))
        fig_casais = mostrar_mapa_casais(casais_filtrados)
        st.plotly_chart(fig_casais, use_container_width=True)
    else:
        st.info("Nenhuma permuta direta encontrada para sua origem/destino.")

    # Resultados triangulações
    st.markdown("<h4 style='color: #2980b9;'>🔺 Triangulações Encontradas</h4>", unsafe_allow_html=True)
    if triang_filtrados:
        st.success(f"{len(triang_filtrados)} triangulação(ões) encontrada(s).")
        st.dataframe(pd.DataFrame(triang_filtrados))
        fig_triang = mostrar_mapa_triangulacoes(triang_filtrados)
        st.plotly_chart(fig_triang, use_container_width=True)
    else:
        st.info("Nenhuma triangulação encontrada para sua origem/destino.")

# ===============================
# Base completa (opcional)
# ===============================
with st.expander("📂 Ver base de dados completa"):
    st.dataframe(df)
