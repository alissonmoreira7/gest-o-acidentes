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
        descricao TEXT NOT NULL,
        gravidade INTEGER NOT NULL
    )
    '''

    cursor.execute(sql)
    
    con.commit()
    con.close()
    print('Tabela criada com sucesso!')

def salvar_dados(setor, descricao, gravidade):
    con = sqlite3.connect('data/incidentes.db')
    cursor = con.cursor()

    sql = '''
    INSERT INTO incidentes (setor, descricao, gravidade)
    VALUES(?, ?, ?)
    '''

    dados = (setor, descricao, gravidade)
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