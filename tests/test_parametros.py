import pytest
import pandas as pd
from unittest.mock import patch, mock_open
from src.parametros import Parametros


class DummyBancoDeDados:
    """Dummy BancoDeDados for testing purposes."""

    def __init__(self, return_data=pd.DataFrame(), sql_dir="sql"):
        self.return_data = return_data
        self.sql_dir = sql_dir

    def realiza_consulta_arquivo(self, sql_filename):
        # Para testes, podemos apenas chamar realiza_consulta com uma consulta fictícia
        return self.return_data


class TestParametros:
    def test_parametros_valores_padrao(self):
        """Testa se os valores padrão são carregados corretamente."""
        p = Parametros()
        assert p.VALOR_BASE_E2 == 5758.83
        assert p.VALOR_BASE_E3 == 10047.80
        assert p.INDICE_PROGRESSAO_VERTICAL == 0.0391
        assert p.INDICE_PROGRESSAO_HORIZONTAL == 0.0797
        assert p.REAJUSTE_ANUAL == 0.1
        assert p.DATA_BASE_REAJUSTE == 5
        assert p.TETO_PREFEITO == 34604.05
        assert p.TETO_PROCURADORES == 41845.49
        assert p.ALIQUOTA_PATRONAL == 0.22
        assert p.ALIQUOTA_PATRONAL_COMPLEMENTAR == 0.085
        assert p.TETO_INSS == 8157.41

    def test_from_aeros_carregamento_bem_sucedido(self):
        """Testa carregamento bem-sucedido do Aeros."""
        dummy_df = pd.DataFrame(
            {
                "VALOR_BASE_E2": [6000.0],
                "VALOR_BASE_E3": [11000.0],
                "TETO_PREFEITO": [35000.0],
                "TETO_PROCURADORES": [42000.0],
                "TETO_INSS": [8500.0],
            }
        )
        dummy_aeros = DummyBancoDeDados(return_data=dummy_df)

        p = Parametros.from_aeros(dummy_aeros)

        assert p.VALOR_BASE_E2 == 6000.0
        assert p.VALOR_BASE_E3 == 11000.0
        assert p.TETO_PREFEITO == 35000.0
        assert p.TETO_PROCURADORES == 42000.0
        assert p.TETO_INSS == 8500.0
        assert p.INDICE_PROGRESSAO_VERTICAL == 0.0391  # Default

    def test_from_aeros_lanca_erro_se_coluna_ausente(self):
        """Testa se erro é levantado quando coluna está ausente no DataFrame."""
        # DataFrame sem a coluna VALOR_BASE_E2
        dummy_df = pd.DataFrame(
            {"VALOR_BASE_E3": [11000.0], "TETO_PREFEITO": [35000.0]}
        )
        dummy_aeros = DummyBancoDeDados(return_data=dummy_df)

        with pytest.raises(KeyError, match="VALOR_BASE_E2"):
            Parametros.from_aeros(dummy_aeros)

    def test_from_aeros_lanca_erro_se_dataframe_vazio(self):
        """Testa se erro é levantado quando DataFrame está vazio."""
        dummy_aeros = DummyBancoDeDados(return_data=pd.DataFrame())

        with pytest.raises(ValueError):
            Parametros.from_aeros(dummy_aeros)

    def test_from_aeros_lanca_erro_se_valores_nulos(self):
        """Testa se valores nulos no DataFrame levantam erro."""
        dummy_df = pd.DataFrame(
            {
                "VALOR_BASE_E2": [None],  # Valor nulo
                "VALOR_BASE_E3": [11000.0],
                "TETO_PREFEITO": [35000.0],
                "TETO_PROCURADORES": [42000.0],
                "TETO_INSS": [8500.0],
            }
        )
        dummy_aeros = DummyBancoDeDados(return_data=dummy_df)

        with pytest.raises(ValueError):
            p = Parametros.from_aeros(dummy_aeros)
            # Força o uso do valor None para verificar se causa erro
            assert p.VALOR_BASE_E2 is not None
