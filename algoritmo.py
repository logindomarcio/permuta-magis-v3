import pandas as pd

def buscar_permutas_diretas(df, origem_user, destinos_user_list):
    """
    Busca permutas diretas (casais) para um usuário específico
    
    LÓGICA: Para formar casal A ↔ B:
    1. A quer ir para onde B está 
    2. B quer ir para onde A está
    """
    casais = []
    
    if not origem_user or not destinos_user_list:
        return casais
    
    # Encontrar dados do usuário
    try:
        usuario_rows = df[df["Origem"] == origem_user]
        if len(usuario_rows) == 0:
            return casais
        
        usuario_row = usuario_rows.iloc[0]
        usuario_nome = usuario_row.get("Nome", "")
        
        # Limpar destinos do usuário
        destinos_limpos = []
        for destino in destinos_user_list:
            if pd.notna(destino) and str(destino).strip():
                destinos_limpos.append(str(destino).strip())
        
        # Para cada destino que o usuário quer
        for destino_desejado in destinos_limpos:
            
            # Buscar juízes no destino desejado
            juizes_no_destino = df[df["Origem"] == destino_desejado]
            
            for _, juiz_row in juizes_no_destino.iterrows():
                juiz_nome = juiz_row.get("Nome", "")
                juiz_origem = juiz_row.get("Origem", "")
                
                # Obter destinos do juiz
                destinos_do_juiz = []
                for col in ["Destino 1", "Destino 2", "Destino 3"]:
                    destino_val = juiz_row.get(col)
                    if pd.notna(destino_val) and str(destino_val).strip():
                        destinos_do_juiz.append(str(destino_val).strip())
                
                # Verificar se o juiz quer ir para onde o usuário está
                if origem_user in destinos_do_juiz:
                    casal = {
                        "Juiz A": usuario_nome,
                        "Entrância A": usuario_row.get("Entrância", ""),
                        "Origem A": origem_user,
                        "Destino A": destino_desejado,
                        "Juiz B": juiz_nome,
                        "Entrância B": juiz_row.get("Entrância", ""),
                        "Origem B": juiz_origem,
                        "Destino B": origem_user
                    }
                    casais.append(casal)
    
    except Exception as e:
        print(f"Erro em buscar_permutas_diretas: {e}")
        return []
    
    return casais


def buscar_triangulacoes(df, origem_user, destinos_user_list):
    """
    Busca triangulações envolvendo o usuário
    
    LÓGICA: A → B → C → A
    """
    triangulos = []
    
    if not origem_user or not destinos_user_list:
        return triangulos
    
    try:
        # Encontrar dados do usuário
        usuario_rows = df[df["Origem"] == origem_user]
        if len(usuario_rows) == 0:
            return triangulos
        
        usuario_row = usuario_rows.iloc[0]
        usuario_nome = usuario_row.get("Nome", "")
        
        # Limpar destinos do usuário
        destinos_limpos = []
        for destino in destinos_user_list:
            if pd.notna(destino) and str(destino).strip():
                destinos_limpos.append(str(destino).strip())
        
        # Para cada destino que o usuário quer (posição B)
        for origem_b in destinos_limpos:
            
            # Buscar juízes em origem_b
            juizes_b = df[df["Origem"] == origem_b]
            
            for _, juiz_b_row in juizes_b.iterrows():
                juiz_b_nome = juiz_b_row.get("Nome", "")
                
                # Destinos que B quer
                destinos_b = []
                for col in ["Destino 1", "Destino 2", "Destino 3"]:
                    destino_val = juiz_b_row.get(col)
                    if pd.notna(destino_val) and str(destino_val).strip():
                        destinos_b.append(str(destino_val).strip())
                
                # Para cada destino que B quer (posição C)
                for origem_c in destinos_b:
                    
                    # Buscar juízes em origem_c
                    juizes_c = df[df["Origem"] == origem_c]
                    
                    for _, juiz_c_row in juizes_c.iterrows():
                        juiz_c_nome = juiz_c_row.get("Nome", "")
                        
                        # Destinos que C quer
                        destinos_c = []
                        for col in ["Destino 1", "Destino 2", "Destino 3"]:
                            destino_val = juiz_c_row.get(col)
                            if pd.notna(destino_val) and str(destino_val).strip():
                                destinos_c.append(str(destino_val).strip())
                        
                        # Verificar se C quer ir para onde o usuário está
                        if origem_user in destinos_c:
                            triangulo = {
                                "Juiz A": usuario_nome,
                                "Entrância A": usuario_row.get("Entrância", ""),
                                "Origem A": origem_user,
                                "A ➝": origem_b,
                                "Juiz B": juiz_b_nome,
                                "Entrância B": juiz_b_row.get("Entrância", ""),
                                "Origem B": origem_b,
                                "B ➝": origem_c,
                                "Juiz C": juiz_c_nome,
                                "Entrância C": juiz_c_row.get("Entrância", ""),
                                "Origem C": origem_c,
                                "C ➝": origem_user
                            }
                            triangulos.append(triangulo)
    
    except Exception as e:
        print(f"Erro em buscar_triangulacoes: {e}")
        return []
    
    return triangulos


