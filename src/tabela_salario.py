from datetime import date
from functools import lru_cache
from dateutil.relativedelta import relativedelta

import config
from src.classe import Classe
from src.nivel import Nivel


class Tabela:
    @lru_cache(maxsize=None)
    @staticmethod
    def valor_do(nivel: Nivel, valor_inicial: float) -> float:
        """Calcula o valor do nível informado."""

        progressao_vertical_total = (1 + config.param.INDICE_PROGRESSAO_VERTICAL) ** (
            nivel.numero - 1
        )

        progressao_horizontal_total = (
            1 + config.param.INDICE_PROGRESSAO_HORIZONTAL
        ) ** (nivel.numero_progressoes_horizontais)

        valor = valor_inicial * progressao_vertical_total * progressao_horizontal_total
        return round(valor, 2)

    @staticmethod
    def valor_do_nivel_para_classe(
        nivel: Nivel, classe: Classe, competencia: date
    ) -> float:
        """Calcula o valor do nível informado para uma classe específica."""
        if classe == Classe.E1 or classe == Classe.E2:  # Classes E1 e E2
            valor_base = Tabela.valor_do(nivel, config.param.VALOR_BASE_E2)
        else:  # Classe E3
            valor_base = Tabela.valor_do(nivel, config.param.VALOR_BASE_E3)

        return valor_base * Tabela.calcula_indice_reajuste(competencia)

    @lru_cache(maxsize=None)
    @staticmethod
    def calcula_indice_reajuste(
        competencia: date, data_calculo: date = date.today()
    ) -> float:
        """Calcula o índice de reajuste para a competência informada."""

        # Se a projeção for executada no mês ou após o mês da data base, não conta o
        # ano corrente, e a primeira data base será no ano seguinte
        if data_calculo.month >= config.param.DATA_BASE_REAJUSTE:
            data_base_inicial = date(
                data_calculo.year, config.param.DATA_BASE_REAJUSTE, 1
            )
        else:
            data_base_inicial = date(
                data_calculo.year - 1, config.param.DATA_BASE_REAJUSTE, 1
            )

        quantidade_anos = relativedelta(competencia, data_base_inicial).years

        # Não permite índices negativos (competências anteriores à data base)
        quantidade_anos = max(0, quantidade_anos)

        return round((1 + config.param.REAJUSTE_ANUAL) ** quantidade_anos, 6)
