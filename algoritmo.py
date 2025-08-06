def buscar_permutas_diretas(df, origem_user=None, destino_user=None):
    # Garantir que a coluna "Entrância" exista
    if "Entrância" not in df.columns:
        df["Entrância"] = None

    casais = []

    for i, linha_a in df.iterrows():
        origem_a = linha_a["Origem"]
        entrancia_a = linha_a["Entrância"] if "Entrância" in linha_a else None
        destinos_a = [linha_a["Destino 1"], linha_a["Destino 2"], linha_a["Destino 3"]]
        destinos_a = [d for d in destinos_a if d is not None]

        for j, linha_b in df.iterrows():
            if i == j:
                continue  # ignora comparação com ele mesmo

            origem_b = linha_b["Origem"]
            entrancia_b = linha_b["Entrância"] if "Entrância" in linha_b else None
            destinos_b = [linha_b["Destino 1"], linha_b["Destino 2"], linha_b["Destino 3"]]
            destinos_b = [d for d in destinos_b if d is not None]

            if origem_b in destinos_a and origem_a in destinos_b:
                casal = {
                    "Juiz A": linha_a["Nome"],
                    "Entrância A": entrancia_a,
                    "Origem A": origem_a,
                    "Destino A": origem_b,

                    "Juiz B": linha_b["Nome"],
                    "Entrância B": entrancia_b,
                    "Origem B": origem_b,
                    "Destino B": origem_a
                }

                # Filtro se usuário especificou origem/destino
                if origem_user and destino_user:
                    if not (
                        (origem_a == origem_user and casal["Destino A"] == destino_user) or
                        (origem_b == origem_user and casal["Destino B"] == destino_user)
                    ):
                        continue

                casais.append(casal)

    return casais


def buscar_triangulacoes(df, origem_user=None, destino_user=None):
    # Garantir que a coluna "Entrância" exista
    if "Entrância" not in df.columns:
        df["Entrância"] = None

    triangulos = []

    for i, linha_a in df.iterrows():
        origem_a = linha_a["Origem"]
        entrancia_a = linha_a["Entrância"] if "Entrância" in linha_a else None
        destinos_a = [linha_a["Destino 1"], linha_a["Destino 2"], linha_a["Destino 3"]]
        destinos_a = [d for d in destinos_a if d is not None]

        for j, linha_b in df.iterrows():
            if i == j:
                continue

            origem_b = linha_b["Origem"]
            entrancia_b = linha_b["Entrância"] if "Entrância" in linha_b else None
            destinos_b = [linha_b["Destino 1"], linha_b["Destino 2"], linha_b["Destino 3"]]
            destinos_b = [d for d in destinos_b if d is not None]

            if origem_b not in destinos_a:
                continue  # A não quer ir para B

            for k, linha_c in df.iterrows():
                if k in [i, j]:
                    continue

                origem_c = linha_c["Origem"]
                entrancia_c = linha_c["Entrância"] if "Entrância" in linha_c else None
                destinos_c = [linha_c["Destino 1"], linha_c["Destino 2"], linha_c["Destino 3"]]
                destinos_c = [d for d in destinos_c if d is not None]

                if origem_c not in destinos_b:
                    continue  # B não quer ir para C

                if origem_a in destinos_c:  # C quer ir para A
                    triangulo = {
                        "Juiz A": linha_a["Nome"],
                        "Entrância A": entrancia_a,
                        "Origem A": origem_a,
                        "A ➝": origem_b,

                        "Juiz B": linha_b["Nome"],
                        "Entrância B": entrancia_b,
                        "Origem B": origem_b,
                        "B ➝": origem_c,

                        "Juiz C": linha_c["Nome"],
                        "Entrância C": entrancia_c,
                        "Origem C": origem_c,
                        "C ➝": origem_a
                    }

                    # Filtro se usuário especificou origem/destino
                    if origem_user and destino_user:
                        if not (
                            (origem_a == origem_user and triangulo["A ➝"] == destino_user) or
                            (origem_b == origem_user and triangulo["B ➝"] == destino_user) or
                            (origem_c == origem_user and triangulo["C ➝"] == destino_user)
                        ):
                            continue

                    triangulos.append(triangulo)

    return triangulos