def buscar_quadrangulacoes(df, origem_user, destinos_user_list):
    """
    Busca quadrangulações envolvendo o usuário
    
    LÓGICA: A → B → C → D → A
    """
    quadrangulos = []
    
    if not origem_user or not destinos_user_list:
        return quadrangulos
    
    try:
        # Encontrar dados do usuário
        usuario_rows = df[df["Origem"] == origem_user]
        if len(usuario_rows) == 0:
            return quadrangulos
        
        usuario_row = usuario_rows.iloc[0]
        usuario_nome = usuario_row.get("Nome", "")
        
        # Limpar destinos do usuário
        destinos_limpos = []
        for destino in destinos_user_list:
            if pd.notna(destino) and str(destino).strip():
                destinos_limpos.append(str(destino).strip())
        
        # Para cada destino que o usuário quer (posição B)
        for origem_b in destinos_limpos:
            
            # Buscar juízes em origem_b
            juizes_b = df[df["Origem"] == origem_b]
            
            for _, juiz_b_row in juizes_b.iterrows():
                juiz_b_nome = juiz_b_row.get("Nome", "")
                
                # Destinos que B quer
                destinos_b = []
                for col in ["Destino 1", "Destino 2", "Destino 3"]:
                    destino_val = juiz_b_row.get(col)
                    if pd.notna(destino_val) and str(destino_val).strip():
                        destinos_b.append(str(destino_val).strip())
                
                # Para cada destino que B quer (posição C)
                for origem_c in destinos_b:
                    
                    # Buscar juízes em origem_c
                    juizes_c = df[df["Origem"] == origem_c]
                    
                    for _, juiz_c_row in juizes_c.iterrows():
                        juiz_c_nome = juiz_c_row.get("Nome", "")
                        
                        # Destinos que C quer
                        destinos_c = []
                        for col in ["Destino 1", "Destino 2", "Destino 3"]:
                            destino_val = juiz_c_row.get(col)
                            if pd.notna(destino_val) and str(destino_val).strip():
                                destinos_c.append(str(destino_val).strip())
                        
                        # Para cada destino que C quer (posição D)
                        for origem_d in destinos_c:
                            
                            # Buscar juízes em origem_d
                            juizes_d = df[df["Origem"] == origem_d]
                            
                            for _, juiz_d_row in juizes_d.iterrows():
                                juiz_d_nome = juiz_d_row.get("Nome", "")
                                
                                # Destinos que D quer
                                destinos_d = []
                                for col in ["Destino 1", "Destino 2", "Destino 3"]:
                                    destino_val = juiz_d_row.get(col)
                                    if pd.notna(destino_val) and str(destino_val).strip():
                                        destinos_d.append(str(destino_val).strip())
                                
                                # Verificar se D quer ir para onde o usuário está
                                if origem_user in destinos_d:
                                    quadrangulo = {
                                        "Juiz A": usuario_nome,
                                        "Entrância A": usuario_row.get("Entrância", ""),
                                        "Origem A": origem_user,
                                        "A ➝": origem_b,
                                        "Juiz B": juiz_b_nome,
                                        "Entrância B": juiz_b_row.get("Entrância", ""),
                                        "Origem B": origem_b,
                                        "B ➝": origem_c,
                                        "Juiz C": juiz_c_nome,
                                        "Entrância C": juiz_c_row.get("Entrância", ""),
                                        "Origem C": origem_c,
                                        "C ➝": origem_d,
                                        "Juiz D": juiz_d_nome,
                                        "Entrância D": juiz_d_row.get("Entrância", ""),
                                        "Origem D": origem_d,
                                        "D ➝": origem_user
                                    }
                                    quadrangulos.append(quadrangulo)
    
    except Exception as e:
        print(f"Erro em buscar_quadrangulacoes: {e}")
        return []
    
    return quadrangulos