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
        """Caso deva ser respeitada uma letra máxima para o funcionário, retorna essa letra.
        Caso possa ter todas as progressões, retorna None."""
        if cm not in self.letras_adquiridas:
            return None  # Pode ter todas as letras
        if self._concede_letras(cm):
            return None  # Pode ter todas as letras
        return self.letras_adquiridas.get(cm, None)  # limita às letras adquiridas

    def _concede_letras(self, cm: int) -> bool:

        if config.param.CONCEDE_NOVAS_LETRAS:
            return self._possui_todas_as_letras_permitidas(cm)
        return False  # Limita a letra à atual adquirida

    def _possui_todas_as_letras_permitidas(self, cm: int) -> bool:
        """Permite que o funcionário tenha novas letras se possuir todas as letras permitidas pelo
        nível atual. Caso contrário, não permite novas letras."""
        nivel_atual = self.nivel_atual.get(cm, 0)
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
