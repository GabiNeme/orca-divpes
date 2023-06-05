from datetime import date

from src.cargo import Nivel
from src.carreira import Carreira2004, Progressao


class Desenvolvimento:
    def __init__(
        self,
        carreira: Carreira2004,
        nivel_atual: Nivel,
        dt_ult_prog_vert: date,
        progs_sem_especial: int,
    ) -> None:
        self.carreira = carreira
        self.progressoes = [
            Progressao(dt_ult_prog_vert, nivel_atual),
        ]
        self.progressoes_sem_especial = progs_sem_especial
        self.concede_letras = self._decide_se_concedera_letras()
        if self.concede_letras:
            self.progressoes[0].nivel = self.carreira.concede_letras_ate_limite(
                self.progressoes[0].nivel
            )

    def _decide_se_concedera_letras(self):
        """Concede todas as letras se a pessoa tiver a uma letra ou na letra máxima
        do nível, mas não concede nenhuma se tiver a 2 letras ou mais de distância do
        máximo."""

        nivel_atual = self.progressoes[0].nivel
        nivel_letra_maxima = self.carreira.concede_letras_ate_limite(nivel_atual)

        if (
            nivel_letra_maxima.numero_progressoes_horizontais
            - nivel_atual.numero_progressoes_horizontais
            >= 2
        ):
            return False
        return True

    def _calcula_progressoes_ate(self, data: date):
        ultima_progressao = self.progressoes[-1]

        while ultima_progressao and data > ultima_progressao.data:
            if self.progressoes_sem_especial == 2:
                self.progressoes_sem_especial = 0
                especial = True
            else:
                self.progressoes_sem_especial += 1
                especial = False

            if self.concede_letras:
                ultima_progressao = (
                    self.carreira.progride_verticalmente_e_horizontalmente(
                        ultima_progressao, especial
                    )
                )
            else:
                ultima_progressao = self.carreira.progride_verticalmente(
                    ultima_progressao, especial
                )

            if ultima_progressao:
                self.progressoes.append(ultima_progressao)

    def obtem_nivel_para(self, data: date) -> Nivel:
        """Retorna o nível que o servidor estará em determinada data."""

        self._calcula_progressoes_ate(data)

        for progressao in reversed(self.progressoes):
            dt_prog = progressao.data
            if dt_prog < data or (
                dt_prog.month == data.month and dt_prog.year == data.year
            ):
                return progressao.nivel
