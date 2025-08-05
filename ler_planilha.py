import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Etapa 1: Autenticar e acessar planilha
escopos = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

credenciais = ServiceAccountCredentials.from_json_keyfile_name(
    "credenciais.json",
    escopos
)

cliente = gspread.authorize(credenciais)
planilha = cliente.open("Permuta - Magistratura Estadual")
aba = planilha.sheet1

# Etapa 2: Obter e transformar dados em DataFrame
dados = aba.get_all_values()
colunas = dados[0]
linhas = dados[1:]

df = pd.DataFrame(linhas, columns=colunas)

# Etapa 3: Padronizar valores vazios → None
for coluna in ["Destino 1", "Destino 2", "Destino 3"]:
    df[coluna] = df[coluna].apply(lambda x: x.strip() if x.strip() != "" else None)

# Também podemos limpar espaços extras em todas as colunas
df["Nome"] = df["Nome"].str.strip()
df["Origem"] = df["Origem"].str.strip()

# Ver resultado
print("🔍 Dados tratados:")
print(df)
