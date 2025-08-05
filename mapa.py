import plotly.graph_objects as go

# Dicionário com coordenadas aproximadas dos estados (pode expandir depois)
estados_coords = {
    "TJAC": {"lat": -9.97499, "lon": -67.8243},
    "TJAL": {"lat": -9.6658, "lon": -35.735},
    "TJAM": {"lat": -3.1187, "lon": -60.0212},
    "TJAP": {"lat": 0.0349, "lon": -51.0694},
    "TJBA": {"lat": -12.9714, "lon": -38.5014},
    "TJCE": {"lat": -3.7172, "lon": -38.5433},
    "TJDF": {"lat": -15.7939, "lon": -47.8828},
    "TJES": {"lat": -20.3155, "lon": -40.3128},
    "TJGO": {"lat": -16.6869, "lon": -49.2648},
    "TJMA": {"lat": -2.5307, "lon": -44.3068},
    "TJMG": {"lat": -19.9167, "lon": -43.9345},
    "TJMS": {"lat": -20.4486, "lon": -54.6295},
    "TJMT": {"lat": -15.5989, "lon": -56.0949},
    "TJPA": {"lat": -1.4558, "lon": -48.5039},
    "TJPB": {"lat": -7.115, "lon": -34.8641},
    "TJPE": {"lat": -8.0476, "lon": -34.877},
    "TJPI": {"lat": -5.0892, "lon": -42.8016},
    "TJRJ": {"lat": -22.9068, "lon": -43.1729},
    "TJRN": {"lat": -5.7945, "lon": -35.211},
    "TJRO": {"lat": -8.7608, "lon": -63.8999},
    "TJRR": {"lat": 2.8238, "lon": -60.6753},
    "TJRS": {"lat": -30.0346, "lon": -51.2177},
    "TJSC": {"lat": -27.5954, "lon": -48.548},
    "TJSE": {"lat": -10.9472, "lon": -37.0731},
    "TJSP": {"lat": -23.5505, "lon": -46.6333},
    "TJTO": {"lat": -10.1849, "lon": -48.3336},
}

def mostrar_mapa_triangulacoes(triangulos):
    fig = go.Figure()

    for tri in triangulos:
        try:
            origem_a = tri["A ➝"]
            origem_b = tri["B ➝"]
            origem_c = tri["C ➝"]

            pontos = [origem_a, origem_b, origem_c, origem_a]  # fecha o triângulo

            lats = [estados_coords[p]["lat"] for p in pontos]
            lons = [estados_coords[p]["lon"] for p in pontos]

            fig.add_trace(go.Scattergeo(
                locationmode='country names',
                lon=lons,
                lat=lats,
                mode='lines+markers+text',
                text=pontos,
                line=dict(width=2, color='blue'),
                marker=dict(size=6),
            ))
        except KeyError as e:
            print(f"[AVISO] Estado não encontrado nas coordenadas: {e}")

    fig.update_layout(
        title="🔺 Triangulações entre Juízes no Mapa do Brasil",
        geo=dict(
            scope='south america',
            projection_type='mercator',
            showland=True,
            landcolor='rgb(217, 217, 217)',
        ),
        height=600
    )

    return fig

def mostrar_mapa_casais(casais):
    fig = go.Figure()

    for casal in casais:
        try:
            estado_a = casal["Origem A"]
            estado_b = casal["Origem B"]

            lats = [estados_coords[estado_a]["lat"], estados_coords[estado_b]["lat"]]
            lons = [estados_coords[estado_a]["lon"], estados_coords[estado_b]["lon"]]

            fig.add_trace(go.Scattergeo(
                locationmode='country names',
                lon=lons,
                lat=lats,
                mode='lines+markers+text',
                text=[estado_a, estado_b],
                line=dict(width=2, color='green'),
                marker=dict(size=6),
            ))
        except KeyError as e:
            print(f"[AVISO] Estado não encontrado nas coordenadas: {e}")

    fig.update_layout(
        title="🔁 Permutas Diretas no Mapa do Brasil",
        geo=dict(
            scope='south america',
            projection_type='mercator',
            showland=True,
            landcolor='rgb(217, 217, 217)',
        ),
        height=600
    )

    return fig
