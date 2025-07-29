from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Optional

from dateutil.relativedelta import relativedelta

from src.classe import Classe
from src.nivel import Nivel
from src.intersticio import Intersticio


@dataclass
class Progressao:
    data: date
    nivel: Nivel
    progs_sem_especial: int = 0
    credito_meses_prox_prog: int = 0


class Carreira(ABC):
    def __init__(self, classe: Classe) -> None:
        self.classe = classe

    def progride_verticalmente_por_quantidade_de_niveis(
        self, ultima_progressao: Progressao, numero_niveis: int
    ) -> Optional[Progressao]:
        """Calcula uma progressão vertical (2 interstícios), permitindo definir quantos
        níveis serão progredidos."""

        self.checa_nivel_valido(ultima_progressao.nivel)
        limite = self.limite(ultima_progressao.nivel)

        if ultima_progressao.nivel.numero >= limite:
            return None

        intersticio = Intersticio.tempo_para_progredir(ultima_progressao.nivel, 2)
        dt_prox_prog = ultima_progressao.data + relativedelta(months=intersticio)

        if numero_niveis + ultima_progressao.nivel.numero > limite:
            numero_niveis = limite - ultima_progressao.nivel.numero
            if numero_niveis == 1:
                # Se leva só um nível na última progressão, ganha crédito de 15 dias
                # para a próxima progressão.
                return Progressao(
                    dt_prox_prog,
                    ultima_progressao.nivel.proximo(numero_niveis, 0),
                    progs_sem_especial=(ultima_progressao.progs_sem_especial + 1) % 3,
                    credito_meses_prox_prog=15,
                )

        return Progressao(
            dt_prox_prog,
            ultima_progressao.nivel.proximo(numero_niveis, 0),
            progs_sem_especial=(ultima_progressao.progs_sem_especial + 1) % 3,
        )

    def progride_verticalmente(
        self, ultima_progressao: Progressao
    ) -> Optional[Progressao]:
        """Calcula uma progressão vertical (2 interstícios), podendo ser especial
        ou não."""

        if ultima_progressao.progs_sem_especial == 2:
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

        letra_maxima = self.letra_maxima_para_nivel(nivel_origem.numero)
        return Nivel(nivel_origem.numero, letra_maxima)

    def limite(self, nivel: Nivel = None) -> int:
        """Limite da carreira enquanto não completar condição de aposentadoria."""
        if self.classe == Classe.E2:
            return 37
        if self.classe == Classe.E3:
            return 36

    def limite_absoluto(self, nivel: Nivel = None) -> int:
        """O limite absoluto da carreira, do qual é sempre impossível passar."""
        return self.limite(nivel)

    def checa_nivel_valido(self, nivel: Nivel):
        """Lança uma exceção se o nível informado for inválido."""

        def numero_invalido(numero_nivel: int) -> bool:
            if numero_nivel > self.limite_absoluto(nivel):
                return True
            return False

        def letra_invalida(nivel: Nivel) -> bool:
            letra_max = self.letra_maxima_para_nivel(nivel.numero)
            nivel_hor_max = Nivel(nivel.numero, letra_max)
            if (
                nivel.numero_progressoes_horizontais
                > nivel_hor_max.numero_progressoes_horizontais
            ):
                return True
            return False

        if numero_invalido(nivel.numero) or letra_invalida(nivel):
            raise (ValueError("O nível " + str(nivel) + " não existe nessa carreira."))

    @abstractmethod
    def letra_maxima_para_nivel(self, numero_nivel: int) -> str:
        raise NotImplementedError


class Carreira2004(Carreira):
    def letra_maxima_para_nivel(self, numero_nivel: int) -> str:
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


class CarreiraAntes2004(Carreira):
    def limite(self, nivel: Nivel = None) -> int:
        limite_classe = super().limite()

        return limite_classe + 2 * (5 - nivel.numero_progressoes_horizontais)

    def limite_absoluto(self, nivel: Nivel = None) -> int:
        """Limite de 25% após o fim da carreira, que só pode acontecer enquanto não
        completar condição de aposentadoria."""
        return self.limite(nivel) + 5

    def letra_maxima_para_nivel(self, numero_nivel: int) -> str:
        """Retorna a máxima letra que é possível ter para um determinado nível."""

        if numero_nivel <= 6:
            return "A"
        if numero_nivel <= 12:
            return "B"
        if numero_nivel <= 18:
            return "C"
        if numero_nivel <= 24:
            return "D"

        if self.classe == Classe.E2:
            if numero_nivel <= 37:
                return "E"
            if numero_nivel <= 39:
                return "D"
            if numero_nivel <= 41:
                return "C"
            if numero_nivel <= 43:
                return "B"
            if numero_nivel <= 45:
                return "A"
            return "0"

        if self.classe == Classe.E3:
            if numero_nivel <= 36:
                return "E"
            if numero_nivel <= 38:
                return "D"
            if numero_nivel <= 40:
                return "C"
            if numero_nivel <= 42:
                return "B"
            if numero_nivel <= 44:
                return "A"
            return "0"

    def progride_verticalmente(
        self, ultima_progressao: Progressao, especial: bool = False
    ) -> Optional[Progressao]:
        """Sobrescreve o método de progressão vertical para calcular a progressão do
        art. 44, ou seja, progredir a cada 48 meses 1 nível até o máximo de 25% a mais
        que o teto da carreira."""
        progressao = super().progride_verticalmente(ultima_progressao)

        if progressao:
            return progressao

        limite_vertical = self.limite_absoluto(ultima_progressao.nivel)

        if ultima_progressao.nivel.numero == limite_vertical:
            return None

        intersticio = 48 - ultima_progressao.credito_meses_prox_prog
        dt_prox_prog = ultima_progressao.data + relativedelta(months=intersticio)

        return Progressao(
            dt_prox_prog,
            ultima_progressao.nivel.proximo(1, 0),
            (ultima_progressao.progs_sem_especial + 1) % 3,
            0,
        )

    def checa_nivel_valido(self, nivel: Nivel):
        nivel_vertical_maximo = self.limite_absoluto(nivel)
        if nivel.numero > nivel_vertical_maximo:
            raise (
                ValueError(
                    "O nível "
                    + str(nivel_vertical_maximo)
                    + " não existe nessa carreira."
                )
            )
