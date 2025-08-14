import streamlit as st
import gspread
import pandas as pd
from algoritmo import buscar_permutas_diretas, buscar_triangulacoes, buscar_quadrangulacoes
from mapa import mostrar_mapa_triangulacoes, mostrar_mapa_casais
import unicodedata
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter

# ===============================
# Configuração da página
# ===============================
st.set_page_config(
    page_title="Busca de Permutas",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
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

def limpar_celula(x):
    if not isinstance(x, str):
        return None
    x = unicodedata.normalize('NFKD', x)
    x = ''.join(c for c in x if not unicodedata.combining(c))
    x = x.replace('\xa0', ' ').strip()
    return x if x else None

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

    # Limpeza reforçada de colunas relevantes
    for coluna in ["Destino 1", "Destino 2", "Destino 3", "E-mail", "Entrância"]:
        if coluna in df.columns:
            df[coluna] = df[coluna].apply(lambda x: str(x).strip() if pd.notnull(x) and str(x).strip() != "" else None)

    df["Nome"] = df["Nome"].str.strip()
    df["Origem"] = df["Origem"].str.strip()
    df["Nome_Normalizado"] = df["Nome"].apply(normalizar_texto)
    
    # Filtrar apenas registros com dados válidos
    df = df[df["Nome"].notna() & (df["Nome"] != "") & df["Origem"].notna() & (df["Origem"] != "")]
    
    return df

def calcular_estatisticas(df):
    """Calcula estatísticas para os dashboards"""
    # Tribunais mais procurados (destinos)
    destinos = []
    for col in ["Destino 1", "Destino 2", "Destino 3"]:
        destinos.extend(df[col].dropna().tolist())
    tribunais_procurados = Counter(destinos).most_common(5)
    
    # Tribunais mais exportadores (origens)
    tribunais_exportadores = df["Origem"].value_counts().head(5)
    
    # Calcular hubs (tribunais que aparecem em muitas combinações)
    todas_localizacoes = set(df["Origem"].unique())
    for col in ["Destino 1", "Destino 2", "Destino 3"]:
        todas_localizacoes.update(df[col].dropna().unique())
    
    hub_scores = {}
    for tribunal in todas_localizacoes:
        # Conta quantas vezes aparece como origem ou destino
        score = 0
        score += len(df[df["Origem"] == tribunal])
        for col in ["Destino 1", "Destino 2", "Destino 3"]:
            score += len(df[df[col] == tribunal])
        hub_scores[tribunal] = score
    
    tribunais_hubs = sorted(hub_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return tribunais_procurados, tribunais_exportadores, tribunais_hubs

def obter_prioridade_destino(origem_juiz, destino_final, df):
    """Retorna a prioridade do destino (1, 2 ou 3) para um juiz"""
    juiz_row = df[df["Origem"] == origem_juiz].iloc[0] if len(df[df["Origem"] == origem_juiz]) > 0 else None
    if juiz_row is None:
        return "", ""
    
    if juiz_row["Destino 1"] == destino_final:
        return "¹", "🔵"  # Azul para prioridade 1
    elif juiz_row["Destino 2"] == destino_final:
        return "²", "🟢"  # Verde para prioridade 2
    elif juiz_row["Destino 3"] == destino_final:
        return "³", "🔴"  # Vermelho para prioridade 3
    return "", ""

def obter_nome_juiz_por_origem(origem, df):
    """Retorna o nome do juiz baseado na origem"""
    juiz_row = df[df["Origem"] == origem]
    if len(juiz_row) > 0:
        return juiz_row.iloc[0]["Nome"]
    return origem  # Fallback para a origem se não encontrar o nome

# ===============================
# CSS personalizado para melhor estética
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
        letter-spacing: -1px;
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
        border: 1px solid #e9ecef;
        text-align: center;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #495057;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .search-section {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin: 2rem 0;
        border: 1px solid #e9ecef;
    }
    
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e9ecef;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #f39c12;
        margin: 1rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #a8e6cf 0%, #81c784 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #27ae60;
        margin: 1rem 0;
    }
    
    .info-box {
        background: linear-gradient(135deg, #a8d8ff 0%, #74b9ff 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #0984e3;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# ===============================
# Interface - Título e descrição
# ===============================
st.markdown('<h1 class="main-header">Busca de Permutas</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Sistema colaborativo e gratuito para interessados projetarem casais de permuta, triangulação e quadrangulação</p>', unsafe_allow_html=True)

# ===============================
# Botão para atualizar dados manualmente
# ===============================
col_update1, col_update2, col_update3 = st.columns([1, 2, 1])
with col_update2:
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
email_user = st.text_input("Digite seu e-mail para acessar a aplicação:", placeholder="exemplo@email.com")

if email_user not in emails_autorizados:
    st.markdown('<div class="warning-box">⚠️ <strong>Acesso restrito.</strong> Seu e-mail não está cadastrado na base de dados.</div>', unsafe_allow_html=True)
    st.stop()

# ===============================
# Estatísticas e métricas
# ===============================
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
    # Calcular número aproximado de permutas possíveis (combinação simples)
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
        fig_procurados = go.Figure(data=[go.Bar(
            x=[item[1] for item in tribunais_procurados],
            y=[item[0] for item in tribunais_procurados],
            orientation='h',
            marker_color='#667eea'
        )])
        fig_procurados.update_layout(
            title="🎯 Tribunais Mais Procurados",
            height=300,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig_procurados, use_container_width=True)

with col2:
    if not tribunais_exportadores.empty:
        fig_exportadores = go.Figure(data=[go.Bar(
            x=tribunais_exportadores.values,
            y=tribunais_exportadores.index,
            orientation='h',
            marker_color='#fd79a8'
        )])
        fig_exportadores.update_layout(
            title="📤 Tribunais Mais Exportadores",
            height=300,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig_exportadores, use_container_width=True)

with col3:
    if tribunais_hubs:
        fig_hubs = go.Figure(data=[go.Bar(
            x=[item[1] for item in tribunais_hubs],
            y=[item[0] for item in tribunais_hubs],
            orientation='h',
            marker_color='#00cec9'
        )])
        fig_hubs.update_layout(
            title="🔗 Tribunais Hubs",
            height=300,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig_hubs, use_container_width=True)

# ===============================
# Seleção por nome do juiz
# ===============================
st.markdown('<div class="search-section">', unsafe_allow_html=True)
st.markdown("<h3 style='color: #495057; font-weight: 600;'>🔍 Escolha seus critérios</h3>", unsafe_allow_html=True)

# Seleção do nome
nomes_disponiveis = sorted(df["Nome"].unique())
nome_selecionado = st.selectbox("👤 Selecione seu nome:", [""] + nomes_disponiveis, index=0)

# Seleção dos tipos de busca
st.markdown("**Tipos de combinações a buscar:**")
col1, col2, col3 = st.columns(3)

with col1:
    buscar_casais = st.checkbox("💑 Permuta Bilateral (Casal)", value=True)
with col2:
    buscar_triangulos = st.checkbox("🔺 Triangulação", value=True)  
with col3:
    buscar_quadrangulos = st.checkbox("🔷 Quadrangulação", value=True)

st.markdown('</div>', unsafe_allow_html=True)

# ===============================
# Busca personalizada
# ===============================
if st.button("🔍 Buscar Permutas e Combinações"):
    if not nome_selecionado:
        st.markdown('<div class="warning-box">⚠️ <strong>Atenção:</strong> Por favor, selecione seu nome para realizar a busca.</div>', unsafe_allow_html=True)
        st.stop()
    
    # Obter dados do juiz selecionado
    juiz_data = df[df["Nome"] == nome_selecionado].iloc[0]
    origem_user = juiz_data["Origem"]
    destinos_user = [juiz_data["Destino 1"], juiz_data["Destino 2"], juiz_data["Destino 3"]]
    destinos_user = [d for d in destinos_user if pd.notna(d) and d != ""]
    
    st.markdown(f"**Buscando combinações para:** {nome_selecionado} ({origem_user})")
    st.markdown(f"**Destinos desejados:** {', '.join(destinos_user)}")
    
    resultados_encontrados = False
    
    # Busca por casais (permuta bilateral)
    if buscar_casais:
        casais_filtrados = buscar_permutas_diretas(df, origem_user, destinos_user)
        
        if casais_filtrados:
            resultados_encontrados = True
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown(f"🎯 **{len(casais_filtrados)} permuta(s) direta(s) encontrada(s):**")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Legenda de cores
            st.markdown("""
            **Legenda de Prioridades:**
            🔵 **Destino 1** - Prioritário | 🟢 **Destino 2** - Secundário | 🔴 **Destino 3** - Terciário
            """)
            
            # Criar tabela simplificada para casais
            casais_tabela = []
            for casal in casais_filtrados:
                # Obter nomes e prioridades
                nome_usuario = nome_selecionado
                nome_parceiro = obter_nome_juiz_por_origem(casal["Origem B"], df)
                
                prioridade_usuario, cor_usuario = obter_prioridade_destino(origem_user, casal["Destino A"], df)
                prioridade_parceiro, cor_parceiro = obter_prioridade_destino(casal["Origem B"], casal["Destino B"], df)
                
                casais_tabela.append({
                    "👤 Seu Nome": nome_usuario,
                    "📍 Sua Origem": origem_user,
                    "🎯 Você vai para": f"{casal['Destino A']}{prioridade_usuario}",
                    "🤝 Parceiro": nome_parceiro,
                    "📍 Origem do Parceiro": casal["Origem B"],
                    "🎯 Parceiro vai para": f"{casal['Destino B']}{prioridade_parceiro}",
                    "💡 Combinação": f"{nome_usuario} ↔ {nome_parceiro}"
                })
            
            df_casais = pd.DataFrame(casais_tabela)
            st.dataframe(df_casais, use_container_width=True, hide_index=True)
            
            if 'mostrar_mapa_casais' in globals():
                st.subheader("🌐 Visualização no Mapa (Casais):")
                fig_casais = mostrar_mapa_casais(casais_filtrados)
                st.plotly_chart(fig_casais, use_container_width=True)
        else:
            st.markdown('<div class="info-box">ℹ️ <strong>Permuta Bilateral:</strong> Nenhuma permuta direta encontrada. Isso pode ocorrer quando não há outro juiz que queira ir para sua origem e você também não queira ir para a origem dele.</div>', unsafe_allow_html=True)
    
    # Busca por triangulações
    if buscar_triangulos:
        triangulos_filtrados = buscar_triangulacoes(df, origem_user, destinos_user)
        
        if triangulos_filtrados:
            resultados_encontrados = True
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown(f"🔺 **{len(triangulos_filtrados)} triangulação(ões) encontrada(s):**")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Legenda de cores para triangulações
            st.markdown("""
            **Legenda de Prioridades:**
            🔵 **Destino 1** - Prioritário | 🟢 **Destino 2** - Secundário | 🔴 **Destino 3** - Terciário
            """)
            
            # Criar tabela simplificada para triangulações
            triangulos_tabela = []
            for i, triangulo in enumerate(triangulos_filtrados, 1):
                # Obter nomes
                nome_a = nome_selecionado if triangulo["Origem A"] == origem_user else obter_nome_juiz_por_origem(triangulo["Origem A"], df)
                nome_b = obter_nome_juiz_por_origem(triangulo["Origem B"], df)
                nome_c = obter_nome_juiz_por_origem(triangulo["Origem C"], df)
                
                # Obter prioridades
                prioridade_a, _ = obter_prioridade_destino(triangulo["Origem A"], triangulo["A ➝"], df)
                prioridade_b, _ = obter_prioridade_destino(triangulo["Origem B"], triangulo["B ➝"], df)
                prioridade_c, _ = obter_prioridade_destino(triangulo["Origem C"], triangulo["C ➝"], df)
                
                # Criar explicação da combinação
                combinacao = f"🔄 {nome_a} → {triangulo['A ➝']}{prioridade_a} → {nome_b} → {triangulo['B ➝']}{prioridade_b} → {nome_c} → {triangulo['C ➝']}{prioridade_c} → {nome_a}"
                
                triangulos_tabela.append({
                    "🔢": f"#{i}",
                    "👤 Participante A": f"{nome_a} ({triangulo['Origem A']})",
                    "👤 Participante B": f"{nome_b} ({triangulo['Origem B']})",
                    "👤 Participante C": f"{nome_c} ({triangulo['Origem C']})",
                    "🔄 Fluxo da Triangulação": combinacao,
                    "📋 Resumo": f"A→{triangulo['A ➝']}{prioridade_a}, B→{triangulo['B ➝']}{prioridade_b}, C→{triangulo['C ➝']}{prioridade_c}"
                })
            
            df_triangulos = pd.DataFrame(triangulos_tabela)
            st.dataframe(df_triangulos, use_container_width=True, hide_index=True)
            
            if 'mostrar_mapa_triangulacoes' in globals():
                st.subheader("🌐 Visualização no Mapa (Triangulações):")
                fig_triang = mostrar_mapa_triangulacoes(triangulos_filtrados)
                st.plotly_chart(fig_triang, use_container_width=True)
        else:
            st.markdown('<div class="info-box">ℹ️ <strong>Triangulação:</strong> Nenhuma triangulação encontrada. Para haver triangulação, é necessário que existam três juízes onde A quer ir para onde B está, B quer ir para onde C está, e C quer ir para onde A está.</div>', unsafe_allow_html=True)
    
    # Busca por quadrangulações
    if buscar_quadrangulos:
        quadrangulos_filtrados = buscar_quadrangulacoes(df, origem_user, destinos_user)
        
        if quadrangulos_filtrados:
            resultados_encontrados = True
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown(f"🔷 **{len(quadrangulos_filtrados)} quadrangulação(ões) encontrada(s):**")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Legenda de cores para quadrangulações
            st.markdown("""
            **Legenda de Prioridades:**
            🔵 **Destino 1** - Prioritário | 🟢 **Destino 2** - Secundário | 🔴 **Destino 3** - Terciário
            """)
            
            # Criar tabela simplificada para quadrangulações
            quadrangulos_tabela = []
            for i, quad in enumerate(quadrangulos_filtrados, 1):
                # Obter nomes
                nome_a = nome_selecionado if quad["Origem A"] == origem_user else obter_nome_juiz_por_origem(quad["Origem A"], df)
                nome_b = obter_nome_juiz_por_origem(quad["Origem B"], df)
                nome_c = obter_nome_juiz_por_origem(quad["Origem C"], df)
                nome_d = obter_nome_juiz_por_origem(quad["Origem D"], df)
                
                # Obter prioridades
                prioridade_a, _ = obter_prioridade_destino(quad["Origem A"], quad["A ➝"], df)
                prioridade_b, _ = obter_prioridade_destino(quad["Origem B"], quad["B ➝"], df)
                prioridade_c, _ = obter_prioridade_destino(quad["Origem C"], quad["C ➝"], df)
                prioridade_d, _ = obter_prioridade_destino(quad["Origem D"], quad["D ➝"], df)
                
                # Criar explicação da combinação
                combinacao = f"🔄 {nome_a} → {quad['A ➝']}{prioridade_a} → {nome_b} → {quad['B ➝']}{prioridade_b} → {nome_c} → {quad['C ➝']}{prioridade_c} → {nome_d} → {quad['D ➝']}{prioridade_d} → {nome_a}"
                
                quadrangulos_tabela.append({
                    "🔢": f"#{i}",
                    "👤 Participante A": f"{nome_a} ({quad['Origem A']})",
                    "👤 Participante B": f"{nome_b} ({quad['Origem B']})",
                    "👤 Participante C": f"{nome_c} ({quad['Origem C']})",
                    "👤 Participante D": f"{nome_d} ({quad['Origem D']})",
                    "🔄 Fluxo da Quadrangulação": combinacao,
                    "📋 Resumo": f"A→{quad['A ➝']}{prioridade_a}, B→{quad['B ➝']}{prioridade_b}, C→{quad['C ➝']}{prioridade_c}, D→{quad['D ➝']}{prioridade_d}"
                })
            
            df_quadrangulos = pd.DataFrame(quadrangulos_tabela)
            st.dataframe(df_quadrangulos, use_container_width=True, hide_index=True)
        else:
            st.markdown('<div class="info-box">ℹ️ <strong>Quadrangulação:</strong> Nenhuma quadrangulação encontrada. Para haver quadrangulação, é necessário que existam quatro juízes onde A quer ir para onde B está, B quer ir para onde C está, C quer ir para onde D está, e D quer ir para onde A está.</div>', unsafe_allow_html=True)
    
    if not resultados_encontrados:
        st.markdown('<div class="info-box">ℹ️ <strong>Nenhum resultado:</strong> Não foram encontradas combinações possíveis com os critérios selecionados. Isso pode acontecer quando os destinos desejados não coincidem com as origens de outros juízes interessados em permuta.</div>', unsafe_allow_html=True)

# ===============================
# Base completa (opcional)
# ===============================
with st.expander("📂 Ver base de dados completa"):
    st.dataframe(df, use_container_width=True)

# ===============================
# Rodapé
# ===============================
st.markdown("""
    <hr style='margin-top: 3rem; border: none; height: 1px; background: linear-gradient(to right, transparent, #ddd, transparent);'>
    <div style='text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 15px; margin-top: 2rem;'>
        <p style='color: #6c757d; margin: 0.5rem 0;'>⚠️ <strong>Aplicação feita de forma colaborativa, gratuita e sem fins econômicos.</strong></p>
        <p style='color: #6c757d; margin: 0.5rem 0;'>🗂️ <strong>Os dados são voluntariamente informados por seus próprios titulares e detentores.</strong></p>
        <p style='color: #6c757d; margin: 0.5rem 0;'>🔒 <strong>A presente aplicação somente é acessada por meio do link pessoal enviado e solicitado pelo interessado.</strong></p>
        <br>
        <p style='color: #495057; margin: 0.5rem 0;'>💡 <strong>Necessita de mentoria em inteligência artificial e aplicação na sua rotina, <a href="mailto:marciocarneirodemesquitajunior@gmail.com" style='color: #667eea;'>contacte-nos</a>!</strong></p>
    </div>
""", unsafe_allow_html=True)