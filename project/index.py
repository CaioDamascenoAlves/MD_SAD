import sqlite3
import pandas as pd
conn = sqlite3.connect("epidemiology.db")
cursor = conn.cursor()

df = pd.read_csv("project\data\caso_full.csv")
# criar tabela 'estados'
cursor.execute("""
    CREATE TABLE IF NOT EXISTS estados (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL
    )
""")

df_states = df.drop_duplicates(subset=["state"])
for i, row in df_states.iterrows():
    cursor.execute("""
        INSERT INTO estados (id, nome)
        VALUES (?,?)
    """, (i, row["state"]))
    
# criar tabela 'cidades'
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cidades (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        codigo_ibge INTEGER,
        id_estado INTEGER NOT NULL,
        FOREIGN KEY (id_estado) REFERENCES estados(id)
    )
""")

df_cities = df.drop_duplicates(subset=["city", "city_ibge_code"])
for i, row in df_cities.iterrows():
    id_state = df_states[df_states["state"] == row["state"]].index[0]
    cursor.execute("""
        INSERT INTO cidades (id, nome, codigo_ibge, id_estado)
        VALUES (?,?,?,?)
    """, (i, row["city"], row["city_ibge_code"], id_state))

# criar tabela 'dados_epidemiologicos'
cursor.execute("""
CREATE TABLE IF NOT EXISTS dados_epidemiologicos (
id INTEGER PRIMARY KEY,
id_cidade INTEGER NOT NULL,
data TEXT NOT NULL,
semana_epidemiologica INTEGER NOT NULL,
populacao_estimada INTEGER NOT NULL,
populacao_estimada_2019 INTEGER NOT NULL,
ultimo_disponivel INTEGER NOT NULL,
repetido INTEGER NOT NULL,
casos_confirmados_ultimo_disponivel INTEGER NOT NULL,
casos_confirmados_ultimo_disponivel_por_100k REAL NOT NULL,
data_ultimo_disponivel TEXT NOT NULL,
taxa_obitos_ultimo_disponivel REAL NOT NULL,
obitos_ultimo_disponivel INTEGER NOT NULL,
ordem_local INTEGER NOT NULL,
tipo_local TEXT NOT NULL,
novos_casos_confirmados INTEGER NOT NULL,
novos_obitos INTEGER NOT NULL,
FOREIGN KEY (id_cidade) REFERENCES cidades(id)
)
""")

df_epid = df.drop_duplicates(subset=["city", "date"])
for i, row in df_epid.iterrows(): id_city = df_cities[(df_cities["city"] == row["city"]) & (df_cities["city_ibge_code"] == row["city_ibge_code"])].index[0]
cursor.execute("""
INSERT INTO dados_epidemiologicos (id, id_cidade, data, semana_epidemiologica, populacao_estimada, populacao_estimada_2019, ultimo_disponivel, repetido, casos_confirmados_ultimo_disponivel, casos_confirmados_ultimo_disponivel_por_100k, data_ultimo_disponivel, taxa_obitos_ultimo_disponivel, obitos_ultimo_disponivel, ordem_local, tipo_local, novos_casos_confirmados, novos_obitos)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (i, id_city, row["date"], row["epidemiological_week"], row["estimated_population_2019"], row["estimated_population_2019"], row["last_available_confirmed"], row["last_available_confirmed_per_100k_inhabitants"], row["last_available_date"], row["last_available_death_rate"], row["last_available_deaths"], row["order_for_place"], row["place_type"], row["new_confirmed"], row["new_deaths"]))
