import psycopg2
import json
import pandas as pd


class BancoDeDados:
    def __init__(self, config_path="db_config.json"):
        """Inicializa a classe do banco de dados."""
        with open(config_path, "r") as f:
            self.dados_conexao = json.load(f)

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
