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


def ver_conteudo():
    # 1. Conecta
    con = sqlite3.connect('data/incidentes.db')
    cursor = con.cursor()
    
    # 2. Executa a busca (O * significa "todas as colunas")
    cursor.execute("SELECT * FROM incidentes")
    
    # 3. Recupera todos os resultados
    linhas = cursor.fetchall()
    
    # 4. Exibe de forma organizada
    print("\n--- CONTEÚDO DA TABELA INCIDENTES ---")
    for linha in linhas:
        print(linha)
    
    con.close()

conexao_db('data/incidentes.db')
excluir_registro('3')

ver_conteudo()