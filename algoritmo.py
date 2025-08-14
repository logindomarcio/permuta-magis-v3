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
    LÓGICA RIGOROSA: A quer ir para onde B está E B quer ir para onde A está
    """
    casais = []
    origem_user_norm = normalizar_texto(origem_user)
    destinos_user_norm = [normalizar_texto(d) for d in destinos_user_list if pd.notna(d) and d.strip()]

    # Obter dados do usuário
    usuario_row = df[df["Origem"] == origem_user].iloc[0] if len(df[df["Origem"] == origem_user]) > 0 else None
    if usuario_row is None:
        return casais

    for i, linha_b in df.iterrows():
        # Pular se é o próprio usuário
        if linha_b["Origem"] == origem_user:
            continue
            
        origem_b = linha_b.get("Origem")
        origem_b_norm = normalizar_texto(origem_b)
        
        # Obter destinos do juiz B
        destinos_b = [
            linha_b.get("Destino 1"),
            linha_b.get("Destino 2"), 
            linha_b.get("Destino 3")
        ]
        destinos_b = [d.strip() for d in destinos_b if pd.notna(d) and str(d).strip()]
        destinos_b_norm = [normalizar_texto(d) for d in destinos_b]

        # CONDIÇÃO 1: O usuário quer ir para onde B está?
        usuario_quer_ir_para_b = origem_b_norm in destinos_user_norm
        
        # CONDIÇÃO 2: B quer ir para onde o usuário está?
        b_quer_ir_para_usuario = origem_user_norm in destinos_b_norm

        # SÓ FORMA CASAL SE AMBAS AS CONDIÇÕES FOREM TRUE
        if usuario_quer_ir_para_b and b_quer_ir_para_usuario:
            casal = {
                "Juiz A": usuario_row.get("Nome"),
                "Entrância A": usuario_row.get("Entrância"),
                "Origem A": origem_user,
                "Destino A": origem_b,

                "Juiz B": linha_b.get("Nome"),
                "Entrância B": linha_b.get("Entrância"),
                "Origem B": origem_b,
                "Destino B": origem_user
            }
            casais.append(casal)

    return casais? {b_quer_ir_para_usuario}")

        # SÓ FORMA CASAL SE AMBAS AS CONDIÇÕES FOREM TRUE
        if usuario_quer_ir_para_b and b_quer_ir_para_usuario:
            casal = {
                "Juiz A": usuario_row.get("Nome"),
                "Entrância A": usuario_row.get("Entrância"),
                "Origem A": origem_user,
                "Destino A": origem_b,

                "Juiz B": linha_b.get("Nome"),
                "Entrância B": linha_b.get("Entrância"),
                "Origem B": origem_b,
                "Destino B": origem_user
            }
            casais.append(casal)
            print(f"[DEBUG] ✅ CASAL FORMADO!")
        else:
            print(f"[DEBUG] ❌ Não forma casal")

    return casais


def buscar_triangulacoes(df, origem_user, destinos_user_list):
    """
    Busca triangulações envolvendo o usuário
    LÓGICA RIGOROSA: A→B, B→C, C→A (todos devem querer ir para onde o próximo está)
    """
    triangulos = []
    origem_user_norm = normalizar_texto(origem_user)
    destinos_user_norm = [normalizar_texto(d) for d in destinos_user_list if pd.notna(d) and d.strip()]

    # Obter dados do usuário
    usuario_row = df[df["Origem"] == origem_user].iloc[0] if len(df[df["Origem"] == origem_user]) > 0 else None
    if usuario_row is None:
        return triangulos

    for i, linha_b in df.iterrows():
        # Pular se é o próprio usuário
        if linha_b["Origem"] == origem_user:
            continue
            
        origem_b = linha_b.get("Origem")
        origem_b_norm = normalizar_texto(origem_b)
        
        # Obter destinos do juiz B
        destinos_b = [
            linha_b.get("Destino 1"),
            linha_b.get("Destino 2"), 
            linha_b.get("Destino 3")
        ]
        destinos_b = [d.strip() for d in destinos_b if pd.notna(d) and str(d).strip()]
        destinos_b_norm = [normalizar_texto(d) for d in destinos_b]

        # CONDIÇÃO 1: Usuário quer ir para onde B está?
        if origem_b_norm not in destinos_user_norm:
            continue

        for j, linha_c in df.iterrows():
            if j == i or linha_c["Origem"] == origem_user:
                continue

            origem_c = linha_c.get("Origem")
            origem_c_norm = normalizar_texto(origem_c)
            
            # Obter destinos do juiz C
            destinos_c = [
                linha_c.get("Destino 1"),
                linha_c.get("Destino 2"), 
                linha_c.get("Destino 3")
            ]
            destinos_c = [d.strip() for d in destinos_c if pd.notna(d) and str(d).strip()]
            destinos_c_norm = [normalizar_texto(d) for d in destinos_c]

            # CONDIÇÃO 2: B quer ir para onde C está?
            if origem_c_norm not in destinos_b_norm:
                continue

            # CONDIÇÃO 3: C quer ir para onde o usuário está?
            if origem_user_norm not in destinos_c_norm:
                continue

            # TODAS AS 3 CONDIÇÕES ATENDIDAS = TRIANGULAÇÃO VÁLIDA
            triangulo = {
                "Juiz A": usuario_row.get("Nome"),
                "Entrância A": usuario_row.get("Entrância"),
                "Origem A": origem_user,
                "A ➝": origem_b,

                "Juiz B": linha_b.get("Nome"),
                "Entrância B": linha_b.get("Entrância"),
                "Origem B": origem_b,
                "B ➝": origem_c,

                "Juiz C": linha_c.get("Nome"),
                "Entrância C": linha_c.get("Entrância"),
                "Origem C": origem_c,
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
    LÓGICA RIGOROSA: A→B, B→C, C→D, D→A (todos devem querer ir para onde o próximo está)
    """
    quadrangulos = []
    origem_user_norm = normalizar_texto(origem_user)
    destinos_user_norm = [normalizar_texto(d) for d in destinos_user_list if pd.notna(d) and d.strip()]

    # Obter dados do usuário
    usuario_row = df[df["Origem"] == origem_user].iloc[0] if len(df[df["Origem"] == origem_user]) > 0 else None
    if usuario_row is None:
        return quadrangulos

    for i, linha_b in df.iterrows():
        # Pular se é o próprio usuário
        if linha_b["Origem"] == origem_user:
            continue
            
        origem_b = linha_b.get("Origem")
        origem_b_norm = normalizar_texto(origem_b)
        
        # Obter destinos do juiz B
        destinos_b = [
            linha_b.get("Destino 1"),
            linha_b.get("Destino 2"), 
            linha_b.get("Destino 3")
        ]
        destinos_b = [d.strip() for d in destinos_b if pd.notna(d) and str(d).strip()]
        destinos_b_norm = [normalizar_texto(d) for d in destinos_b]

        # CONDIÇÃO 1: Usuário quer ir para onde B está?
        if origem_b_norm not in destinos_user_norm:
            continue

        for j, linha_c in df.iterrows():
            if j == i or linha_c["Origem"] == origem_user:
                continue

            origem_c = linha_c.get("Origem")
            origem_c_norm = normalizar_texto(origem_c)
            
            # Obter destinos do juiz C
            destinos_c = [
                linha_c.get("Destino 1"),
                linha_c.get("Destino 2"), 
                linha_c.get("Destino 3")
            ]
            destinos_c = [d.strip() for d in destinos_c if pd.notna(d) and str(d).strip()]
            destinos_c_norm = [normalizar_texto(d) for d in destinos_c]

            # CONDIÇÃO 2: B quer ir para onde C está?
            if origem_c_norm not in destinos_b_norm:
                continue

            for k, linha_d in df.iterrows():
                if k in [i, j] or linha_d["Origem"] == origem_user:
                    continue

                origem_d = linha_d.get("Origem")
                origem_d_norm = normalizar_texto(origem_d)
                
                # Obter destinos do juiz D
                destinos_d = [
                    linha_d.get("Destino 1"),
                    linha_d.get("Destino 2"), 
                    linha_d.get("Destino 3")
                ]
                destinos_d = [d.strip() for d in destinos_d if pd.notna(d) and str(d).strip()]
                destinos_d_norm = [normalizar_texto(d) for d in destinos_d]

                # CONDIÇÃO 3: C quer ir para onde D está?
                if origem_d_norm not in destinos_c_norm:
                    continue

                # CONDIÇÃO 4: D quer ir para onde o usuário está?
                if origem_user_norm not in destinos_d_norm:
                    continue

                # TODAS AS 4 CONDIÇÕES ATENDIDAS = QUADRANGULAÇÃO VÁLIDA
                quadrangulo = {
                    "Juiz A": usuario_row.get("Nome"),
                    "Entrância A": usuario_row.get("Entrância"),
                    "Origem A": origem_user,
                    "A ➝": origem_b,

                    "Juiz B": linha_b.get("Nome"),
                    "Entrância B": linha_b.get("Entrância"),
                    "Origem B": origem_b,
                    "B ➝": origem_c,

                    "Juiz C": linha_c.get("Nome"),
                    "Entrância C": linha_c.get("Entrância"),
                    "Origem C": origem_c,
                    "C ➝": origem_d,

                    "Juiz D": linha_d.get("Nome"),
                    "Entrância D": linha_d.get("Entrância"),
                    "Origem D": origem_d,
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