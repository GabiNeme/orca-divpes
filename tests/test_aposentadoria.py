from datetime import date

from src.aposentadoria import Aposentadoria, DadosPrevidenciarios, Sexo


class TestAposentadoria:
    def test_aposentadoria_por_tempo_contribuicao(self):
        servidor = DadosPrevidenciarios(
            data_nascimento=date(1992, 4, 4),
            sexo=Sexo.FEMININO,
            data_admissao=date(2018, 7, 13),
            tempo_INSS=0,
            tempo_sevico_publico=0,
        )

        aposentadoria = Aposentadoria(servidor, t_min_serv_pub=10, t_min_camara=5)

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

        aposentadoria = Aposentadoria(servidor, t_min_serv_pub=10, t_min_camara=5)

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

        aposentadoria = Aposentadoria(servidor, t_min_serv_pub=10, t_min_camara=5)

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

        aposentadoria = Aposentadoria(servidor, t_min_serv_pub=10, t_min_camara=5)

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

        aposentadoria = Aposentadoria(servidor, t_min_serv_pub=10, t_min_camara=5)

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

        aposentadoria = Aposentadoria(servidor, t_min_serv_pub=10, t_min_camara=5)

        assert aposentadoria.data_aposentadoria == date(2022, 1, 1)
        assert aposentadoria.compulsoria
