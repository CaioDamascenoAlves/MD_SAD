# MD_SAD
## Metodologia Star Schema
#### Este projeto é destinado à conversão do dataset da covid-19 no brasil .CSV  em banco de dados SQLite e PostgreSQL, além da criação de uma modelagem dimensional tipo estrela, migração dos dados e população do novo esquema dimensional.
## Requisitos
### 
    Python 3.x
    Biblioteca Pandas
    Biblioteca SQLAlchemy
    SQLite ou PostgreSQL
## Instalação
    Clone este repositório em sua máquina local
    Baixe o data set: https://data.brasil.io/dataset/covid19/caso_full.csv.gz
    
## Uso

    Colocar o arquivo csv na pasta raíz do projeto.
    Abrir o terminal na pasta raíz do projeto.
    Executar primeiro o artivo To_SQL_NotNull.py
    Depois executar o Modelagem.py
## Resultado
  O script irá criar uma nova base de dados SQLite ou PostgreSQL, com a modelagem dimensional tipo estrela, migrar os dados do arquivo csv e popular o novo esquema dimensional.
## Contribuição
  Contribuições são sempre bem-vindas. Para contribuir, basta abrir uma pull request com suas alterações.
