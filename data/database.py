import sqlite3
import pandas as pd

class SegurDatabase:
    def __init__(self, db_path='data/incidentes.db'):
        self.db_path = db_path
        self._init_tables()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_tables(self):
        with self._get_connection() as con:
            cursor = con.cursor()
            cursor.execute('''
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
            ''')

            cursor.execute('''
                CREATRE TABLE IF NOT EXISTS inpecoes(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    data_inspecao TEXT NOT NULL, 
                    equipamento TEXT NOT NULL,
                    inspetor TEXT NOT NULL,
                    resultado TEXT NOT NULL,
                    observacoes TEXT NOT NULL
                )
            ''')
            con.commit()
            #LEMBRAR DE TRATAR OS TIPOS DE COLUNAS!!!!


class GestaoIncidentes(SegurDatabase):
    def salvar_incidente(self, data_evento, hora_evento, setor, gravidade, usuario, descricao):
        sql = '''
            INSERT INTO incidentes (data_evento, hora_evento, setor, gravidade, usuario, descricao)
            VALUES(?, ?, ?, ?, ?, ?)
        '''
        with self._get_connection() as con:
            con.cursor().execute(sql, (str(data_evento), str(hora_evento), setor, int(gravidade), usuario, descricao))
            con.commit()

    def carregar_incidentes(self):
        with self._get_connection() as con:
            df = pd.read_sql_query('SELECT * FROM incidentes', con)
            con.close()

        df['data_evento'] = pd.to_datetime(df['data_evento'])
        df['gravidade'] = pd.to_numeric(df['gravidade'], errors='coerce')
        df['hora_num'] = pd.to_datetime(df['hora_evento'], format='%H:%M:%S').dt.hour
        return df

    def excluir_incidente(self, id_registro):
        with self._get_connection() as con:
            con.cursor().execute("DELETE FROM incidentes WHERE id = ?", (id_registro))
            con.commit()

class GestaoInspecoes(SegurDatabase):
    def salvar_checklist(self, equipamento, usuario, resultado, obs):
        sql = '''
            INSERT INTO inspecoes (equipamento, usuario, resultado, observacoes)
            VALUES(?, ?, ?, ?)
            '''
        
        with self._get_connection() as con:
            con.cursor().execute(sql, (equipamento, usuario, resultado, obs))
            con.commit()

    def carregar_inspecoes(self):
        with self._get_connection() as con:
            return pd.read_sql_query("SELECT * FROM inspecoes ORDER BY data_inspecao DESC", con)
