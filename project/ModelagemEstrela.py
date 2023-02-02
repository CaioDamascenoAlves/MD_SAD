import sqlite3
import psycopg2

# conectando ao banco de dados SQLite
conn = sqlite3.connect("dados_epidemiologicos_NN_F.db")
cursor = conn.cursor()

# recuperando os dados da tabela SQLite
cursor.execute("SELECT * FROM dados_epidemiologicos")
data = cursor.fetchall()

# Conectando ao servidor de banco de dados PostgreSQL
conn2 = psycopg2.connect("dbname=postgres user=postgres password=postgres host=localhost port=5432")
conn2.autocommit = True
cursor2 = conn2.cursor()

# Criando um novo banco de dados PostgreSQL
cursor2.execute("DROP DATABASE IF EXISTS bdmodelstar")
cursor2.execute("CREATE DATABASE bdstarmodel")
conn2.commit()

# conectando ao novo banco de dados PostgreSQL
conn2 = psycopg2.connect("dbname=bdstarmodel user=postgres password=postgres host=localhost port=5432")
cursor2 = conn2.cursor()

# criando tabelas de dimensão
cursor2.execute("""
CREATE TABLE city (
    city_id SERIAL PRIMARY KEY,
    city_name TEXT NOT NULL
);
""")

cursor2.execute("""
CREATE TABLE state (
    state_id SERIAL PRIMARY KEY,
    state_name TEXT NOT NULL
);
""")

cursor2.execute("""
CREATE TABLE place_type (
    place_type_id SERIAL PRIMARY KEY,
    place_type_name TEXT NOT NULL
);
""")

# criando tabela de fato de data

cursor2.execute("""
CREATE TABLE date (
date_id SERIAL PRIMARY KEY,
date TEXT NOT NULL,
epidemiological_week INTEGER NOT NULL
);
""")

# criando tabela de fato de dados

cursor2.execute("""
CREATE TABLE fact (
fact_id SERIAL PRIMARY KEY,
city_id INTEGER REFERENCES city(city_id),
state_id INTEGER REFERENCES state(state_id),
place_type_id INTEGER REFERENCES place_type(place_type_id),
date_id INTEGER REFERENCES date(date_id),
new_confirmed INTEGER NOT NULL,
new_deaths INTEGER NOT NULL
);
""")

def populate_tables(data):
    city_dict = {}
    state_dict = {}
    place_type_dict = {} 
    date_dict = {}
    
    for row in data:
        # recuperando informações da linha
        city_name = row[0]
        state_name = row[1]
        place_type_name = row[2]
        date = row[3]
        epidemiological_week = row[4]
        new_confirmed = row[5]
        new_deaths = row[6]

        # verificando se a cidade já está no dicionário
        if city_name not in city_dict:
            cursor2.execute("INSERT INTO city (city_name) VALUES (%s) RETURNING city_id", (city_name,))
            city_id = cursor2.fetchone()[0]
            city_dict[city_name] = city_id
        else:
            city_id = city_dict[city_name]

        # verificando se o estado já está no dicionário
        if state_name not in state_dict:
            cursor2.execute("INSERT INTO state (state_name) VALUES (%s) RETURNING state_id", (state_name,))
            state_id = cursor2.fetchone()[0]
            state_dict[state_name] = state_id
        else:
            state_id = state_dict[state_name]

        # verificando se o tipo de local já está no dicionário
        if place_type_name not in place_type_dict:
            cursor2.execute("INSERT INTO place_type (place_type_name) VALUES (%s) RETURNING place_type_id", (place_type_name,))
            place_type_id = cursor2.fetchone()[0]
            place_type_dict[place_type_name] = place_type_id
        else:
            place_type_id = place_type_dict[place_type_name]
        # verificando se o data já está no dicionário
        if date not in date_dict:
            cursor2.execute("INSERT INTO date (date, epidemiological_week) VALUES (%s,%s) RETURNING date_id", (date,epidemiological_week))
            date_id = cursor2.fetchone()[0]
            date_dict[date] = date_id
        else:
            date_id = date_dict[date]

        # inserindo informações na tabela de fato
        cursor2.execute("INSERT INTO fact (city_id, state_id, place_type_id, new_confirmed, new_deaths) VALUES (%s, %s, %s, %s, %s)", (city_id, state_id, place_type_id, new_confirmed, new_deaths))

    conn2.commit()

populate_tables(data)
