import sqlite3
import pandas as pd

def init_db():
    con = sqlite3.connect('data/incidentes.db')
   
    cursor = con.cursor()
    
    sql = '''
    CREATE TABLE IF NOT EXISTS incidentes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        data_evento TEXT NOT NULL,                      
        hora_evento TEXT NOT NULL,
        setor TEXT NOT NULL,
        gravidade INTEGER NOT NULL,
        usuario TEXT NOT NULL,
        descricao TEXT NOT NULL
    )
    '''

    cursor.execute(sql)
    
    con.commit()
    con.close()

def salvar_dados(data_evento, hora_evento, setor, gravidade, usuario, descricao):
    con = sqlite3.connect('data/incidentes.db')
    cursor = con.cursor()

    sql = '''
    INSERT INTO incidentes (data_evento, hora_evento, setor, gravidade, usuario, descricao)
    VALUES(?, ?, ?, ?, ?, ?)
    '''

    dados = (str(data_evento), str(hora_evento), setor, int(gravidade), usuario, descricao)
    
    cursor.execute(sql, dados)
    con.commit()
    con.close()

def excluir_registro(id_registro):  
    con = sqlite3.connect('data/incidentes.db')
    cursor = con.cursor()

    sql = '''DELETE FROM incidentes WHERE id = ?'''

    cursor.execute(sql, (id_registro,))

    con.commit()
    con.close()

def carregar_dados():
    con = sqlite3.connect('data/incidentes.db')
    df = pd.read_sql_query("SELECT * FROM incidentes", con)
    con.close()

    if not df.empty:
        df['data_evento'] = pd.to_datetime(df['data_evento'])

        df['gravidade'] = pd.to_numeric(df['gravidade'], errors='coerce')

        df['hora_num'] = pd.to_datetime(df['hora_evento'], format='%H:%M:%S').dt.hour

    return df