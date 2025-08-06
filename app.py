import streamlit as st
import gspread
import pandas as pd
from algoritmo import buscar_permutas_diretas, buscar_triangulacoes
from mapa import mostrar_mapa_triangulacoes, mostrar_mapa_casais

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

    # Garantir que a coluna Entrância existe
    if "Entrância" not in df.columns:
        df["Entrância"] = None

    # Limpar espaços e valores vazios
    for coluna in ["Destino 1", "Destino 2", "Destino 3", "E-mail", "Entrância"]:
        if coluna in df.columns:
            df[coluna] = df[coluna].apply(lambda x: x.strip() if x and x.strip() != "" else None)

    df["Nome"] = df["Nome"].str.strip()
    df["Origem"] = df["Origem"].str.strip()
    return df

# ===============================
# Estilo - cor de fundo bege claro
# ===============================
st.markdown(
    """
    <style>
    body { background-color: #fdf6e3; }
    </style>
    """,
    unsafe_allow_html=True
)

# ===============================
# Interface - Título e descrição
# ===============================
st.markdown(
    """
    <h1 style='text-align: center; font-family: serif; color: #2c3e50;'>
    Permuta - Magistratura Estadual
    </h1>
    <h4 style='text-align: center; font-family: serif; color: #7f8c8d;'>
    A presente aplicação tem finalidade meramente ilustrativa, gratuita e não oficial e nem é vinculada a qualquer Tribunal ou instituição associativa.
    Os dados abaixo foram voluntariamente preenchidos por interessados. Eventuais problemas técnicos são naturais.
    O objetivo foi gerar visualização gráfica e rápida dos dados.
    </h4>
    """,
    unsafe_allow_html=True
)

# ===============================
# Botão para atualizar dados manualmente
# ===============================
if st.button("🔄 Atualizar base de dados agora"):
    st.cache_data.clear()
    st.success("✅ Base de dados atualizada! Clique novamente em 'Buscar' para ver os dados mais recentes.")

# ===============================
# Carregar dados
# ===============================
df = carregar_dados()

# Lista de e-mails autorizados
emails_autorizados = set(df["E-mail"].dropna().unique())

# ===============================
# Login por e-mail
# ===============================
email_user = st.text_input("Digite seu e-mail para acessar a aplicação:")

if email_user not in emails_autorizados:
    st.warning("Acesso restrito. Seu e-mail não está cadastrado na base de dados.")
    st.stop()

# ===============================
# Lista fixa de todos os TJs do Brasil
# ===============================
lista_tjs = sorted([
    "TJAC", "TJAL", "TJAM", "TJAP", "TJBA", "TJCE", "TJDFT", "TJES", "TJGO", "TJMA",
    "TJMG", "TJMS", "TJMT", "TJPA", "TJPB", "TJPE", "TJPI", "TJPR", "TJRJ", "TJRN",
    "TJRO", "TJRR", "TJRS", "TJSC", "TJSE", "TJSP", "TJTO"
])

# ===============================
# Seleção de origem e destino
# ===============================
st.markdown("<h3 style='color: #34495e;'>🔍 Escolha seus critérios</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    origem_user = st.selectbox("📍 Sua Origem", lista_tjs)
with col2:
    destino_user = st.selectbox("🎯 Seu Destino Preferencial", lista_tjs)

# ===============================
# 🔎 Consulta personalizada
# ===============================
if st.button("🔍 Buscar Permutas e Triangulações para meu caso"):
    casais_filtrados = buscar_permutas_diretas(df, origem_user, destino_user)
    triangulos_filtrados = buscar_triangulacoes(df, origem_user, destino_user)

    # Acrescentar coluna Entrância nos resultados
    for casal in casais_filtrados:
        juiz_a = casal["Juiz A"]
        juiz_b = casal["Juiz B"]
        casal["Entrância A"] = df.loc[df["Nome"] == juiz_a, "Entrância"].values[0] if not df.loc[df["Nome"] == juiz_a, "Entrância"].empty else None
        casal["Entrância B"] = df.loc[df["Nome"] == juiz_b, "Entrância"].values[0] if not df.loc[df["Nome"] == juiz_b, "Entrância"].empty else None

    for triang in triangulos_filtrados:
        for pos in ["A", "B", "C"]:
            juiz_nome = triang[f"Juiz {pos}"]
            triang[f"Entrância {pos}"] = df.loc[df["Nome"] == juiz_nome, "Entrância"].values[0] if not df.loc[df["Nome"] == juiz_nome, "Entrância"].empty else None

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

# ===============================
# Rodapé
# ===============================
st.markdown(
    """
    <hr>
    <p>⚠️ <b>Aplicação feita de forma colaborativa, gratuita e sem fins econômicos.</b></p>
    <p>🗂️ <b>Os dados são voluntariamente informados por seus próprios titulares e detentores.</b></p>
    <p>🔒 <b>A presente aplicação somente é acessada por meio do link pessoal enviado e solicitado pelo interessado.</b></p>
    <br>
    <p>💡 <b>Necessita de mentoria em inteligência artificial e aplicação na sua rotina, <a href="mailto:marciocarneirodemesquitajunior@gmail.com">contacte-nos</a>!</b></p>
    """,
    unsafe_allow_html=True
)
