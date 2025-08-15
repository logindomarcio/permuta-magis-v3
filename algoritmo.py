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
    
    LÓGICA CRÍTICA:
    Para formar casal entre usuário A e juiz B:
    1. A deve querer ir para onde B está (origem de B)
    2. B deve querer ir para onde A está (origem de A)
    AMBAS condições são OBRIGATÓRIAS
    """
    casais = []
    
    # Validar entrada
    if not origem_user or not destinos_user_list:
        return casais
    
    # Encontrar dados do usuário
    usuario_rows = df[df["Origem"].str.strip() == origem_user.strip()]
    if len(usuario_rows) == 0:
        return casais
    
    usuario_row = usuario_rows.iloc[0]
    usuario_nome = str(usuario_row.get("Nome", "")).strip()
    
    # Limpar e preparar destinos do usuário
    destinos_limpos = []
    for destino in destinos_user_list:
        if pd.notna(destino):
            destino_limpo = str(destino).strip()
            if destino_limpo:
                destinos_limpos.append(destino_limpo)
    
    # Para cada destino que o usuário quer
    for destino_desejado in destinos_limpos:
        
        # Encontrar TODOS os juízes que estão no destino desejado
        juizes_no_destino = df[df["Origem"].str.strip() == destino_desejado.strip()]
        
        for idx, juiz_row in juizes_no_destino.iterrows():
            juiz_nome = str(juiz_row.get("Nome", "")).strip()
            juiz_origem = str(juiz_row.get("Origem", "")).strip()
            
            # Obter destinos deste juiz (limpar dados)
            destinos_do_juiz = []
            for coluna in ["Destino 1", "Destino 2", "Destino 3"]:
                destino_val = juiz_row.get(coluna)
                if pd.notna(destino_val):
                    destino_limpo = str(destino_val).strip()
                    if destino_limpo:
                        destinos_do_juiz.append(destino_limpo)
            
            # VERIFICAÇÃO CRÍTICA: Este juiz quer ir para onde o usuário está?
            if origem_user.strip() in destinos_do_juiz:
                
                # Formar casal válido
                casal = {
                    "Juiz A": usuario_nome,
                    "Entrância A": str(usuario_row.get("Entrância", "")).strip(),
                    "Origem A": origem_user.strip(),
                    "Destino A": destino_desejado.strip(),
                    "Juiz B": juiz_nome,
                    "Entrância B": str(juiz_row.get("Entrância", "")).strip(),
                    "Origem B": juiz_origem,
                    "Destino B": origem_user.strip()
                }
                casais.append(casal)
    
    return casais            for coluna in ["Destino 1", "Destino 2", "Destino 3"]:
                destino_val = juiz_row.get(coluna)
                if pd.notna(destino_val):
                    destino_limpo = str(destino_val).strip()
                    if destino_limpo:
                        destinos_do_juiz.append(destino_limpo)
            
            # VERIFICAÇÃO CRÍTICA: Este juiz quer ir para onde o usuário está?
            if origem_user.strip() in destinos_do_juiz:
                
                # Formar casal válido
                casal = {
                    "Juiz A": usuario_nome,
                    "Entrância A": str(usuario_row.get("Entrância", "")).strip(),
                    "Origem A": origem_user.strip(),
                    "Destino A": destino_desejado.strip(),
                    "Juiz B": juiz_nome,
                    "Entrância B": str(juiz_row.get("Entrância", "")).strip(),
                    "Origem B": juiz_origem,
                    "Destino B": origem_user.strip()
                }
                casais.append(casal)
    
    return casais


def buscar_triangulacoes(df, origem_user, destinos_user_list):
    """
    Busca triangulações envolvendo o usuário
    
    LÓGICA CRÍTICA para A→B→C→A:
    1. A (usuário) quer ir para onde B está
    2. B quer ir para onde C está
    3. C quer ir para onde A (usuário) está
    TODAS as 3 condições são OBRIGATÓRIAS
    """
    triangulos = []
    
    # Validar entrada
    if not origem_user or not destinos_user_list:
        return triangulos
    
    # Encontrar dados do usuário
    usuario_rows = df[df["Origem"].str.strip() == origem_user.strip()]
    if len(usuario_rows) == 0:
        return triangulos
    
    usuario_row = usuario_rows.iloc[0]
    usuario_nome = str(usuario_row.get("Nome", "")).strip()
    
    # Limpar destinos do usuário
    destinos_limpos = []
    for destino in destinos_user_list:
        if pd.notna(destino):
            destino_limpo = str(destino).strip()
            if destino_limpo:
                destinos_limpos.append(destino_limpo)
    
    # Para cada destino que o usuário quer (será a posição B)
    for origem_b in destinos_limpos:
        
        # Encontrar juízes que estão em origem_b
        juizes_b = df[df["Origem"].str.strip() == origem_b.strip()]
        
        for _, juiz_b_row in juizes_b.iterrows():
            juiz_b_nome = str(juiz_b_row.get("Nome", "")).strip()
            
            # Obter destinos que o juiz B quer
            destinos_b = []
            for coluna in ["Destino 1", "Destino 2", "Destino 3"]:
                destino_val = juiz_b_row.get(coluna)
                if pd.notna(destino_val):
                    destino_limpo = str(destino_val).strip()
                    if destino_limpo:
                        destinos_b.append(destino_limpo)
            
            # Para cada destino que B quer (será a posição C)
            for origem_c in destinos_b:
                
                # Encontrar juízes que estão em origem_c
                juizes_c = df[df["Origem"].str.strip() == origem_c.strip()]
                
                for _, juiz_c_row in juizes_c.iterrows():
                    juiz_c_nome = str(juiz_c_row.get("Nome", "")).strip()
                    
                    # Obter destinos que o juiz C quer
                    destinos_c = []
                    for coluna in ["Destino 1", "Destino 2", "Destino 3"]:
                        destino_val = juiz_c_row.get(coluna)
                        if pd.notna(destino_val):
                            destino_limpo = str(destino_val).strip()
                            if destino_limpo:
                                destinos_c.append(destino_limpo)
                    
                    # VERIFICAÇÃO CRÍTICA: C quer ir para onde o usuário está?
                    if origem_user.strip() in destinos_c:
                        
                        # TRIANGULAÇÃO VÁLIDA!
                        triangulo = {
                            "Juiz A": usuario_nome,
                            "Entrância A": str(usuario_row.get("Entrância", "")).strip(),
                            "Origem A": origem_user.strip(),
                            "A ➝": origem_b.strip(),
                            "Juiz B": juiz_b_nome,
                            "Entrância B": str(juiz_b_row.get("Entrância", "")).strip(),
                            "Origem B": origem_b.strip(),
                            "B ➝": origem_c.strip(),
                            "Juiz C": juiz_c_nome,
                            "Entrância C": str(juiz_c_row.get("Entrância", "")).strip(),
                            "Origem C": origem_c.strip(),
                            "C ➝": origem_user.strip()
                        }
                        triangulos.append(triangulo)
    
    return triangulos


def buscar_quadrangulacoes(df, origem_user, destinos_user_list):
    """
    Busca quadrangulações envolvendo o usuário
    
    LÓGICA CRÍTICA para A→B→C→D→A:
    1. A (usuário) quer ir para onde B está
    2. B quer ir para onde C está
    3. C quer ir para onde D está
    4. D quer ir para onde A (usuário) está
    TODAS as 4 condições são OBRIGATÓRIAS
    """
    quadrangulos = []
    
    # Validar entrada
    if not origem_user or not destinos_user_list:
        return quadrangulos
    
    # Encontrar dados do usuário
    usuario_rows = df[df["Origem"].str.strip() == origem_user.strip()]
    if len(usuario_rows) == 0:
        return quadrangulos
    
    usuario_row = usuario_rows.iloc[0]
    usuario_nome = str(usuario_row.get("Nome", "")).strip()
    
    # Limpar destinos do usuário
    destinos_limpos = []
    for destino in destinos_user_list:
        if pd.notna(destino):
            destino_limpo = str(destino).strip()
            if destino_limpo:
                destinos_limpos.append(destino_limpo)
    
    # Para cada destino que o usuário quer (posição B)
    for origem_b in destinos_limpos:
        
        # Encontrar juízes em origem_b
        juizes_b = df[df["Origem"].str.strip() == origem_b.strip()]
        
        for _, juiz_b_row in juizes_b.iterrows():
            juiz_b_nome = str(juiz_b_row.get("Nome", "")).strip()
            
            # Destinos que B quer
            destinos_b = []
            for coluna in ["Destino 1", "Destino 2", "Destino 3"]:
                destino_val = juiz_b_row.get(coluna)
                if pd.notna(destino_val):
                    destino_limpo = str(destino_val).strip()
                    if destino_limpo:
                        destinos_b.append(destino_limpo)
            
            # Para cada destino que B quer (posição C)
            for origem_c in destinos_b:
                
                # Encontrar juízes em origem_c
                juizes_c = df[df["Origem"].str.strip() == origem_c.strip()]
                
                for _, juiz_c_row in juizes_c.iterrows():
                    juiz_c_nome = str(juiz_c_row.get("Nome", "")).strip()
                    
                    # Destinos que C quer
                    destinos_c = []
                    for coluna in ["Destino 1", "Destino 2", "Destino 3"]:
                        destino_val = juiz_c_row.get(coluna)
                        if pd.notna(destino_val):
                            destino_limpo = str(destino_val).strip()
                            if destino_limpo:
                                destinos_c.append(destino_limpo)
                    
                    # Para cada destino que C quer (posição D)
                    for origem_d in destinos_c:
                        
                        # Encontrar juízes em origem_d
                        juizes_d = df[df["Origem"].str.strip() == origem_d.strip()]
                        
                        for _, juiz_d_row in juizes_d.iterrows():
                            juiz_d_nome = str(juiz_d_row.get("Nome", "")).strip()
                            
                            # Destinos que D quer
                            destinos_d = []
                            for coluna in ["Destino 1", "Destino 2", "Destino 3"]:
                                destino_val = juiz_d_row.get(coluna)
                                if pd.notna(destino_val):
                                    destino_limpo = str(destino_val).strip()
                                    if destino_limpo:
                                        destinos_d.append(destino_limpo)
                            
                            # VERIFICAÇÃO CRÍTICA: D quer ir para onde o usuário está?
                            if origem_user.strip() in destinos_d:
                                
                                # QUADRANGULAÇÃO VÁLIDA!
                                quadrangulo = {
                                    "Juiz A": usuario_nome,
                                    "Entrância A": str(usuario_row.get("Entrância", "")).strip(),
                                    "Origem A": origem_user.strip(),
                                    "A ➝": origem_b.strip(),
                                    "Juiz B": juiz_b_nome,
                                    "Entrância B": str(juiz_b_row.get("Entrância", "")).strip(),
                                    "Origem B": origem_b.strip(),
                                    "B ➝": origem_c.strip(),
                                    "Juiz C": juiz_c_nome,
                                    "Entrância C": str(juiz_c_row.get("Entrância", "")).strip(),
                                    "Origem C": origem_c.strip(),
                                    "C ➝": origem_d.strip(),
                                    "Juiz D": juiz_d_nome,
                                    "Entrância D": str(juiz_d_row.get("Entrância", "")).strip(),
                                    "Origem D": origem_d.strip(),
                                    "D ➝": origem_user.strip()
                                }
                                quadrangulos.append(quadrangulo)
    
    return quadrangulos