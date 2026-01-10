import sqlite3

def conexao_db(nome_banco):
    con = sqlite3.connect(nome_banco)
   
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

conexao_db('data/incidentes.db')