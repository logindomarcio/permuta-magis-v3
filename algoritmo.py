import unicodedata
import pandas as pd

def normalizar_texto(texto):
    """Normaliza texto removendo acentos e convertendo para minúsculas"""
    if not isinstance(texto, str):
        return ""
    texto_norm = unicodedata.normalize('NFKD', texto)
    texto_sem_acento = ''.join(c for c in texto_norm if not unicodedata.combining(c))
    return texto_sem_acento.strip().lower()


def buscar_permutas_diretas(df, origem_user, destinos_user_list):
    """
    Busca permutas diretas (casais) para um usuário específico
    
    LÓGICA CORRETA:
    1. Usuário A (origem X) quer ir para tribunal Y
    2. Deve existir usuário B (origem Y) que quer ir para tribunal X
    3. Ambas condições DEVEM ser atendidas simultaneamente
    """
    casais = []
    
    # Dados do usuário que está fazendo a busca
    usuario_rows = df[df["Origem"] == origem_user]
    if len(usuario_rows) == 0:
        return casais
    
    usuario_row = usuario_rows.iloc[0]
    usuario_nome = usuario_row.get("Nome", "")
    
    # Destinos que o usuário quer (limpar dados)
    destinos_user = []
    for destino in destinos_user_list:
        if pd.notna(destino) and str(destino).strip():
            destinos_user.append(str(destino).strip())
    
    # Para cada destino que o usuário quer ir
    for destino_desejado in destinos_user:
        
        # Buscar TODOS os juízes que estão na origem desejada pelo usuário
        juizes_no_destino = df[df["Origem"] == destino_desejado]
        
        for _, juiz_potencial in juizes_no_destino.iterrows():
            juiz_nome = juiz_potencial.get("Nome", "")
            juiz_origem = juiz_potencial.get("Origem", "")
            
            # Verificar se este juiz quer ir para onde o usuário está
            destinos_do_juiz = []
            for col in ["Destino 1", "Destino 2", "Destino 3"]:
                destino_val = juiz_potencial.get(col)
                if pd.notna(destino_val) and str(destino_val).strip():
                    destinos_do_juiz.append(str(destino_val).strip())
            
            # CONDIÇÃO CRÍTICA: O juiz deve querer ir para onde o usuário está
            if origem_user in destinos_do_juiz:
                # MATCH PERFEITO! Formar casal
                casal = {
                    "Juiz A": usuario_nome,
                    "Entrância A": usuario_row.get("Entrância", ""),
                    "Origem A": origem_user,
                    "Destino A": destino_desejado,
                    "Juiz B": juiz_nome,
                    "Entrância B": juiz_potencial.get("Entrância", ""),
                    "Origem B": juiz_origem,
                    "Destino B": origem_user
                }
                casais.append(casal)
    
    return casais


def buscar_triangulacoes(df, origem_user, destinos_user_list):
    """
    Busca triangulações envolvendo o usuário
    
    LÓGICA CORRETA para A→B→C→A:
    1. A (usuário) quer ir para onde B está
    2. B quer ir para onde C está  
    3. C quer ir para onde A (usuário) está
    """
    triangulos = []
    
    # Dados do usuário
    usuario_rows = df[df["Origem"] == origem_user]
    if len(usuario_rows) == 0:
        return triangulos
    
    usuario_row = usuario_rows.iloc[0]
    usuario_nome = usuario_row.get("Nome", "")
    
    # Destinos que o usuário quer
    destinos_user = []
    for destino in destinos_user_list:
        if pd.notna(destino) and str(destino).strip():
            destinos_user.append(str(destino).strip())
    
    # Para cada destino que o usuário quer (posição B na triangulação)
    for origem_b in destinos_user:
        
        # Encontrar juízes que estão em origem_b
        juizes_b = df[df["Origem"] == origem_b]
        
        for _, juiz_b in juizes_b.iterrows():
            juiz_b_nome = juiz_b.get("Nome", "")
            
            # Destinos que o juiz B quer
            destinos_b = []
            for col in ["Destino 1", "Destino 2", "Destino 3"]:
                destino_val = juiz_b.get(col)
                if pd.notna(destino_val) and str(destino_val).strip():
                    destinos_b.append(str(destino_val).strip())
            
            # Para cada destino que B quer (posição C na triangulação)
            for origem_c in destinos_b:
                
                # Encontrar juízes que estão em origem_c
                juizes_c = df[df["Origem"] == origem_c]
                
                for _, juiz_c in juizes_c.iterrows():
                    juiz_c_nome = juiz_c.get("Nome", "")
                    
                    # Destinos que o juiz C quer
                    destinos_c = []
                    for col in ["Destino 1", "Destino 2", "Destino 3"]:
                        destino_val = juiz_c.get(col)
                        if pd.notna(destino_val) and str(destino_val).strip():
                            destinos_c.append(str(destino_val).strip())
                    
                    # CONDIÇÃO CRÍTICA: C deve querer ir para onde o usuário está
                    if origem_user in destinos_c:
                        # TRIANGULAÇÃO VÁLIDA!
                        triangulo = {
                            "Juiz A": usuario_nome,
                            "Entrância A": usuario_row.get("Entrância", ""),
                            "Origem A": origem_user,
                            "A ➝": origem_b,
                            "Juiz B": juiz_b_nome,
                            "Entrância B": juiz_b.get("Entrância", ""),
                            "Origem B": origem_b,
                            "B ➝": origem_c,
                            "Juiz C": juiz_c_nome,
                            "Entrância C": juiz_c.get("Entrância", ""),
                            "Origem C": origem_c,
                            "C ➝": origem_user
                        }
                        triangulos.append(triangulo)
    
    return triangulos


