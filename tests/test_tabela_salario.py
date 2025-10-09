from datetime import date
import pytest

import config
from src.classe import Classe
from src.nivel import Nivel
from src.tabela_salario import Tabela

# Configura os parâmetros para os testes
config.param.VALOR_BASE_E2 = 5758.83
config.param.VALOR_BASE_E3 = 10047.80
config.param.INDICE_PROGRESSAO_VERTICAL = 0.0391
config.param.INDICE_PROGRESSAO_HORIZONTAL = 0.0797
config.param.REAJUSTE_ANUAL = 0.1
config.param.DATA_BASE_REAJUSTE = 5


class TestTabela:
    @pytest.mark.parametrize(
        "nivel, valor",
        [
            ("1.0", 5758.83),
            ("5.A", 7248.81),
            ("10.B", 9481.05),
            ("15.C", 12400.71),
            ("20.D", 16219.45),
            ("30.E", 25698.8),
        ],
    )
    def test_valor_do_nivel(self, nivel: str, valor: float):
        tabela = Tabela
        nivel_ = Nivel.from_string(nivel)
        assert tabela.valor_do(nivel_, 5758.83) == valor

    def test_valor_do_nivel_E2(self):
        tabela = Tabela()
        assert (
            tabela.valor_do_nivel_para_classe(Nivel(1, "0"), Classe.E2, date.today())
            == 5758.83
        )
        assert (
            tabela.valor_do_nivel_para_classe(Nivel(20, "A"), Classe.E2, date.today())
            == 12886.26
        )
        assert (
            tabela.valor_do_nivel_para_classe(Nivel(31, "E"), Classe.E2, date.today())
            == 26703.62
        )

    def test_valor_do_nivel_E3(self):
        tabela = Tabela()
        assert (
            tabela.valor_do_nivel_para_classe(Nivel(1, "0"), Classe.E3, date.today())
            == 10047.80
        )
        assert (
            tabela.valor_do_nivel_para_classe(Nivel(16, "B"), Classe.E3, date.today())
            == 20822.72
        )
        assert (
            tabela.valor_do_nivel_para_classe(Nivel(33, "E"), Classe.E3, date.today())
            == 50306.2
        )

    def test_reajuste_zero_ate_proxima_data_base(self):
        # Competência antes da data do cálculo
        assert (
            Tabela.calcula_indice_reajuste(
                competencia=date(2023, 1, 1), data_calculo=date(2023, 4, 1)
            )
            == 1.0
        )
        # No mesmo ano, quando cálculo é feito no mês da data base
        assert (
            Tabela.calcula_indice_reajuste(
                competencia=date(2023, 12, 31), data_calculo=date(2023, 5, 1)
            )
            == 1.0
        )
        # No mesmo ano, quando cálculo é feito após o mês da data base
        assert (
            Tabela.calcula_indice_reajuste(
                competencia=date(2023, 12, 1), data_calculo=date(2023, 6, 1)
            )
            == 1.0
        )
        # No ano seguinte, quando cálculo é feito após o mês da data base
        assert (
            Tabela.calcula_indice_reajuste(
                competencia=date(2024, 3, 1), data_calculo=date(2023, 6, 1)
            )
            == 1.0
        )
        # No mesmo ano, quando cálculo e competência são feitos antes da data base
        assert (
            Tabela.calcula_indice_reajuste(
                competencia=date(2024, 3, 1), data_calculo=date(2024, 2, 1)
            )
            == 1.0
        )

    def test_reajuste_aplicado_ano_corrente(self):
        assert (
            Tabela.calcula_indice_reajuste(
                competencia=date(2023, 5, 1), data_calculo=date(2023, 1, 1)
            )
            == 1.1
        )

    def test_reajuste_aplicado_anos_seguinte(self):
        assert (
            Tabela.calcula_indice_reajuste(
                competencia=date(2024, 5, 1), data_calculo=date(2023, 1, 1)
            )
            == 1.21
        )
        assert (
            Tabela.calcula_indice_reajuste(
                competencia=date(2025, 5, 1), data_calculo=date(2023, 1, 1)
            )
            == 1.331
        )
