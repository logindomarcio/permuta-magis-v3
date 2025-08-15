import unicodedata

def normalizar_texto(texto):
    if not isinstance(texto, str):
        return ""
    texto_norm = unicodedata.normalize('NFKD', texto)
    texto_sem_acento = ''.join(c for c in texto_norm if not unicodedata.combining(c))
    return texto_sem_acento.strip().lower()


def buscar_permutas_diretas(df, origem_user, destino_user):
    """
    MANTENDO A LÓGICA ORIGINAL QUE FUNCIONA
    Busca permutas diretas entre origem_user e destino_user
    """
    casais = []

    # Normalizar entrada do usuário
    origem_user = normalizar_texto(origem_user)
    destino_user = normalizar_texto(destino_user)

    for i, linha_a in df.iterrows():
        origem_a = normalizar_texto(linha_a.get("Origem"))
        entrancia_a = linha_a.get("Entrância")
        destinos_a = [
            normalizar_texto(linha_a.get("Destino 1")),
            normalizar_texto(linha_a.get("Destino 2")),
            normalizar_texto(linha_a.get("Destino 3"))
        ]
        destinos_a = [d for d in destinos_a if d]

        for j, linha_b in df.iterrows():
            if i == j:
                continue

            origem_b = normalizar_texto(linha_b.get("Origem"))
            entrancia_b = linha_b.get("Entrância")
            destinos_b = [
                normalizar_texto(linha_b.get("Destino 1")),
                normalizar_texto(linha_b.get("Destino 2")),
                normalizar_texto(linha_b.get("Destino 3"))
            ]
            destinos_b = [d for d in destinos_b if d]

            if origem_b in destinos_a and origem_a in destinos_b:
                casal = {
                    "Juiz A": linha_a.get("Nome"),
                    "Entrância A": entrancia_a,
                    "Origem A": linha_a.get("Origem"),
                    "Destino A": linha_b.get("Origem"),

                    "Juiz B": linha_b.get("Nome"),
                    "Entrância B": entrancia_b,
                    "Origem B": linha_b.get("Origem"),
                    "Destino B": linha_a.get("Origem")
                }

                if origem_user and destino_user:
                    if not (
                        (origem_a == origem_user and origem_b == destino_user) or
                        (origem_b == origem_user and origem_a == destino_user)
                    ):
                        continue

                casais.append(casal)

    return casais


def buscar_triangulacoes(df, origem_user, destino_user):
    """
    MANTENDO A LÓGICA ORIGINAL QUE FUNCIONA
    Busca triangulações envolvendo origem_user e destino_user
    """
    triangulos = []

    origem_user = normalizar_texto(origem_user)
    destino_user = normalizar_texto(destino_user)

    for i, linha_a in df.iterrows():
        origem_a = normalizar_texto(linha_a.get("Origem"))
        entrancia_a = linha_a.get("Entrância")
        destinos_a = [
            normalizar_texto(linha_a.get("Destino 1")),
            normalizar_texto(linha_a.get("Destino 2")),
            normalizar_texto(linha_a.get("Destino 3"))
        ]
        destinos_a = [d for d in destinos_a if d]

        for j, linha_b in df.iterrows():
            if i == j:
                continue

            origem_b = normalizar_texto(linha_b.get("Origem"))
            entrancia_b = linha_b.get("Entrância")
            destinos_b = [
                normalizar_texto(linha_b.get("Destino 1")),
                normalizar_texto(linha_b.get("Destino 2")),
                normalizar_texto(linha_b.get("Destino 3"))
            ]
            destinos_b = [d for d in destinos_b if d]

            if origem_b not in destinos_a:
                continue

            for k, linha_c in df.iterrows():
                if k in [i, j]:
                    continue

                origem_c = normalizar_texto(linha_c.get("Origem"))
                entrancia_c = linha_c.get("Entrância")
                destinos_c = [
                    normalizar_texto(linha_c.get("Destino 1")),
                    normalizar_texto(linha_c.get("Destino 2")),
                    normalizar_texto(linha_c.get("Destino 3"))
                ]
                destinos_c = [d for d in destinos_c if d]

                if origem_c not in destinos_b:
                    continue

                if origem_a in destinos_c:
                    triangulo = {
                        "Juiz A": linha_a.get("Nome"),
                        "Entrância A": entrancia_a,
                        "Origem A": linha_a.get("Origem"),
                        "A ➝": linha_b.get("Origem"),

                        "Juiz B": linha_b.get("Nome"),
                        "Entrância B": entrancia_b,
                        "Origem B": linha_b.get("Origem"),
                        "B ➝": linha_c.get("Origem"),

                        "Juiz C": linha_c.get("Nome"),
                        "Entrância C": entrancia_c,
                        "Origem C": linha_c.get("Origem"),
                        "C ➝": linha_a.get("Origem")
                    }

                    if origem_user and destino_user:
                        if not (
                            (origem_a == origem_user and origem_b == destino_user) or
                            (origem_b == origem_user and origem_c == destino_user) or
                            (origem_c == origem_user and origem_a == destino_user)
                        ):
                            continue

                    triangulos.append(triangulo)

    return triangulos


