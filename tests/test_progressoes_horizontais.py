from unittest.mock import Mock

import pandas as pd
import pytest

import config
from config import ConcessaoLetras
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

    def test_obtem_letra_maxima_concede_todas(self, progressoes_horizontais):
        """Testa obtem_letra_maxima quando modo é CONCEDE_TODAS e está no máximo."""
        original = config.param.CONCESSAO_LETRAS
        config.param.CONCESSAO_LETRAS = ConcessaoLetras.CONCEDE_TODAS
        try:
            result = progressoes_horizontais.obtem_letra_maxima(1)
            assert result is None  # Pode ter todas as letras
        finally:
            config.param.CONCESSAO_LETRAS = original

    def test_obtem_letra_maxima_nao_alcancou_maximo(self, progressoes_horizontais):
        """Testa obtem_letra_maxima quando servidor não possui todas as letras permitidas."""
        original = config.param.CONCESSAO_LETRAS
        config.param.CONCESSAO_LETRAS = ConcessaoLetras.CONCEDE_TODAS
        try:
            result = progressoes_horizontais.obtem_letra_maxima(2)
            assert result == "0"
        finally:
            config.param.CONCESSAO_LETRAS = original

    def test_obtem_letra_maxima_nao_concede(self, progressoes_horizontais):
        """Testa obtem_letra_maxima quando modo é NAO_CONCEDE."""
        original = config.param.CONCESSAO_LETRAS
        config.param.CONCESSAO_LETRAS = ConcessaoLetras.NAO_CONCEDE
        try:
            result = progressoes_horizontais.obtem_letra_maxima(1)
            assert result == "A"  # Limita à adquirida
        finally:
            config.param.CONCESSAO_LETRAS = original

    def test_obtem_letra_maxima_concede_uma(self, progressoes_horizontais):
        """Testa obtem_letra_maxima quando modo é CONCEDE_UMA (uma letra a mais)."""
        original = config.param.CONCESSAO_LETRAS
        config.param.CONCESSAO_LETRAS = ConcessaoLetras.CONCEDE_UMA
        try:
            # Para cm=1, adquirida 'A' -> permite 'B'
            result = progressoes_horizontais.obtem_letra_maxima(1)
            assert result == "B"
        finally:
            config.param.CONCESSAO_LETRAS = original

    def test_obtem_letra_maxima_cm_nao_encontrado_verdadeiro(
        self, progressoes_horizontais
    ):
        """Testa obtem_letra_maxima para cm não encontrado: espera que seja retornado màximo 0."""
        original = config.param.CONCESSAO_LETRAS
        config.param.CONCESSAO_LETRAS = ConcessaoLetras.CONCEDE_UMA
        try:
            # cm=999 não existe nos dados de teste, deve retornar None
            result = progressoes_horizontais.obtem_letra_maxima(999)
            assert result == "0"
        finally:
            config.param.CONCESSAO_LETRAS = original
