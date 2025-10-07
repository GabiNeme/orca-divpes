from functools import lru_cache

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
    def valor_do_nivel_para_classe(nivel: Nivel, classe: Classe) -> float:
        """Calcula o valor do nível informado para uma classe específica."""
        if classe == Classe.E1 or classe == Classe.E2:
            return Tabela.valor_do(nivel, config.param.VALOR_BASE_E2)

        return Tabela.valor_do(nivel, config.param.VALOR_BASE_E3)