def buscar_quadrangulacoes(df, origem_user, destinos_user_list):
    """
    Busca quadrangulações envolvendo o usuário
    
    LÓGICA CORRETA para A→B→C→D→A:
    1. A (usuário) quer ir para onde B está
    2. B quer ir para onde C está
    3. C quer ir para onde D está
    4. D quer ir para onde A (usuário) está
    """
    quadrangulos = []
    
    # Dados do usuário
    usuario_rows = df[df["Origem"] == origem_user]
    if len(usuario_rows) == 0:
        return quadrangulos
    
    usuario_row = usuario_rows.iloc[0]
    usuario_nome = usuario_row.get("Nome", "")
    
    # Destinos que o usuário quer
    destinos_user = []
    for destino in destinos_user_list:
        if pd.notna(destino) and str(destino).strip():
            destinos_user.append(str(destino).strip())
    
    # Para cada destino que o usuário quer (posição B)
    for origem_b in destinos_user:
        
        # Encontrar juízes que estão em origem_b
        juizes_b = df[df["Origem"] == origem_b]
        
        for _, juiz_b in juizes_b.iterrows():
            juiz_b_nome = juiz_b.get("Nome", "")
            
            # Destinos que o juiz B quer
            destinos_b = []
            for col in ["Destino 1", "Destino 2", "Destino 3"]:
                destino_val = juiz_b.get(col)
                if pd.notna(destino_val) and str(destino_val).strip():
                    destinos_b.append(str(destino_val).strip())
            
            # Para cada destino que B quer (posição C)
            for origem_c in destinos_b:
                
                # Encontrar juízes que estão em origem_c
                juizes_c = df[df["Origem"] == origem_c]
                
                for _, juiz_c in juizes_c.iterrows():
                    juiz_c_nome = juiz_c.get("Nome", "")
                    
                    # Destinos que o juiz C quer
                    destinos_c = []
                    for col in ["Destino 1", "Destino 2", "Destino 3"]:
                        destino_val = juiz_c.get(col)
                        if pd.notna(destino_val) and str(destino_val).strip():
                            destinos_c.append(str(destino_val).strip())
                    
                    # Para cada destino que C quer (posição D)
                    for origem_d in destinos_c:
                        
                        # Encontrar juízes que estão em origem_d
                        juizes_d = df[df["Origem"] == origem_d]
                        
                        for _, juiz_d in juizes_d.iterrows():
                            juiz_d_nome = juiz_d.get("Nome", "")
                            
                            # Destinos que o juiz D quer
                            destinos_d = []
                            for col in ["Destino 1", "Destino 2", "Destino 3"]:
                                destino_val = juiz_d.get(col)
                                if pd.notna(destino_val) and str(destino_val).strip():
                                    destinos_d.append(str(destino_val).strip())
                            
                            # CONDIÇÃO CRÍTICA: D deve querer ir para onde o usuário está
                            if origem_user in destinos_d:
                                # QUADRANGULAÇÃO VÁLIDA!
                                quadrangulo = {
                                    "Juiz A": usuario_nome,
                                    "Entrância A": usuario_row.get("Entrância", ""),
                                    "Origem A": origem_user,
                                    "A ➝": origem_b,
                                    "Juiz B": juiz_b_nome,
                                    "Entrância B": juiz_b.get("Entrância", ""),
                                    "Origem B": origem_b,
                                    "B ➝": origem_c,
                                    "Juiz C": juiz_c_nome,
                                    "Entrância C": juiz_c.get("Entrância", ""),
                                    "Origem C": origem_c,
                                    "C ➝": origem_d,
                                    "Juiz D": juiz_d_nome,
                                    "Entrância D": juiz_d.get("Entrância", ""),
                                    "Origem D": origem_d,
                                    "D ➝": origem_user
                                }
                                quadrangulos.append(quadrangulo)
    
    return quadrangulos


