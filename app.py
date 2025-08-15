import streamlit as st
import gspread
import pandas as pd
from algoritmo import buscar_permutas_por_nome
import unicodedata
import plotly.graph_objects as go
from collections import Counter

# ===============================
# Configuração da página
# ===============================
st.set_page_config(
    page_title="Busca de Permutas",
    page_icon="⚖️",
    layout="wide"
)

# ===============================
# Funções auxiliares
# ===============================
def normalizar_texto(texto):
    if not isinstance(texto, str):
        return ""
    texto_norm = unicodedata.normalize('NFKD', texto)
    texto_sem_acento = ''.join(c for c in texto_norm if not unicodedata.combining(c))
    return texto_sem_acento.strip().lower()

def obter_prioridade_destino(origem_juiz, destino_final, df):
    """Retorna a prioridade do destino (1, 2 ou 3) para um juiz"""
    juiz_row = df[df["Origem"] == origem_juiz]
    if len(juiz_row) == 0:
        return ""
    
    juiz_data = juiz_row.iloc[0]
    if juiz_data.get("Destino 1") == destino_final:
        return "¹"
    elif juiz_data.get("Destino 2") == destino_final:
        return "²"
    elif juiz_data.get("Destino 3") == destino_final:
        return "³"
    return ""

def calcular_estatisticas(df):
    """Calcula estatísticas para os dashboards"""
    # Tribunais mais procurados
    destinos = []
    for col in ["Destino 1", "Destino 2", "Destino 3"]:
        destinos.extend(df[col].dropna().tolist())
    tribunais_procurados = Counter(destinos).most_common(5)
    
    # Tribunais mais exportadores
    tribunais_exportadores = df["Origem"].value_counts().head(5)
    
    # Tribunais hubs
    todas_localizacoes = set(df["Origem"].unique())
    for col in ["Destino 1", "Destino 2", "Destino 3"]:
        todas_localizacoes.update(df[col].dropna().unique())
    
    hub_scores = {}
    for tribunal in todas_localizacoes:
        score = len(df[df["Origem"] == tribunal])
        for col in ["Destino 1", "Destino 2", "Destino 3"]:
            score += len(df[df[col] == tribunal])
        hub_scores[tribunal] = score
    
    tribunais_hubs = sorted(hub_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return tribunais_procurados, tribunais_exportadores, tribunais_hubs

# ===============================
# CSS personalizado
# ===============================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 3.5rem;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 1.3rem;
        text-align: center;
        color: #6c757d;
        margin-bottom: 2rem;
        line-height: 1.5;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        text-align: center;
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #495057;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# ===============================
# Função para carregar dados
# ===============================
@st.cache_data
def carregar_dados():
    creds_dict = st.secrets["google_service_account"]
    gc = gspread.service_account_from_dict(creds_dict)
    sheet = gc.open("Permuta - Magistratura Estadual").sheet1
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])

    # Limpeza de dados
    if "Entrância" not in df.columns:
        df["Entrância"] = None

    for coluna in ["Destino 1", "Destino 2", "Destino 3", "E-mail", "Entrância"]:
        if coluna in df.columns:
            df[coluna] = df[coluna].apply(lambda x: str(x).strip() if pd.notnull(x) and str(x).strip() != "" else None)

    df["Nome"] = df["Nome"].str.strip()
    df["Origem"] = df["Origem"].str.strip()
    
    # Filtrar apenas registros válidos
    df = df[df["Nome"].notna() & (df["Nome"] != "") & df["Origem"].notna() & (df["Origem"] != "")]
    
    return df

# ===============================
# Interface principal
# ===============================
st.markdown('<h1 class="main-header">Busca de Permutas</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Sistema colaborativo e gratuito para interessados projetarem casais de permuta, triangulação e quadrangulação</p>', unsafe_allow_html=True)

# Botão para atualizar dados
col_update1, col_update2, col_update3 = st.columns([1, 2, 1])
with col_update2:
    if st.button("🔄 Atualizar base de dados agora"):
        st.cache_data.clear()
        st.success("✅ Base de dados atualizada!")

# Carregar dados
df = carregar_dados()

# Login por e-mail
emails_autorizados = set(df["E-mail"].dropna().unique())
email_user = st.text_input("Digite seu e-mail para acessar a aplicação:")

if email_user not in emails_autorizados:
    st.warning("⚠️ Acesso restrito. Seu e-mail não está cadastrado na base de dados.")
    st.stop()

# Estatísticas
tribunais_procurados, tribunais_exportadores, tribunais_hubs = calcular_estatisticas(df)

