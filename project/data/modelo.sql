-- Criar tabela de estados
CREATE TABLE estados (
  id INTEGER PRIMARY KEY,
  nome TEXT NOT NULL
);

-- Criar tabela de cidades
CREATE TABLE cidades (
  id INTEGER PRIMARY KEY,
  nome TEXT NOT NULL,
  codigo_ibge TEXT NOT NULL,
  id_estado INTEGER,
  FOREIGN KEY (id_estado) REFERENCES estados(id)
);

-- Criar tabela de dados epidemiológicos
CREATE TABLE dados_epidemiologicos (
  id INTEGER PRIMARY KEY,
  id_cidade INTEGER,
  data DATE NOT NULL,
  semana_epidemiologica INTEGER NOT NULL,
  populacao_estimada REAL NOT NULL,
  populacao_estimada_2019 REAL NOT NULL,
  ultimo_disponivel BOOLEAN NOT NULL,
  repetido BOOLEAN NOT NULL,
  casos_confirmados_ultimo_disponivel INTEGER NOT NULL,
  casos_confirmados_ultimo_disponivel_por_100k INTEGER NOT NULL,
  data_ultimo_disponivel DATE NOT NULL,
  taxa_obitos_ultimo_disponivel REAL NOT NULL,
  obitos_ultimo_disponivel INTEGER NOT NULL,
  ordem_local INTEGER NOT NULL,
  tipo_local TEXT NOT NULL,
  novos_casos_confirmados INTEGER NOT NULL,
  novos_obitos INTEGER NOT NULL,
  FOREIGN KEY (id_cidade) REFERENCES cidades(id)
);
