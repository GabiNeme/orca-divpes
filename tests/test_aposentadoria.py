from datetime import date

from src.aposentadoria import (
    AposentadoriaAntes98,
    AposentadoriaIntegral,
    DadosPrevidenciarios,
    Sexo,
    AposentadoriaAtual,
    atribui_aposentadoria,
)


class TestAposentadoriaAtual:
    def test_aposentadoria_por_tempo_contribuicao(self):
        servidor = DadosPrevidenciarios(
            data_nascimento=date(1992, 4, 4),
            sexo=Sexo.FEMININO,
            data_admissao=date(2018, 7, 13),
            tempo_INSS=0,
            tempo_sevico_publico=0,
        )

        aposentadoria = AposentadoriaAtual(servidor)

        assert aposentadoria.data_aposentadoria == date(2048, 7, 13)
        assert not aposentadoria.compulsoria

    def test_aposentadoria_por_idade_sem_INSS(self):
        servidor = DadosPrevidenciarios(
            data_nascimento=date(1998, 1, 1),
            sexo=Sexo.MASCULINO,
            data_admissao=date(2018, 7, 13),
            tempo_INSS=0,
            tempo_sevico_publico=0,
        )

        aposentadoria = AposentadoriaAtual(servidor)

        assert aposentadoria.data_aposentadoria == date(2058, 1, 1)
        assert not aposentadoria.compulsoria

    def test_aposentadoria_por_idade_com_INSS(self):
        servidor = DadosPrevidenciarios(
            data_nascimento=date(1992, 1, 1),
            sexo=Sexo.MASCULINO,
            data_admissao=date(2018, 7, 13),
            tempo_INSS=3000,
            tempo_sevico_publico=0,
        )

        aposentadoria = AposentadoriaAtual(servidor)

        assert aposentadoria.data_aposentadoria == date(2052, 1, 1)
        assert not aposentadoria.compulsoria

    def test_aposentadoria_por_tempo_minimo_servico_publico(self):
        servidor = DadosPrevidenciarios(
            data_nascimento=date(1960, 1, 1),
            sexo=Sexo.MASCULINO,
            data_admissao=date(2018, 7, 13),
            tempo_INSS=10220,  # 28 anos
            tempo_sevico_publico=730,  # 2 anos
        )

        aposentadoria = AposentadoriaAtual(servidor)

        assert aposentadoria.data_aposentadoria == date(2026, 7, 14)
        assert not aposentadoria.compulsoria

    def test_aposentadoria_por_tempo_minimo_de_camara(self):
        servidor = DadosPrevidenciarios(
            data_nascimento=date(1960, 1, 1),
            sexo=Sexo.FEMININO,
            data_admissao=date(2018, 7, 13),
            tempo_INSS=7300,  # 20 anos
            tempo_sevico_publico=2920,  # 8 anos
        )

        aposentadoria = AposentadoriaAtual(servidor)

        assert aposentadoria.data_aposentadoria == date(2023, 7, 13)
        assert not aposentadoria.compulsoria

    def test_aposentadoria_compulsoria(self):
        servidor = DadosPrevidenciarios(
            data_nascimento=date(1947, 1, 1),
            sexo=Sexo.MASCULINO,
            data_admissao=date(2018, 7, 13),
            tempo_INSS=0,
            tempo_sevico_publico=0,
        )

        aposentadoria = AposentadoriaAtual(servidor)

        assert aposentadoria.data_aposentadoria == date(2022, 1, 1)
        assert aposentadoria.compulsoria


class TestAposentadoriaIntegral:
    def test_aposentadoria_integral_sem_tempo_anterior(self):
        servidor = DadosPrevidenciarios(
            data_nascimento=date(1974, 5, 8),
            sexo=Sexo.FEMININO,
            data_admissao=date(2002, 9, 13),
            tempo_INSS=0,
            tempo_sevico_publico=0,
        )

        aposentadoria = AposentadoriaIntegral(servidor)

        assert aposentadoria.data_aposentadoria == date(2032, 9, 13)
        assert not aposentadoria.compulsoria

    def test_aposentadoria_integral_com_tempo_anterior(self):
        servidor = DadosPrevidenciarios(
            data_nascimento=date(1978, 5, 12),
            sexo=Sexo.FEMININO,
            data_admissao=date(2006, 2, 12),
            tempo_INSS=0,
            tempo_sevico_publico=1750,
        )

        aposentadoria = AposentadoriaIntegral(servidor)

        assert aposentadoria.data_aposentadoria == date(2033, 5, 12)
        assert not aposentadoria.compulsoria