def buscar_quadrangulacoes(df, origem_user, destino_user):
    """
    NOVA FUNÇÃO: Busca quadrangulações baseada na lógica funcionante
    """
    quadrangulos = []

    origem_user = normalizar_texto(origem_user)
    destino_user = normalizar_texto(destino_user)

    for i, linha_a in df.iterrows():
        origem_a = normalizar_texto(linha_a.get("Origem"))
        entrancia_a = linha_a.get("Entrância")
        destinos_a = [
            normalizar_texto(linha_a.get("Destino 1")),
            normalizar_texto(linha_a.get("Destino 2")),
            normalizar_texto(linha_a.get("Destino 3"))
        ]
        destinos_a = [d for d in destinos_a if d]

        for j, linha_b in df.iterrows():
            if i == j:
                continue

            origem_b = normalizar_texto(linha_b.get("Origem"))
            entrancia_b = linha_b.get("Entrância")
            destinos_b = [
                normalizar_texto(linha_b.get("Destino 1")),
                normalizar_texto(linha_b.get("Destino 2")),
                normalizar_texto(linha_b.get("Destino 3"))
            ]
            destinos_b = [d for d in destinos_b if d]

            if origem_b not in destinos_a:
                continue

            for k, linha_c in df.iterrows():
                if k in [i, j]:
                    continue

                origem_c = normalizar_texto(linha_c.get("Origem"))
                entrancia_c = linha_c.get("Entrância")
                destinos_c = [
                    normalizar_texto(linha_c.get("Destino 1")),
                    normalizar_texto(linha_c.get("Destino 2")),
                    normalizar_texto(linha_c.get("Destino 3"))
                ]
                destinos_c = [d for d in destinos_c if d]

                if origem_c not in destinos_b:
                    continue

                for l, linha_d in df.iterrows():
                    if l in [i, j, k]:
                        continue

                    origem_d = normalizar_texto(linha_d.get("Origem"))
                    entrancia_d = linha_d.get("Entrância")
                    destinos_d = [
                        normalizar_texto(linha_d.get("Destino 1")),
                        normalizar_texto(linha_d.get("Destino 2")),
                        normalizar_texto(linha_d.get("Destino 3"))
                    ]
                    destinos_d = [d for d in destinos_d if d]

                    if origem_d not in destinos_c:
                        continue

                    if origem_a in destinos_d:
                        quadrangulo = {
                            "Juiz A": linha_a.get("Nome"),
                            "Entrância A": entrancia_a,
                            "Origem A": linha_a.get("Origem"),
                            "A ➝": linha_b.get("Origem"),

                            "Juiz B": linha_b.get("Nome"),
                            "Entrância B": entrancia_b,
                            "Origem B": linha_b.get("Origem"),
                            "B ➝": linha_c.get("Origem"),

                            "Juiz C": linha_c.get("Nome"),
                            "Entrância C": entrancia_c,
                            "Origem C": linha_c.get("Origem"),
                            "C ➝": linha_d.get("Origem"),

                            "Juiz D": linha_d.get("Nome"),
                            "Entrância D": entrancia_d,
                            "Origem D": linha_d.get("Origem"),
                            "D ➝": linha_a.get("Origem")
                        }

                        if origem_user and destino_user:
                            if not (
                                (origem_a == origem_user and origem_b == destino_user) or
                                (origem_b == origem_user and origem_c == destino_user) or
                                (origem_c == origem_user and origem_d == destino_user) or
                                (origem_d == origem_user and origem_a == destino_user)
                            ):
                                continue

                        quadrangulos.append(quadrangulo)

    return quadrangulos


# FUNÇÕES AUXILIARES PARA BUSCA POR NOME
def buscar_permutas_por_nome(df, nome_juiz):
    """
    NOVA FUNÇÃO: Busca permutas para um juiz específico pelo nome
    """
    # Encontrar dados do juiz
    juiz_row = df[df["Nome"].str.contains(nome_juiz, case=False, na=False)]
    if len(juiz_row) == 0:
        return [], [], []
    
    juiz_data = juiz_row.iloc[0]
    origem_juiz = juiz_data["Origem"]
    destinos_juiz = [
        juiz_data.get("Destino 1"),
        juiz_data.get("Destino 2"),
        juiz_data.get("Destino 3")
    ]
    destinos_juiz = [d for d in destinos_juiz if d and str(d).strip()]
    
    casais = []
    triangulos = []
    quadrangulos = []
    
    # Para cada destino do juiz, buscar combinações
    for destino in destinos_juiz:
        # Buscar casais
        casais_temp = buscar_permutas_diretas(df, origem_juiz, destino)
        casais.extend(casais_temp)
        
        # Buscar triangulações
        triangulos_temp = buscar_triangulacoes(df, origem_juiz, destino)
        triangulos.extend(triangulos_temp)
        
        # Buscar quadrangulações
        quadrangulos_temp = buscar_quadrangulacoes(df, origem_juiz, destino)
        quadrangulos.extend(quadrangulos_temp)
    
    return casais, triangulos, quadrangulos