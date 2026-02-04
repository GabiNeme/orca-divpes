from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src.progressoes_horizontais import ProgressoesHorizontais


class TestProgressoesHorizontais:
    @pytest.fixture
    def mock_banco_de_dados(self):
        """Mock do BancoDeDados que retorna dados de teste."""
        mock_banco = Mock()
        # Dados de teste: cm, nivel_atual, letras_adquiridas
        test_data = pd.DataFrame(
            {
                "cm": [1, 2, 3],
                "nivel_atual": ["5", "10", None],
                "letras_adquiridas": ["A", "BASE", None],
            }
        )
        mock_banco.return_value.realiza_consulta_arquivo.return_value = test_data
        return mock_banco

    @pytest.fixture
    def progressoes_horizontais(self, mock_banco_de_dados):
        """Instância de ProgressoesHorizontais com banco mockado."""
        return ProgressoesHorizontais(banco_de_dados=mock_banco_de_dados)

    def test_init_carrega_dados_corretamente(self, progressoes_horizontais):
        """Testa se os dados são carregados corretamente do banco."""
        assert progressoes_horizontais.letras_adquiridas == {
            1: "A",
            2: "0",  # BASE convertido para '0'
            3: "0",  # None convertido para '0'
        }
        assert progressoes_horizontais.nivel_atual == {
            1: 5,
            2: 10,
            3: 1,  # None convertido para 1
        }

    @patch("config.param.CONCEDE_NOVAS_LETRAS", True)
    def test_obtem_letra_maxima_concede_novas_letras_no_maximo(
        self, progressoes_horizontais
    ):
        """Testa obtem_letra_maxima quando CONCEDE_NOVAS_LETRAS=True e está no máximo."""
        # Para cm=1, nivel_atual=5, letras_adquiridas='A'
        # CarreiraAtual().concede_letras_ate_limite(Nivel(5, "0")) retorna Nivel(5, "A") que tem numero_progressoes_horizontais=1
        # Nivel.nivel_horizontal_para_numero('A') = 1
        # 1 >= 1, então concede novas letras
        result = progressoes_horizontais.obtem_letra_maxima(1)
        assert result is None  # Pode ter todas as letras

    @patch("config.param.CONCEDE_NOVAS_LETRAS", True)
    def test_obtem_letra_maxima_nao_concede_novas_letras_abaixo_maximo(
        self, progressoes_horizontais
    ):
        """Testa obtem_letra_maxima quando CONCEDE_NOVAS_LETRAS=True mas não está no máximo."""
        # Para cm=2, nivel_atual=1, letras_adquiridas='0'
        # CarreiraAtual().concede_letras_ate_limite(Nivel(1, "0")) retorna Nivel(1, "A") que tem numero_progressoes_horizontais=1
        # Nivel.nivel_horizontal_para_numero('0') = 0
        # 0 >= 1? Não, então limita às adquiridas
        result = progressoes_horizontais.obtem_letra_maxima(2)
        assert result == "0"

    @patch("config.param.CONCEDE_NOVAS_LETRAS", False)
    def test_obtem_letra_maxima_nao_concede_novas_letras_config_false(
        self, progressoes_horizontais
    ):
        """Testa obtem_letra_maxima quando CONCEDE_NOVAS_LETRAS=False."""
        result = progressoes_horizontais.obtem_letra_maxima(1)
        assert result == "A"  # Limita à adquirida

    def test_obtem_letra_maxima_cm_nao_encontrado(self, progressoes_horizontais):
        """Testa obtem_letra_maxima para cm não encontrado."""
        result = progressoes_horizontais.obtem_letra_maxima(999)
        assert result is None
