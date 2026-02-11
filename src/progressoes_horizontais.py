import pandas as pd

import config
from src.banco_de_dados import BancoDeDados
from src.carreira import CarreiraAtual
from src.nivel import Nivel


class ProgressoesHorizontais:
    def __init__(self, banco_de_dados: BancoDeDados = BancoDeDados) -> None:
        self.banco_de_dados = banco_de_dados
        self.letras_adquiridas = {}  # type: dict[int, str]
        self.nivel_atual = {}  # type: dict[int, int]
        self._extrai_do_aeros_letra_maxima()

    def _extrai_do_aeros_letra_maxima(self) -> None:
        df_dados_faltantes = self.banco_de_dados().realiza_consulta_arquivo(
            "progressoes.sql"
        )

        for _, row in df_dados_faltantes.iterrows():
            cm: int = int(row["cm"])
            letras_adquiridas: str = row["letras_adquiridas"]
            if letras_adquiridas == "BASE" or pd.isna(letras_adquiridas):
                letras_adquiridas = "0"
            self.letras_adquiridas[cm] = letras_adquiridas

            nivel_atual_str: str = row["nivel_atual"]
            if pd.isna(nivel_atual_str):
                nivel_atual = 1
            else:
                nivel_atual = int(nivel_atual_str)
            self.nivel_atual[cm] = nivel_atual

    def obtem_letra_maxima(self, cm: int) -> str | None:
        """Respeita a configuração geral de concessão de letras.
        No entanto, caso o funcionário não possua todas as letras permitidas
        para o seu nível atual, ele não receberá novas letras independente da configuração geral.

        Retorna None se o funcionário pode ter todas as letras.
        Retorna a letra máxima que o funcionário pode ter caso contrário."""

        possui_todas_letras_permitidas = self._possui_todas_as_letras_permitidas(cm)

        # Se o servidor não possui todas as letras permitidas, ele não irá ganhar
        # letras novas independente da configuração geral
        if not possui_todas_letras_permitidas:
            return self.letras_adquiridas.get(cm, "0")

        if config.param.CONCESSAO_LETRAS == config.ConcessaoLetras.NAO_CONCEDE:
            return self.letras_adquiridas.get(cm, "0")  # limita às letras adquiridas
        elif config.param.CONCESSAO_LETRAS == config.ConcessaoLetras.CONCEDE_UMA:
            letra_atual = self.letras_adquiridas.get(cm, "0")
            return Nivel.proxima_letra(letra_atual)
        elif config.param.CONCESSAO_LETRAS == config.ConcessaoLetras.CONCEDE_TODAS:
            return None  # pode ter todas as letras

    def _possui_todas_as_letras_permitidas(self, cm: int) -> bool:
        """Descobre se o funcionário já possui todas as letras permitidas para o seu nível atual."""
        nivel_atual = self.nivel_atual.get(cm, 1)
        letra_maxima_do_nivel_atual = CarreiraAtual().concede_letras_ate_limite(
            Nivel(nivel_atual, "0")
        )
        letras_adquiridas = self.letras_adquiridas.get(cm, "0")

        if (
            Nivel.nivel_horizontal_para_numero(letras_adquiridas)
            >= letra_maxima_do_nivel_atual.numero_progressoes_horizontais
        ):
            return True
        return False


progressoes_horizontais = ProgressoesHorizontais()
