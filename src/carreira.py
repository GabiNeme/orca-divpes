from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Optional

from dateutil.relativedelta import relativedelta

from src.cargo import Classe, Nivel
from src.intersticio import Intersticio


@dataclass
class Progressao:
    data: date
    nivel: Nivel


class Carreira(ABC):
    def __init__(self, classe: Classe) -> None:
        self.classe = classe

    def progride_verticalmente(
        self, ultima_progressao: Progressao, especial: bool
    ) -> Optional[Progressao]:
        """Calcula uma progressão vertical (2 interstícios), podendo ser especial
        ou não."""

        self.checa_nivel_valido(ultima_progressao.nivel)
        limite = self.limite(ultima_progressao.nivel)

        if ultima_progressao.nivel.numero == limite:
            return None

        intersticio = Intersticio.tempo_para_progredir(ultima_progressao.nivel, 2)
        dt_prox_prog = ultima_progressao.data + relativedelta(months=intersticio)

        if especial:
            num_niveis = 3
        else:
            num_niveis = 2

        if num_niveis + ultima_progressao.nivel.numero > limite:
            num_niveis = limite - ultima_progressao.nivel.numero

        return Progressao(dt_prox_prog, ultima_progressao.nivel.proximo(num_niveis, 0))

    def progride_verticalmente_e_horizontalmente(
        self, ultima_progressao: Progressao, especial: bool
    ) -> Optional[Progressao]:
        """Calcula uma progressão vertical (2 interstícios), podendo ser especial ou
        não, e concede todas as letras permitidas pelo nível final."""

        progressao = self.progride_verticalmente(ultima_progressao, especial)

        if not progressao:
            return None

        nivel_com_letras = self.concede_letras_ate_limite(progressao.nivel)
        return Progressao(progressao.data, nivel_com_letras)

    def concede_letras_ate_limite(self, nivel_origem: Nivel) -> Nivel:
        """Concede progressões veriticais até o máximo permitido por aquele nível
        vertical."""

        self.checa_nivel_valido(nivel_origem)

        letra_maxima = self._letra_maxima_para_nivel(nivel_origem.numero)
        return Nivel(nivel_origem.numero, letra_maxima)

    @abstractmethod
    def _letra_maxima_para_nivel(self, numero_nivel: int) -> str:
        raise NotImplementedError

    @abstractmethod
    def checa_nivel_valido(self, nivel: Nivel) -> bool:
        raise NotImplementedError

    @abstractmethod
    def limite(self, nivel: Nivel = None) -> int:
        raise NotImplementedError


class Carreira2004(Carreira):
    def limite(self, nivel: Nivel = None) -> int:
        if self.classe == Classe.E2:
            return 37
        if self.classe == Classe.E3:
            return 36

    def _letra_maxima_para_nivel(self, numero_nivel: int) -> str:
        """Retorna a máxima letra que é possível ter para um determinado nível."""

        transicao_para_letra = [
            (1, "A"),
            (7, "B"),
            (13, "C"),
            (19, "D"),
            (25, "E"),
        ]

        for i in reversed(range(len(transicao_para_letra))):
            if transicao_para_letra[i][0] <= numero_nivel:
                return transicao_para_letra[i][1]

    def checa_nivel_valido(self, nivel: Nivel):
        """Lança uma exceção se o nível informado for inválido."""

        def numero_invalido(numero_nivel: int) -> bool:
            if numero_nivel > self.limite(nivel):
                return True
            return False

        def letra_invalida(nivel: Nivel) -> bool:
            letra_max = self._letra_maxima_para_nivel(nivel.numero)
            nivel_hor_max = Nivel(nivel.numero, letra_max)

            if (
                nivel.numero_progressoes_horizontais
                > nivel_hor_max.numero_progressoes_horizontais
            ):
                return True
            return False

        if numero_invalido(nivel.numero) or letra_invalida(nivel):
            raise (ValueError("O nível " + str(nivel) + " não existe nessa carreira."))
