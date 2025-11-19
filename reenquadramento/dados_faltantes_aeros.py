from dataclasses import dataclass

import pandas as pd

from src.banco_de_dados import BancoDeDados


@dataclass
class DadosFaltantesAeros:
    nome: str
    qtde_dias_licenca: int
    letra_maxima: str


def obtem_dados_faltantes_aeros() -> dict[int, DadosFaltantesAeros]:
    """
    Obtém dados faltantes do Aeros para o reenquadramento.
    Retorna um dicionário com os dados necessários.
    """
    df_dados_faltantes = BancoDeDados().realiza_consulta_arquivo(
        "dados_faltantes_reenquadramento.sql"
    )

    dados_faltantes_aeros = {}
    for _, row in df_dados_faltantes.iterrows():
        cm: int = int(row["cm"])
        nome: str = row["nome"]
        qtde_dias_licenca: int = int(
            row["qtde_dias_licenca"] if not pd.isna(row["qtde_dias_licenca"]) else 0
        )
        letra_maxima: str = row["letra_maxima"]
        if letra_maxima == "BASE" or pd.isna(letra_maxima):
            letra_maxima = "0"

        dados_faltantes_aeros[cm] = DadosFaltantesAeros(
            nome=nome,
            qtde_dias_licenca=qtde_dias_licenca,
            letra_maxima=letra_maxima,
        )

    dados_faltantes_aeros[545].qtde_dias_licenca = 680

    return dados_faltantes_aeros
