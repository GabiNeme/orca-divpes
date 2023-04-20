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


class Carreira2004:
    def __init__(self, classe: Classe) -> None:
        if classe == Classe.E2:
            self.limite = 37
            self.transicao_para_letra = [
                (1, "A"),
                (7, "B"),
                (13, "C"),
                (19, "D"),
                (27, "E"),
            ]
        elif classe == Classe.E3:
            self.limite = 36
            self.transicao_para_letra = [
                (1, "A"),
                (7, "B"),
                (13, "C"),
                (19, "D"),
                (25, "E"),
            ]

    def progride_verticalmente(
        self, ultima_progressao: Progressao, especial: bool
    ) -> Optional[Progressao]:
        """Calcula uma progressão vertical (2 interstícios), podendo ser especial
        ou não."""

        self.checa_nivel_valido(ultima_progressao.nivel)

        if ultima_progressao.nivel.numero == self.limite:
            return None

        intersticio = Intersticio.tempo_para_progredir(ultima_progressao.nivel, 2)
        dt_prox_prog = ultima_progressao.data + relativedelta(months=intersticio)

        if especial:
            num_niveis = 3
        else:
            num_niveis = 2

        if num_niveis + ultima_progressao.nivel.numero > self.limite:
            num_niveis = self.limite - ultima_progressao.nivel.numero

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

    def _letra_maxima_para_nivel(self, numero_nivel: int) -> str:
        """Retorna a máxima letra que é possível ter para um determinado nível."""

        for i in reversed(range(len(self.transicao_para_letra))):
            if self.transicao_para_letra[i][0] <= numero_nivel:
                return self.transicao_para_letra[i][1]

    def checa_nivel_valido(self, nivel: Nivel):
        """Lança uma exceção se o nível informado for inválido."""

        def numero_invalido(numero_nivel: int) -> bool:
            if numero_nivel > self.limite:
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

    def progressao_vertical_anterior(self, progressao: Progressao):
        """Calcula a progressão que aconteceu imediatamente antes da informada."""

        self.checa_nivel_valido(progressao.nivel)

        dois_niveis_atras = progressao.nivel.anterior(2, 0)
        intersticio = Intersticio.tempo_para_progredir(dois_niveis_atras, 2)
        dt_prog_anterior = progressao.data - relativedelta(months=intersticio)

        return Progressao(dt_prog_anterior, dois_niveis_atras)
