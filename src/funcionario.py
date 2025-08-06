from dataclasses import dataclass
from datetime import date
from typing import Optional

from src.carreira import Progressao, Carreira, CarreiraAtual
from src.classe import Classe
from src.nivel import Nivel


@dataclass
class Registro:
    cm: int
    classe: Classe
    data_anuenio: date
    num_ats: int
    procurador: bool


@dataclass
class Aposentadoria:
    data_aposentadoria: date
    num_art_98_data_aposentadoria: int


class Funcionario:
    def __init__(
        self,
        registro: Registro,
        aposentadoria: Aposentadoria,
        ultima_progressao: Progressao,
        carreira: Carreira,
    ):
        self.registro = registro
        self.aposentadoria = aposentadoria
        self.progressoes = [ultima_progressao]
        self.carreira = carreira

    def _concede_letras(self) -> bool:
        """Concede todas as letras se a pessoa tiver na letra máxima do nível,
        mas não concede nenhuma caso contrário."""

        nivel_atual = self.progressoes[0].nivel
        nivel_letra_maxima = CarreiraAtual().concede_letras_ate_limite(nivel_atual)

        if (
            nivel_letra_maxima.numero_progressoes_horizontais
            - nivel_atual.numero_progressoes_horizontais
            > 0
        ):
            return False
        return True

    def _calcula_progressoes_ate(self, data: date):
        ultima_progressao = self.progressoes[-1]

        concede_letras = self._concede_letras()
        while ultima_progressao and data > ultima_progressao.data:
            if concede_letras:
                ultima_progressao = (
                    self.carreira.progride_verticalmente_e_horizontalmente(
                        ultima_progressao
                    )
                )
            else:
                ultima_progressao = self.carreira.progride_verticalmente(
                    ultima_progressao
                )

            if ultima_progressao:
                self.progressoes.append(ultima_progressao)

    def obtem_nivel_para(self, data: date) -> Optional[Nivel]:
        """Retorna o nível que o servidor estará em determinada data.
        Se tiver aposentado, retorna None"""
        if data >= self.aposentadoria.data_aposentadoria:
            return None

        self._calcula_progressoes_ate(data)

        for progressao in reversed(self.progressoes):
            dt_prog = progressao.data
            if dt_prog < data or (
                dt_prog.month == data.month and dt_prog.year == data.year
            ):
                return progressao.nivel
