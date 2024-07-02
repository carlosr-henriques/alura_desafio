from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
import pandas as pd
import pyodbc as py
import urllib
import json
import os

load_dotenv(dotenv_path=find_dotenv(),  # Or BASE_DIR/'.env',
            verbose=True,               # Print verbose output for debugging purposes
            override=True)

SERVER = os.getenv("MSSQL_SERVER")
PORT = os.getenv("MSSQL_PORT")
DATABASE = os.getenv("MSSQL_DATABASE")
USERNAME = os.getenv("MSSQL_USER")
PASSWORD = os.getenv("MSSQL_PASSWORD")

def connection_mssql_pyodbc():
    connectionString = f"DRIVER={'ODBC Driver 17 for SQL Server'};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}"

    connection = py.connect(connectionString)
    cur = connection.cursor()

    return connection, cur

def create_database():

    """
    Utilizado o pyodbc + T-SQL para a criação da tabela. Poderia ser feito com ORM, aproveitando a conexão com o SQLAlchemy, porém, devido a falta de conhecimento da ferramenta, optei pela opção mais segura.
    """

    create_table = """
        IF OBJECT_ID('dbo.feedback', 'U') IS NULL
            BEGIN
                CREATE TABLE dbo.feedback
                (
                    id_feedback VARCHAR(255) NOT NULL,
                    sentiment  VARCHAR(8000) NOT NULL,
                    code VARCHAR(8000) NOT NULL,
                    reason VARCHAR(8000) NOT NULL,
                    date_transaction DATETIME default (CURRENT_TIMESTAMP) NOT NULL,
                    CONSTRAINT pk_feedback PRIMARY KEY (id_feedback)
                );
            END
    """
    
    con, cur = connection_mssql_pyodbc()

    cur.execute(create_table)
    con.close()

    print("Tabela criada ou já existente.")

def select():

    query = F"""
        SELECT
            [id_feedback]
            ,[sentiment]
            ,[code]
            ,[reason]
            ,[date_transaction]
        FROM
            {DATABASE}.[dbo].[feedback]
"""
    con, cur = connection_mssql_pyodbc()
    df = pd.read_sql(query, con)

    return df



def insert(data: dict):

    """
    con : sqlalchemy.engine.(Engine or Connection) or sqlite3.Connection
        Using SQLAlchemy makes it possible to use any DB supported by that library. Legacy support is provided for sqlite3.Connection objects. The user is responsible for engine disposal and connection closure for the SQLAlchemy connectable.

    Portanto, foi necessário usar o SQLAlchemy nesta etapa, diferente da etapa de criação do banco, feita com pyodbc.
    """
    id_ = data[0]["id"]
    sentiment = data[0]["sentiment"]
    code = data[0]["requested_features"][0]["code"]
    reason = data[0]["requested_features"][0]["reason"]

    df = pd.DataFrame(
        {
            "id_feedback": [id_],
            "sentiment": [sentiment],
            "code": [code],
            "reason": [reason],

        }
    )

    params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                 f"SERVER={SERVER};"
                                 f"DATABASE={DATABASE};"
                                 f"UID={USERNAME};"
                                 f"PWD={PASSWORD}")
    engine = create_engine(f"mssql+pyodbc://?odbc_connect={params}", echo=False)

    df.to_sql(name="feedback", con=engine, index=False, if_exists='append')

    print("Dados inseridos")