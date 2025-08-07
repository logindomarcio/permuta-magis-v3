import unicodedata

def normalizar_texto(texto):
    if not isinstance(texto, str):
        return ""
    texto_norm = unicodedata.normalize('NFKD', texto)
    texto_sem_acento = ''.join(c for c in texto_norm if not unicodedata.combining(c))
    return texto_sem_acento.strip().lower()


def buscar_permutas_diretas(df, origem_user=None, destino_user=None):
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


def buscar_triangulacoes(df, origem_user=None, destino_user=None):
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
