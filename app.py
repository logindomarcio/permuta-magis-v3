import streamlit as st
import gspread
import pandas as pd
from algoritmo import buscar_permutas_diretas, buscar_triangulacoes
from mapa import mostrar_mapa_triangulacoes, mostrar_mapa_casais

# ===============================
# Lista fixa de todos os TJs do Brasil (ordem alfabética)
# ===============================
LISTA_TJ = sorted([
    "TJAC", "TJAL", "TJAM", "TJAP", "TJBA", "TJCE", "TJDFT", "TJES",
    "TJGO", "TJMA", "TJMG", "TJMS", "TJMT", "TJPA", "TJPB", "TJPE",
    "TJPI", "TJPR", "TJRJ", "TJRN", "TJRO", "TJRR", "TJRS", "TJSC",
    "TJSE", "TJSP", "TJTO"
])

# ===============================
# Função para carregar dados via st.secrets
# ===============================
@st.cache_data
def carregar_dados():
    creds_dict = st.secrets["google_service_account"]
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

# Botão para atualizar dados
if st.button("🔄 Atualizar dados da planilha"):
    st.cache_data.clear()
    st.success("✅ Dados atualizados com sucesso!")

# Carregar dados
df = carregar_dados()

# ===============================
# Seleção de origem e destino (fixos)
# ===============================
st.markdown("<h3 style='color: #34495e;'>🔍 Escolha seus critérios</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    origem_user = st.selectbox("📍 Sua Origem", LISTA_TJ)
with col2:
    destino_user = st.selectbox("🎯 Seu Destino Preferencial", LISTA_TJ)

# ===============================
# 🔎 Consulta personalizada
# ===============================
if st.button("🔍 Buscar Permutas e Triangulações para meu caso"):

    # -------- Permutas Diretas --------
    casais_filtrados = buscar_permutas_diretas(df, origem_user, destino_user)
    if casais_filtrados:
        st.markdown(
            f"<h4 style='color: #16a085;'>🎯 {len(casais_filtrados)} permuta(s) direta(s) encontrada(s)</h4>",
            unsafe_allow_html=True
        )
        st.info(f"Troca direta entre juízes que ligam **{origem_user} ↔ {destino_user}**.")

        casais_df = pd.DataFrame(casais_filtrados)
        st.dataframe(casais_df, use_container_width=True)

        st.subheader("🌐 Visualização no Mapa (Casais):")
        fig_casais = mostrar_mapa_casais(casais_filtrados)
        st.plotly_chart(fig_casais, use_container_width=True)
    else:
        st.warning("⚠️ Nenhuma permuta direta encontrada para sua origem e destino.")

    # -------- Triangulações --------
    triangulos_filtrados = buscar_triangulacoes(df, origem_user, destino_user)
    if triangulos_filtrados:
        st.markdown(
            f"<h4 style='color: #c0392b;'>🔺 {len(triangulos_filtrados)} triangulação(ões) possível(is)</h4>",
            unsafe_allow_html=True
        )
        st.info("Cada triangulação mostra a Origem atual e o Destino desejado de cada juiz.")

        for idx, triang in enumerate(triangulos_filtrados, 1):
            st.markdown(f"**Triangulação {idx}:**")
            triang_df = pd.DataFrame([
                {"Posição": "A → B", "Juiz": triang["Juiz A"], "Origem": triang["Origem A"], "Destino": triang["Destino A"]},
                {"Posição": "B → C", "Juiz": triang["Juiz B"], "Origem": triang["Origem B"], "Destino": triang["Destino B"]},
                {"Posição": "C → A", "Juiz": triang["Juiz C"], "Origem": triang["Origem C"], "Destino": triang["Destino C"]}
            ])
            st.dataframe(triang_df, use_container_width=True)

        st.subheader("🌐 Visualização no Mapa (Triangulações):")
        fig_triang = mostrar_mapa_triangulacoes(triangulos_filtrados)
        st.plotly_chart(fig_triang, use_container_width=True)
    else:
        st.warning("⚠️ Nenhuma triangulação encontrada para sua origem e destino.")

# ===============================
# Base completa (opcional)
# ===============================
with st.expander("📂 Ver base de dados completa"):
    st.dataframe(df)