# Métricas numéricas
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number">{len(df)}</div>
        <div class="metric-label">Juízes Cadastrados</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    num_permutas = len(df) * (len(df) - 1) // 2
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number">{num_permutas}</div>
        <div class="metric-label">Permutas Possíveis</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    tribunais_unicos = len(set(df["Origem"].unique()))
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number">{tribunais_unicos}</div>
        <div class="metric-label">Tribunais Envolvidos</div>
    </div>
    """, unsafe_allow_html=True)

# Gráficos estatísticos
st.markdown("### 📊 Estatísticas dos Tribunais")
col1, col2, col3 = st.columns(3)

with col1:
    if tribunais_procurados:
        fig = go.Figure(data=[go.Bar(
            x=[item[1] for item in tribunais_procurados],
            y=[item[0] for item in tribunais_procurados],
            orientation='h',
            marker_color='#667eea'
        )])
        fig.update_layout(title="🎯 Tribunais Mais Procurados", height=300)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    if not tribunais_exportadores.empty:
        fig = go.Figure(data=[go.Bar(
            x=tribunais_exportadores.values,
            y=tribunais_exportadores.index,
            orientation='h',
            marker_color='#fd79a8'
        )])
        fig.update_layout(title="📤 Tribunais Mais Exportadores", height=300)
        st.plotly_chart(fig, use_container_width=True)

with col3:
    if tribunais_hubs:
        fig = go.Figure(data=[go.Bar(
            x=[item[1] for item in tribunais_hubs],
            y=[item[0] for item in tribunais_hubs],
            orientation='h',
            marker_color='#00cec9'
        )])
        fig.update_layout(title="🔗 Tribunais Hubs", height=300)
        st.plotly_chart(fig, use_container_width=True)

# ===============================
# Busca por nome
# ===============================
st.markdown("### 🔍 Escolha seus critérios")

# Seleção do nome
nomes_disponiveis = sorted(df["Nome"].unique())
nome_selecionado = st.selectbox("👤 Selecione seu nome:", [""] + nomes_disponiveis)

# Tipos de busca
st.markdown("**Tipos de combinações a buscar:**")
col1, col2, col3 = st.columns(3)
with col1:
    buscar_casais = st.checkbox("💑 Permuta Bilateral (Casal)", value=True)
with col2:
    buscar_triangulos = st.checkbox("🔺 Triangulação", value=True)
with col3:
    buscar_quadrangulos = st.checkbox("🔷 Quadrangulação", value=True)

# Busca
if st.button("🔍 Buscar Permutas e Combinações"):
    if not nome_selecionado:
        st.warning("⚠️ Por favor, selecione seu nome para realizar a busca.")
        st.stop()
    
    # Buscar combinações usando a função que funciona
    casais, triangulos, quadrangulos = buscar_permutas_por_nome(df, nome_selecionado)
    
    resultados_encontrados = False
    
    # Exibir casais
    if buscar_casais and casais:
        resultados_encontrados = True
        st.success(f"🎯 **{len(casais)} permuta(s) direta(s) encontrada(s):**")
        st.markdown("**Legenda:** 🔵 Destino 1 | 🟢 Destino 2 | 🔴 Destino 3")
        
        # Tabela simplificada
        casais_tabela = []
        for casal in casais:
            prioridade_a = obter_prioridade_destino(casal["Origem A"], casal["Destino A"], df)
            prioridade_b = obter_prioridade_destino(casal["Origem B"], casal["Destino B"], df)
            
            casais_tabela.append({
                "👤 Seu Nome": casal["Juiz A"],
                "📍 Sua Origem": casal["Origem A"],
                "🎯 Você vai para": f"{casal['Destino A']}{prioridade_a}",
                "🤝 Parceiro": casal["Juiz B"],
                "📍 Origem do Parceiro": casal["Origem B"],
                "🎯 Parceiro vai para": f"{casal['Destino B']}{prioridade_b}"
            })
        
        st.dataframe(pd.DataFrame(casais_tabela), use_container_width=True, hide_index=True)
    
    # Exibir triangulações
    if buscar_triangulos and triangulos:
        resultados_encontrados = True
        st.success(f"🔺 **{len(triangulos)} triangulação(ões) encontrada(s):**")
        st.markdown("**Legenda:** 🔵 Destino 1 | 🟢 Destino 2 | 🔴 Destino 3")
        
        triangulos_tabela = []
        for i, tri in enumerate(triangulos, 1):
            prioridade_a = obter_prioridade_destino(tri["Origem A"], tri["A ➝"], df)
            prioridade_b = obter_prioridade_destino(tri["Origem B"], tri["B ➝"], df)
            prioridade_c = obter_prioridade_destino(tri["Origem C"], tri["C ➝"], df)
            
            fluxo = f"{tri['Juiz A']} → {tri['A ➝']}{prioridade_a} → {tri['Juiz B']} → {tri['B ➝']}{prioridade_b} → {tri['Juiz C']} → {tri['C ➝']}{prioridade_c}"
            
            triangulos_tabela.append({
                "🔢": f"#{i}",
                "👤 Participante A": f"{tri['Juiz A']} ({tri['Origem A']})",
                "👤 Participante B": f"{tri['Juiz B']} ({tri['Origem B']})",
                "👤 Participante C": f"{tri['Juiz C']} ({tri['Origem C']})",
                "🔄 Fluxo": fluxo
            })
        
        st.dataframe(pd.DataFrame(triangulos_tabela), use_container_width=True, hide_index=True)
    
    # Exibir quadrangulações
    if buscar_quadrangulos and quadrangulos:
        resultados_encontrados = True
        st.success(f"🔷 **{len(quadrangulos)} quadrangulação(ões) encontrada(s):**")
        st.markdown("**Legenda:** 🔵 Destino 1 | 🟢 Destino 2 | 🔴 Destino 3")
        
        quadrangulos_tabela = []
        for i, quad in enumerate(quadrangulos, 1):
            prioridade_a = obter_prioridade_destino(quad["Origem A"], quad["A ➝"], df)
            prioridade_b = obter_prioridade_destino(quad["Origem B"], quad["B ➝"], df)
            prioridade_c = obter_prioridade_destino(quad["Origem C"], quad["C ➝"], df)
            prioridade_d = obter_prioridade_destino(quad["Origem D"], quad["D ➝"], df)
            
            fluxo = f"{quad['Juiz A']} → {quad['A ➝']}{prioridade_a} → {quad['Juiz B']} → {quad['B ➝']}{prioridade_b} → {quad['Juiz C']} → {quad['C ➝']}{prioridade_c} → {quad['Juiz D']} → {quad['D ➝']}{prioridade_d}"
            
            quadrangulos_tabela.append({
                "🔢": f"#{i}",
                "👤 Participante A": f"{quad['Juiz A']} ({quad['Origem A']})",
                "👤 Participante B": f"{quad['Juiz B']} ({quad['Origem B']})",
                "👤 Participante C": f"{quad['Juiz C']} ({quad['Origem C']})",
                "👤 Participante D": f"{quad['Juiz D']} ({quad['Origem D']})",
                "🔄 Fluxo": fluxo
            })
        
        st.dataframe(pd.DataFrame(quadrangulos_tabela), use_container_width=True, hide_index=True)
    
    # Mensagens de ausência de resultados
    if buscar_casais and not casais:
        st.info("ℹ️ **Permuta Bilateral:** Nenhuma permuta direta encontrada. Isso ocorre quando não há outro juiz que queira ir para sua origem e você também queira ir para a origem dele.")
    
    if buscar_triangulos and not triangulos:
        st.info("ℹ️ **Triangulação:** Nenhuma triangulação encontrada. Para haver triangulação, é necessário que existam três juízes onde A quer ir para onde B está, B quer ir para onde C está, e C quer ir para onde A está.")
    
    if buscar_quadrangulos and not quadrangulos:
        st.info("ℹ️ **Quadrangulação:** Nenhuma quadrangulação encontrada. Para haver quadrangulação, é necessário que existam quatro juízes onde A quer ir para onde B está, B quer ir para onde C está, C quer ir para onde D está, e D quer ir para onde A está.")
    
    if not resultados_encontrados:
        st.info("ℹ️ **Nenhum resultado:** Não foram encontradas combinações possíveis com os critérios selecionados.")

# Base completa
with st.expander("📂 Ver base de dados completa"):
    st.dataframe(df, use_container_width=True)

# Rodapé
st.markdown("""
    <hr style='margin-top: 3rem;'>
    <div style='text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 15px;'>
        <p style='color: #6c757d;'>⚠️ <strong>Aplicação colaborativa, gratuita e sem fins econômicos.</strong></p>
        <p style='color: #6c757d;'>🗂️ <strong>Dados voluntariamente informados pelos próprios titulares.</strong></p>
        <p style='color: #6c757d;'>🔒 <strong>Acesso restrito por e-mail cadastrado.</strong></p>
        <p style='color: #495057;'>💡 <strong>Mentoria em IA: <a href="mailto:marciocarneirodemesquitajunior@gmail.com">contacte-nos</a></strong></p>
    </div>
""", unsafe_allow_html=True)