def buscar_todas_permutas_diretas(df):
    """Busca todas as permutas diretas possíveis no dataframe"""
    casais = []
    
    for i, linha_a in df.iterrows():
        origem_a = linha_a.get("Origem", "")
        if not origem_a:
            continue
            
        nome_a = linha_a.get("Nome", "")
        entrancia_a = linha_a.get("Entrância", "")
        
        # Destinos que A quer
        destinos_a = []
        for col in ["Destino 1", "Destino 2", "Destino 3"]:
            destino_val = linha_a.get(col)
            if pd.notna(destino_val) and str(destino_val).strip():
                destinos_a.append(str(destino_val).strip())

        for j, linha_b in df.iterrows():
            if i >= j:  # Evitar duplicatas
                continue

            origem_b = linha_b.get("Origem", "")
            if not origem_b:
                continue
                
            nome_b = linha_b.get("Nome", "")
            entrancia_b = linha_b.get("Entrância", "")
            
            # Destinos que B quer
            destinos_b = []
            for col in ["Destino 1", "Destino 2", "Destino 3"]:
                destino_val = linha_b.get(col)
                if pd.notna(destino_val) and str(destino_val).strip():
                    destinos_b.append(str(destino_val).strip())

            # Verificar se há permuta direta entre A e B
            if origem_b in destinos_a and origem_a in destinos_b:
                casal = {
                    "Juiz A": nome_a,
                    "Entrância A": entrancia_a,
                    "Origem A": origem_a,
                    "Destino A": origem_b,
                    "Juiz B": nome_b,
                    "Entrância B": entrancia_b,
                    "Origem B": origem_b,
                    "Destino B": origem_a
                }
                casais.append(casal)

    return casais


def buscar_todas_triangulacoes(df):
    """Busca todas as triangulações possíveis no dataframe"""
    triangulos = []

    for i, linha_a in df.iterrows():
        origem_a = linha_a.get("Origem", "")
        if not origem_a:
            continue
            
        nome_a = linha_a.get("Nome", "")
        entrancia_a = linha_a.get("Entrância", "")
        
        # Destinos que A quer
        destinos_a = []
        for col in ["Destino 1", "Destino 2", "Destino 3"]:
            destino_val = linha_a.get(col)
            if pd.notna(destino_val) and str(destino_val).strip():
                destinos_a.append(str(destino_val).strip())

        for j, linha_b in df.iterrows():
            if i == j:
                continue

            origem_b = linha_b.get("Origem", "")
            if not origem_b or origem_b not in destinos_a:
                continue
                
            nome_b = linha_b.get("Nome", "")
            entrancia_b = linha_b.get("Entrância", "")
            
            # Destinos que B quer
            destinos_b = []
            for col in ["Destino 1", "Destino 2", "Destino 3"]:
                destino_val = linha_b.get(col)
                if pd.notna(destino_val) and str(destino_val).strip():
                    destinos_b.append(str(destino_val).strip())

            for k, linha_c in df.iterrows():
                if k in [i, j]:
                    continue

                origem_c = linha_c.get("Origem", "")
                if not origem_c or origem_c not in destinos_b:
                    continue
                    
                nome_c = linha_c.get("Nome", "")
                entrancia_c = linha_c.get("Entrância", "")
                
                # Destinos que C quer
                destinos_c = []
                for col in ["Destino 1", "Destino 2", "Destino 3"]:
                    destino_val = linha_c.get(col)
                    if pd.notna(destino_val) and str(destino_val).strip():
                        destinos_c.append(str(destino_val).strip())

                if origem_a in destinos_c:
                    # Evitar duplicatas ordenando por índice
                    indices_ordenados = sorted([i, j, k])
                    if [i, j, k] == indices_ordenados:  # Só adiciona se está na ordem
                        triangulo = {
                            "Juiz A": nome_a,
                            "Entrância A": entrancia_a,
                            "Origem A": origem_a,
                            "A ➝": origem_b,
                            "Juiz B": nome_b,
                            "Entrância B": entrancia_b,
                            "Origem B": origem_b,
                            "B ➝": origem_c,
                            "Juiz C": nome_c,
                            "Entrância C": entrancia_c,
                            "Origem C": origem_c,
                            "C ➝": origem_a
                        }
                        triangulos.append(triangulo)

    return triangulos