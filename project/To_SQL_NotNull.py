import pandas as pd
import sqlite3

# Criar conexão com o banco de dados
conn = sqlite3.connect("dados_epidemiologicos_NN_F.db")

# Ler o arquivo CSV
df = pd.read_csv("project\data\caso_full.csv")

# Remover valores nulos
df.dropna(inplace=True)

# Inserir os dados no esquema relacional
df.to_sql("dados_epidemiologicos", conn, if_exists="replace", index=False)

# Fechar conexão com o banco de dados
conn.close()
