import sqlite3
import pandas as pd

def init_db():
    con = sqlite3.connect('data/incidentes.db')
   
    cursor = con.cursor()
    
    sql = '''
    CREATE TABLE IF NOT EXISTS incidentes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        setor TEXT NOT NULL,
        gravidade INTEGER NOT NULL,
        usuario TEXT NOT NULL,
        descricao TEXT NOT NULL
    )
    '''

    cursor.execute(sql)
    
    con.commit()
    con.close()

def salvar_dados(setor, descricao, gravidade, usuario):
    con = sqlite3.connect('data/incidentes.db')
    cursor = con.cursor()

    sql = '''
    INSERT INTO incidentes (setor, gravidade, usuario, descricao)
    VALUES(?, ?, ?, ?)
    '''

    dados = (setor, gravidade, usuario, descricao)
    cursor.execute(sql, dados)

    con.commit()
    con.close()

def excluir_registro(id_registro):  
    con = sqlite3.connect('data/incidentes.db')
    cursor = con.cursor()

    sql = '''DELETE FROM incidentes WHERE id = ?'''

    cursor.execute(sql, (id_registro))

    con.commit()
    con.close()

def carregar_dados():
    con = sqlite3.connect('data/incidentes.db')
    df = pd.read_sql_query("SELECT * FROM incidentes", con)
    con.close()
    return df