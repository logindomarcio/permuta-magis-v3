import unicodedata
import pandas as pd

def normalizar_texto(texto):
    if not isinstance(texto, str):
        return ""
    texto_norm = unicodedata.normalize('NFKD', texto)
    texto_sem_acento = ''.join(c for c in texto_norm if not unicodedata.combining(c))
    return texto_sem_acento.strip().lower()


def buscar_permutas_diretas(df, origem_user, destinos_user_list):
    """
    Busca permutas diretas (casais) para um usuário específico
    """
    casais = []
    origem_user_norm = normalizar_texto(origem_user)
    destinos_user_norm = [normalizar_texto(d) for d in destinos_user_list if pd.notna(d)]

    # Obter dados do usuário
    usuario_row = df[df["Origem"] == origem_user].iloc[0] if len(df[df["Origem"] == origem_user]) > 0 else None
    if usuario_row is None:
        return casais

    for i, linha_a in df.iterrows():
        # Pular se é o próprio usuário
        if linha_a["Origem"] == origem_user:
            continue
            
        origem_a = normalizar_texto(linha_a.get("Origem"))
        entrancia_a = linha_a.get("Entrância")
        destinos_a = [
            normalizar_texto(linha_a.get("Destino 1")),
            normalizar_texto(linha_a.get("Destino 2")),
            normalizar_texto(linha_a.get("Destino 3"))
        ]
        destinos_a = [d for d in destinos_a if d]

        # Verificar se o usuário quer ir para onde linha_a está
        # E se linha_a quer ir para onde o usuário está
        if origem_a in destinos_user_norm and origem_user_norm in destinos_a:
            casal = {
                "Juiz A": usuario_row.get("Nome"),  # Nome do usuário
                "Entrância A": usuario_row.get("Entrância"),
                "Origem A": origem_user,
                "Destino A": linha_a.get("Origem"),

                "Juiz B": linha_a.get("Nome"),
                "Entrância B": entrancia_a,
                "Origem B": linha_a.get("Origem"),
                "Destino B": origem_user
            }
            casais.append(casal)

    return casais


def buscar_triangulacoes(df, origem_user, destinos_user_list):
    """
    Busca triangulações envolvendo o usuário
    """
    triangulos = []
    origem_user_norm = normalizar_texto(origem_user)
    destinos_user_norm = [normalizar_texto(d) for d in destinos_user_list if pd.notna(d)]

    # Obter dados do usuário
    usuario_row = df[df["Origem"] == origem_user].iloc[0] if len(df[df["Origem"] == origem_user]) > 0 else None
    if usuario_row is None:
        return triangulos

    for i, linha_a in df.iterrows():
        # Pular se é o próprio usuário
        if linha_a["Origem"] == origem_user:
            continue
            
        origem_a = normalizar_texto(linha_a.get("Origem"))
        entrancia_a = linha_a.get("Entrância")
        destinos_a = [
            normalizar_texto(linha_a.get("Destino 1")),
            normalizar_texto(linha_a.get("Destino 2")),
            normalizar_texto(linha_a.get("Destino 3"))
        ]
        destinos_a = [d for d in destinos_a if d]

        # Verificar se o usuário quer ir para onde A está
        if origem_a not in destinos_user_norm:
            continue

        for j, linha_b in df.iterrows():
            if j == i or linha_b["Origem"] == origem_user:
                continue

            origem_b = normalizar_texto(linha_b.get("Origem"))
            entrancia_b = linha_b.get("Entrância")
            destinos_b = [
                normalizar_texto(linha_b.get("Destino 1")),
                normalizar_texto(linha_b.get("Destino 2")),
                normalizar_texto(linha_b.get("Destino 3"))
            ]
            destinos_b = [d for d in destinos_b if d]

            # Verificar se A quer ir para onde B está
            if origem_b not in destinos_a:
                continue

            # Verificar se B quer ir para onde o usuário está
            if origem_user_norm in destinos_b:
                triangulo = {
                    "Juiz A": usuario_row.get("Nome"),  # Nome do usuário
                    "Entrância A": usuario_row.get("Entrância"),
                    "Origem A": origem_user,
                    "A ➝": linha_a.get("Origem"),

                    "Juiz B": linha_a.get("Nome"),
                    "Entrância B": entrancia_a,
                    "Origem B": linha_a.get("Origem"),
                    "B ➝": linha_b.get("Origem"),

                    "Juiz C": linha_b.get("Nome"),
                    "Entrância C": entrancia_b,
                    "Origem C": linha_b.get("Origem"),
                    "C ➝": origem_user
                }
                triangulos.append(triangulo)

    return triangulos