class TestAposentadoriaAntes98:
    def test_regra_transicao_qdo_completa_aniversario(self):
        servidor = DadosPrevidenciarios(
            data_nascimento=date(1968, 5, 30),
            sexo=Sexo.MASCULINO,
            data_admissao=date(1990, 8, 13),
            tempo_INSS=0,
            tempo_sevico_publico=0,
        )
        # 13/08/2025 - 35 anos contribuição e 57 anos idade -> total 92 pontos
        # 30/05/2026 - 35 anos contribuição e 58 anos idade -> total 93 pontos
        # 13/08/2026 - 36 anos contribuição e 58 anos idade -> total 94 pontos
        # 30/05/2027 - 36 anos contribuição e 59 anos idade -> total 95 pontos

        aposentadoria = AposentadoriaAntes98(servidor)

        assert aposentadoria.data_aposentadoria == date(2027, 5, 30)
        assert not aposentadoria.compulsoria

    def test_regra_transicao_qdo_completa_contribuicao(self):
        servidor = DadosPrevidenciarios(
            data_nascimento=date(1969, 8, 18),
            sexo=Sexo.FEMININO,
            data_admissao=date(1990, 5, 30),
            tempo_INSS=0,
            tempo_sevico_publico=0,
        )
        # 30/05/2020 - 30 anos contribuição e 50 anos idade -> total 80 pontos
        # 18/08/2020 - 30 anos contribuição e 51 anos idade -> total 81 pontos
        # 30/05/2021 - 31 anos contribuição e 51 anos idade -> total 82 pontos
        # 18/08/2021 - 31 anos contribuição e 52 anos idade -> total 83 pontos
        # 30/05/2022 - 32 anos contribuição e 52 anos idade -> total 84 pontos
        # 18/08/2022 - 32 anos contribuição e 53 anos idade -> total 85 pontos

        aposentadoria = AposentadoriaAntes98(servidor)

        assert aposentadoria.data_aposentadoria == date(2022, 8, 18)
        assert not aposentadoria.compulsoria

    def test_regra_transicao_com_mesmo_dia_admissao_e_aniversario(self):
        servidor = DadosPrevidenciarios(
            data_nascimento=date(1972, 1, 1),
            sexo=Sexo.FEMININO,
            data_admissao=date(1995, 1, 1),
            tempo_INSS=0,
            tempo_sevico_publico=0,
        )
        # 01/01/2025 - 30 anos contribuição e 53 anos idade -> total 83 pontos
        # 01/01/2026 - 31 anos contribuição e 54 anos idade -> total 85 pontos

        aposentadoria = AposentadoriaAntes98(servidor)

        assert aposentadoria.data_aposentadoria == date(2026, 1, 1)
        assert not aposentadoria.compulsoria

    def test_aposentadoria_integral_mais_vantajosa(self):
        servidor = DadosPrevidenciarios(
            data_nascimento=date(1969, 12, 5),
            sexo=Sexo.FEMININO,
            data_admissao=date(2010, 2, 10),
            tempo_INSS=0,
            tempo_sevico_publico=7300,  # 20 anos
        )
        # 05/12/2022 - 32 anos de contribuição e 53 anos de idade -> total 85 pontos
        # precisa ter 15 anos de CMBH, tem 13, então aposentaria por essa regra só em 10/02/2025

        # Pela regra integral, completa a idade minima em 05/12/2024, com 14 anos de CMBH
        # e 35 anos de contribuição

        aposentadoria = AposentadoriaAntes98(servidor)

        assert aposentadoria.data_aposentadoria == date(2024, 12, 5)
        assert not aposentadoria.compulsoria


class TesytAtribuiAposentadoria:
    def test_atribui_aposentadoria_antes_98(self):
        servidor = DadosPrevidenciarios(
            data_nascimento=date(1960, 1, 1),
            sexo=Sexo.MASCULINO,
            data_admissao=date(1980, 1, 1),
            tempo_INSS=0,
            tempo_sevico_publico=0,
        )
        cls = atribui_aposentadoria(servidor)
        assert cls is AposentadoriaAntes98

    def test_atribui_aposentadoria_integral():
        servidor = DadosPrevidenciarios(
            data_nascimento=date(1970, 1, 1),
            sexo=Sexo.FEMININO,
            data_admissao=date(2000, 1, 1),
            tempo_INSS=0,
            tempo_sevico_publico=0,
        )

        cls = atribui_aposentadoria(servidor)
        assert cls is AposentadoriaIntegral

    def test_atribui_aposentadoria_atual():
        servidor = DadosPrevidenciarios(
            data_nascimento=date(1980, 1, 1),
            sexo=Sexo.FEMININO,
            data_admissao=date(2010, 1, 1),
            tempo_INSS=1200,
            tempo_sevico_publico=0,
        )

        cls = atribui_aposentadoria(servidor)
        assert cls is AposentadoriaAtual

    def test_atribui_aposentadoria_integral_with_tempo_servico_publico():
        # Admissao: 2005-01-01, tempo_sevico_publico: 2000 dias (~5.48 anos)
        # Ingresso no serviço público: 2005-01-01 - 2000 dias = 1999-06-15
        servidor = DadosPrevidenciarios(
            data_nascimento=date(1975, 1, 1),
            sexo=Sexo.FEMININO,
            data_admissao=date(2005, 1, 1),
            tempo_INSS=0,
            tempo_sevico_publico=2000,
        )
        cls = atribui_aposentadoria(servidor)
        assert cls is AposentadoriaIntegral
