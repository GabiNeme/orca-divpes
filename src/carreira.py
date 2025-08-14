from abc import ABC
from dataclasses import dataclass
from datetime import date
from typing import Optional

from dateutil.relativedelta import relativedelta

from src.nivel import Nivel
from src.intersticio import Intersticio


@dataclass
class Progressao:
    data: date
    nivel: Nivel
    progs_sem_especial: int = 0


class Carreira(ABC):
    def __init__(self) -> None:
        return

    def incrementa(self, progs_sem_especial: int) -> int:
        """Incrementa a progressão especial (concede 1 a cada 2 progressões)."""
        return (progs_sem_especial + 1) % 2

    def progride_verticalmente_por_quantidade_de_niveis(
        self, ultima_progressao: Progressao, numero_niveis: int
    ) -> Optional[Progressao]:
        """Calcula uma progressão vertical (2 interstícios), permitindo definir quantos
        níveis serão progredidos."""

        self.checa_nivel_valido(ultima_progressao.nivel)
        limite = self._limite()

        if ultima_progressao.nivel.numero >= limite:
            return None

        intersticio = Intersticio.tempo_para_progredir(ultima_progressao.nivel, 2)
        dt_prox_prog = ultima_progressao.data + relativedelta(months=intersticio)

        if numero_niveis + ultima_progressao.nivel.numero > limite:
            numero_niveis = limite - ultima_progressao.nivel.numero

        return Progressao(
            dt_prox_prog,
            ultima_progressao.nivel.proximo(numero_niveis, 0),
            progs_sem_especial=self.incrementa(ultima_progressao.progs_sem_especial),
        )

    def progride_verticalmente(
        self, ultima_progressao: Progressao
    ) -> Optional[Progressao]:
        """Calcula uma progressão vertical (2 interstícios), podendo ser especial
        ou não."""

        if ultima_progressao.progs_sem_especial >= 1:
            niveis = 3
        else:
            niveis = 2

        return self.progride_verticalmente_por_quantidade_de_niveis(
            ultima_progressao, niveis
        )

    def progride_verticalmente_e_horizontalmente(
        self, ultima_progressao: Progressao
    ) -> Optional[Progressao]:
        """Calcula uma progressão vertical (2 interstícios), podendo ser especial ou
        não, e concede todas as letras permitidas pelo nível final."""

        progressao = self.progride_verticalmente(ultima_progressao)

        if not progressao:
            return None

        nivel_com_letras = self.concede_letras_ate_limite(progressao.nivel)
        return Progressao(
            progressao.data, nivel_com_letras, progressao.progs_sem_especial
        )

    def concede_letras_ate_limite(self, nivel_origem: Nivel) -> Nivel:
        """Concede progressões veriticais até o máximo permitido por aquele nível
        vertical."""

        self.checa_nivel_valido(nivel_origem)

        letra_maxima = self._letra_maxima_para_nivel(nivel_origem.numero)
        return Nivel(nivel_origem.numero, letra_maxima)

    def _limite(self) -> int:
        """Limite da carreira enquanto não completar condição de aposentadoria."""
        return 33

    def checa_nivel_valido(self, nivel: Nivel):
        """Lança uma exceção se o nível informado for inválido."""

        def numero_invalido(numero_nivel: int) -> bool:
            if numero_nivel > self._limite():
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

    def _letra_maxima_para_nivel(self, numero_nivel: int) -> str:
        """Retorna a máxima letra que é possível ter para um determinado nível."""

        transicao_para_letra = [
            (1, "A"),
            (3, "B"),
            (5, "C"),
            (7, "D"),
            (9, "E"),
        ]

        for i in reversed(range(len(transicao_para_letra))):
            if transicao_para_letra[i][0] <= numero_nivel:
                return transicao_para_letra[i][1]

class CarreiraConcurso2008(Carreira):
    """Carreira do concurso de 2008."""

    def _limite(self) -> int:
        """Limite da carreira enquanto não completar condição de aposentadoria."""
        return 35

class CarreiraConcurso2004(Carreira):
    """Carreira do concurso de 2004."""

    def _limite(self) -> int:
        """Limite da carreira enquanto não completar condição de aposentadoria."""
        return 37

class CarreiraAtual(Carreira):

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


def atribui_carreira(cm: int) -> Carreira:
    """Atribui a nova carreira ao funcionário com base no concurso."""
    if cm <= 336:
        return CarreiraConcurso2004()
    elif cm <= 545:
        return CarreiraConcurso2008()
    return Carreira()
