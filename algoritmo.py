def buscar_permutas_diretas(df):
    casais = []

    for i, linha_a in df.iterrows():
        origem_a = linha_a["Origem"]
        destinos_a = [linha_a["Destino 1"], linha_a["Destino 2"], linha_a["Destino 3"]]
        destinos_a = [d for d in destinos_a if d is not None]

        for j, linha_b in df.iterrows():
            if i == j:
                continue  # ignora comparação com ele mesmo

            origem_b = linha_b["Origem"]
            destinos_b = [linha_b["Destino 1"], linha_b["Destino 2"], linha_b["Destino 3"]]
            destinos_b = [d for d in destinos_b if d is not None]

            if origem_b in destinos_a and origem_a in destinos_b:
                casais.append({
                    "Juiz A": linha_a["Nome"],
                    "Origem A": origem_a,
                    "Destino A": origem_b,
                    "Juiz B": linha_b["Nome"],
                    "Origem B": origem_b,
                    "Destino B": origem_a
                })

    return casais

def buscar_triangulacoes(df):
    triangulos = []

    for i, linha_a in df.iterrows():
        origem_a = linha_a["Origem"]
        destinos_a = [linha_a["Destino 1"], linha_a["Destino 2"], linha_a["Destino 3"]]
        destinos_a = [d for d in destinos_a if d is not None]

        for j, linha_b in df.iterrows():
            if i == j:
                continue

            origem_b = linha_b["Origem"]
            destinos_b = [linha_b["Destino 1"], linha_b["Destino 2"], linha_b["Destino 3"]]
            destinos_b = [d for d in destinos_b if d is not None]

            if origem_b not in destinos_a:
                continue  # A não quer ir para B

            for k, linha_c in df.iterrows():
                if k in [i, j]:
                    continue

                origem_c = linha_c["Origem"]
                destinos_c = [linha_c["Destino 1"], linha_c["Destino 2"], linha_c["Destino 3"]]
                destinos_c = [d for d in destinos_c if d is not None]

                if origem_c not in destinos_b:
                    continue  # B não quer ir para C

                if origem_a in destinos_c:  # C quer ir para A
                    triangulos.append({
                        "Juiz A": linha_a["Nome"],
                        "A ➝": origem_b,
                        "Juiz B": linha_b["Nome"],
                        "B ➝": origem_c,
                        "Juiz C": linha_c["Nome"],
                        "C ➝": origem_a
                    })

    return triangulos
