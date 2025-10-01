import psycopg2
import json
import pandas as pd
import os


class BancoDeDados:
    def __init__(self, config_path="db_config.json", sql_dir="sql"):
        """Inicializa a classe do banco de dados."""
        with open(config_path, "r") as f:
            self.dados_conexao = json.load(f)
        self.sql_dir = sql_dir

    def realiza_consulta(self, SQL: str) -> pd.DataFrame:
        """Realiza uma consulta SQL e retorna os resultados como um DataFrame do pandas."""
        conn = psycopg2.connect(**self.dados_conexao)
        cur = conn.cursor()
        cur.execute(SQL)
        columns = [desc[0] for desc in cur.description]
        results = cur.fetchall()
        cur.close()
        conn.close()
        return pd.DataFrame(results, columns=columns)

    def realiza_consulta_arquivo(self, sql_filename: str) -> pd.DataFrame:
        """Realiza uma consulta SQL a partir de um arquivo e retorna os resultados como DataFrame."""
        sql_path = os.path.join(self.sql_dir, sql_filename)
        with open(sql_path, "r", encoding="utf-8") as f:
            sql_query = f.read()
        return self.realiza_consulta(sql_query)