def buscar_quadrangulacoes(df, origem_user, destinos_user_list):
    """
    Busca quadrangulações envolvendo o usuário
    """
    quadrangulos = []
    origem_user_norm = normalizar_texto(origem_user)
    destinos_user_norm = [normalizar_texto(d) for d in destinos_user_list if pd.notna(d)]

def buscar_quadrangulacoes(df, origem_user, destinos_user_list):
    """
    Busca quadrangulações envolvendo o usuário
    """
    quadrangulos = []
    origem_user_norm = normalizar_texto(origem_user)
    destinos_user_norm = [normalizar_texto(d) for d in destinos_user_list if pd.notna(d)]

    # Obter dados do usuário
    usuario_row = df[df["Origem"] == origem_user].iloc[0] if len(df[df["Origem"] == origem_user]) > 0 else None
    if usuario_row is None:
        return quadrangulos

    for i, linha_a in df.iterrows():
        # Pular se é o próprio usuário
        if linha_a["Origem"] == origem_user:
            continue
            
        origem_a = normalizar_texto(linha_a.get("Origem"))
        entrancia_a = linha_a.get("Entrância")
        destinos_a = [
            normalizar_texto(linha_a.get("Destino 1")),
            normalizar_texto(linha_a.get("Destino 2")),
            normalizar_texto(linha_a.get("Destino 3"))
        ]
        destinos_a = [d for d in destinos_a if d]

        # Verificar se o usuário quer ir para onde A está
        if origem_a not in destinos_user_norm:
            continue

        for j, linha_b in df.iterrows():
            if j == i or linha_b["Origem"] == origem_user:
                continue

            origem_b = normalizar_texto(linha_b.get("Origem"))
            entrancia_b = linha_b.get("Entrância")
            destinos_b = [
                normalizar_texto(linha_b.get("Destino 1")),
                normalizar_texto(linha_b.get("Destino 2")),
                normalizar_texto(linha_b.get("Destino 3"))
            ]
            destinos_b = [d for d in destinos_b if d]

            # Verificar se A quer ir para onde B está
            if origem_b not in destinos_a:
                continue

            for k, linha_c in df.iterrows():
                if k in [i, j] or linha_c["Origem"] == origem_user:
                    continue

                origem_c = normalizar_texto(linha_c.get("Origem"))
                entrancia_c = linha_c.get("Entrância")
                destinos_c = [
                    normalizar_texto(linha_c.get("Destino 1")),
                    normalizar_texto(linha_c.get("Destino 2")),
                    normalizar_texto(linha_c.get("Destino 3"))
                ]
                destinos_c = [d for d in destinos_c if d]

                # Verificar se B quer ir para onde C está
                if origem_c not in destinos_b:
                    continue

                # Verificar se C quer ir para onde o usuário está
                if origem_user_norm in destinos_c:
                    quadrangulo = {
                        "Juiz A": usuario_row.get("Nome"),  # Nome do usuário
                        "Entrância A": usuario_row.get("Entrância"),
                        "Origem A": origem_user,
                        "A ➝": linha_a.get("Origem"),

                        "Juiz B": linha_a.get("Nome"),
                        "Entrância B": entrancia_a,
                        "Origem B": linha_a.get("Origem"),
                        "B ➝": linha_b.get("Origem"),

                        "Juiz C": linha_b.get("Nome"),
                        "Entrância C": entrancia_b,
                        "Origem C": linha_b.get("Origem"),
                        "C ➝": linha_c.get("Origem"),

                        "Juiz D": linha_c.get("Nome"),
                        "Entrância D": entrancia_c,
                        "Origem D": linha_c.get("Origem"),
                        "D ➝": origem_user
                    }
                    quadrangulos.append(quadrangulo)

    return quadrangulos


def buscar_todas_permutas_diretas(df):
    """
    Busca todas as permutas diretas possíveis no dataframe
    """
    casais = []

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
            if i >= j:  # Evitar duplicatas
                continue

            origem_b = normalizar_texto(linha_b.get("Origem"))
            entrancia_b = linha_b.get("Entrância")
            destinos_b = [
                normalizar_texto(linha_b.get("Destino 1")),
                normalizar_texto(linha_b.get("Destino 2")),
                normalizar_texto(linha_b.get("Destino 3"))
            ]
            destinos_b = [d for d in destinos_b if d]

            # Verificar se há permuta direta entre A e B
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
                casais.append(casal)

    return casais


def buscar_todas_triangulacoes(df):
    """
    Busca todas as triangulações possíveis no dataframe
    """
    triangulos = []

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
                    # Evitar duplicatas ordenando por índice
                    indices_ordenados = sorted([i, j, k])
                    if [i, j, k] == indices_ordenados:  # Só adiciona se está na ordem
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
                        triangulos.append(triangulo)

    return triangulos