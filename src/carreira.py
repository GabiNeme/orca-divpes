from abc import ABC
from dataclasses import dataclass
from datetime import date
from typing import Optional

from dateutil.relativedelta import relativedelta

from src.classe import Classe
from src.intersticio import Intersticio, IntersticioE2, IntersticioE3
from src.nivel import Nivel


@dataclass
class Progressao:
    data: date
    nivel: Nivel
    progs_sem_especial: int = 0


class Carreira(ABC):
    def __init__(self, intersticio: Intersticio = None) -> None:
        self.intersticio = intersticio

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

        intersticio = self.intersticio.tempo_para_progredir(ultima_progressao.nivel, 2)
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
        self, ultima_progressao: Progressao, letra_maxima: str = None
    ) -> Optional[Progressao]:
        """Calcula uma progressão vertical (2 interstícios), podendo ser especial ou
        não, e concede todas as letras permitidas pelo nível final se letra máxima for
        None. Caso contrário concede todas as letras permitidas até letra_maxima."""

        progressao = self.progride_verticalmente(ultima_progressao)

        if not progressao:
            return None

        if letra_maxima:
            nivel_com_letras = self.progride_ate_letra(progressao.nivel, letra_maxima)
        else:
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

    def progride_ate_letra(self, nivel_origem: Nivel, letra: str) -> Nivel:
        """Concede progressões horizontais até no máximo letra informada."""
        letra_solicitada_count: int = Nivel(
            nivel_origem.numero, letra
        ).numero_progressoes_horizontais

        # Não retrocede nível se a letra solicitada for menor que nível origem
        if nivel_origem.numero_progressoes_horizontais > letra_solicitada_count:
            return nivel_origem

        letra_maxima: str = self._letra_maxima_para_nivel(nivel_origem.numero)
        letra_maxima_count: int = Nivel(
            nivel_origem.numero, letra_maxima
        ).numero_progressoes_horizontais
        if letra_solicitada_count > letra_maxima_count:
            return Nivel(nivel_origem.numero, letra_maxima)

        return Nivel(nivel_origem.numero, letra)

    def _limite(self) -> int:
        """Limite da carreira enquanto não completar condição de aposentadoria."""
        return NotImplementedError("Método deve ser implementado em subclasses.")

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
            (6, "C"),
            (8, "D"),
            (11, "E"),
        ]

        for i in reversed(range(len(transicao_para_letra))):
            if transicao_para_letra[i][0] <= numero_nivel:
                return transicao_para_letra[i][1]


# Carreiras E2


class CarreiraE2(Carreira):
    """Carreira da classe E2."""

    def __init__(self) -> None:
        super().__init__(IntersticioE2())

    def _limite(self):
        return 32


class CarreiraE2Concurso2008(CarreiraE2):
    """Carreira do concurso de 2008."""

    def _limite(self) -> int:
        """Limite da carreira enquanto não completar condição de aposentadoria."""
        return 34


class CarreiraE2Concurso2004(CarreiraE2):
    """Carreira do concurso de 2004."""

    def _limite(self) -> int:
        """Limite da carreira enquanto não completar condição de aposentadoria."""
        return 36


class CarreiraE2PassaDoTetoAtual(CarreiraE2):
    """Carreira do concurso de 2004 que passa do teto atual."""

    def _limite(self) -> int:
        """Limite da carreira enquanto não completar condição de aposentadoria."""
        return 40


# Carreiras E3


class CarreiraE3(Carreira):
    """Carreira da classe E3."""

    def __init__(self) -> None:
        super().__init__(IntersticioE3())

    def _limite(self):
        return 31


class CarreiraE3Concurso2008(CarreiraE3):
    """Carreira do concurso de 2008."""

    def _limite(self) -> int:
        """Limite da carreira enquanto não completar condição de aposentadoria."""
        return 33


class CarreiraE3Concurso2004(CarreiraE3):
    """Carreira do concurso de 2004."""

    def _limite(self) -> int:
        """Limite da carreira enquanto não completar condição de aposentadoria."""
        return 35


class CarreiraE3PassaDoTetoAtual(CarreiraE3):
    """Carreira do concurso de 2004 que passa do teto atual."""

    def _limite(self) -> int:
        """Limite da carreira enquanto não completar condição de aposentadoria."""
        return 39


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

    def _limite(self) -> int:
        """Limite da carreira enquanto não completar condição de aposentadoria."""
        return 48


def atribui_carreira(cm: int, classe: Classe) -> Carreira:
    """Atribui a nova carreira ao funcionário com base no concurso."""
    if classe == Classe.E3:
        if cm < 330:
            return CarreiraE3PassaDoTetoAtual()
        elif cm < 412:
            return CarreiraE3Concurso2004()
        elif cm <= 545:
            return CarreiraE3Concurso2008()
        return CarreiraE3()

    # E1 ou E2
    if cm < 330:
        return CarreiraE2PassaDoTetoAtual()
    elif cm < 412:
        return CarreiraE2Concurso2004()
    elif cm <= 545:
        return CarreiraE2Concurso2008()
    return CarreiraE2()
