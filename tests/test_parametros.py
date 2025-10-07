import pandas as pd
import pytest

import config


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
        p = config.Parametros()
        assert p.VALOR_BASE_E2 == None
        assert p.VALOR_BASE_E3 == None
        assert p.INDICE_PROGRESSAO_VERTICAL == 0.0391
        assert p.INDICE_PROGRESSAO_HORIZONTAL == 0.0797
        assert p.REAJUSTE_ANUAL == 0.1
        assert p.DATA_BASE_REAJUSTE == 5
        assert p.TETO_PREFEITO == None
        assert p.TETO_PROCURADORES == None
        assert p.ALIQUOTA_PATRONAL == 0.22
        assert p.ALIQUOTA_PATRONAL_COMPLEMENTAR == 0.085
        assert p.TETO_INSS == None

    def test_from_aeros_carregamento_bem_sucedido(self):
        """Testa carregamento bem-sucedido do Aeros."""
        dummy_df = pd.DataFrame(
            {
                "valor_base_e2": [6000.0],
                "valor_base_e3": [11000.0],
                "teto_prefeito": [35000.0],
                "teto_procuradores": [42000.0],
                "teto_inss": [8500.0],
            }
        )
        dummy_aeros = DummyBancoDeDados(return_data=dummy_df)

        p = config.Parametros.from_aeros(dummy_aeros)

        assert p.VALOR_BASE_E2 == 6000.0
        assert p.VALOR_BASE_E3 == 11000.0
        assert p.TETO_PREFEITO == 35000.0
        assert p.TETO_PROCURADORES == 42000.0
        assert p.TETO_INSS == 8500.0
        assert p.INDICE_PROGRESSAO_VERTICAL == 0.0391  # Default

    def test_from_aeros_lanca_erro_se_coluna_ausente(self):
        """Testa se erro é levantado quando coluna está ausente no DataFrame."""
        # DataFrame sem a coluna valor_base_e2
        dummy_df = pd.DataFrame(
            {"valor_base_e3": [11000.0], "teto_prefeito": [35000.0]}
        )
        dummy_aeros = DummyBancoDeDados(return_data=dummy_df)

        with pytest.raises(KeyError, match="valor_base_e2"):
            config.Parametros.from_aeros(dummy_aeros)

    def test_from_aeros_lanca_erro_se_dataframe_vazio(self):
        """Testa se erro é levantado quando DataFrame está vazio."""
        dummy_aeros = DummyBancoDeDados(return_data=pd.DataFrame())

        with pytest.raises(ValueError):
            config.Parametros.from_aeros(dummy_aeros)

    def test_from_aeros_lanca_erro_se_valores_nulos(self):
        """Testa se valores nulos no DataFrame levantam erro."""
        dummy_df = pd.DataFrame(
            {
                "valor_base_e2": [None],  # Valor nulo
                "valor_base_e3": [11000.0],
                "teto_prefeito": [35000.0],
                "teto_procuradores": [42000.0],
                "teto_inss": [8500.0],
            }
        )
        dummy_aeros = DummyBancoDeDados(return_data=dummy_df)

        with pytest.raises(ValueError):
            p = config.Parametros.from_aeros(dummy_aeros)
            # Força o uso do valor None para verificar se causa erro
            assert p.VALOR_BASE_E2 is not None
