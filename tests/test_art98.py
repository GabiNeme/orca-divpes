from datetime import date

import pytest
from freezegun import freeze_time

from src.art98 import Art98, DadosArt98


class TestArt98:
    @freeze_time("2020-02-01")
    def test_media_usufruto_igual_media_cmbh_se_admissao_maior_que_data_atual(self):
        art98 = Art98(date(2021, 1, 1), 20, media_usufruto_cmbh=4)
        assert art98.media_usufruto_por_ano() == 4

    @pytest.mark.parametrize(
        "data_inicio_art98, usufruto, media_usufruto",
        [
            (date(2005, 8, 16), 35, 2),
            (date(2007, 4, 9), 0, 0),
            (date(2009, 10, 26), 87, 8),
            (date(2018, 6, 13), 8, 8),
        ],
    )
    @freeze_time("2020-02-01")
    def test_media_usufruto_calculada(
        self, data_inicio_art98: date, usufruto: int, media_usufruto: int
    ):
        art98 = Art98(data_inicio_art98, usufruto)

        assert art98.media_usufruto_por_ano() == media_usufruto

    @freeze_time("2020-06-01")
    def test_media_zero_se_menos_que_1_ano(self):
        art98 = Art98(date(2020, 2, 1), 0)

        assert art98.media_usufruto_por_ano() == 0

    @pytest.mark.parametrize(
        "data_inicio_art98, data, usufruto, num_art98",
        [
            (date(2005, 3, 21), date(2020, 3, 1), 0, 224),
            (date(2005, 3, 21), date(2020, 4, 1), 0, 272),
            (date(2005, 3, 19), date(2023, 4, 1), 0, 312),
            (date(2005, 8, 10), date(2028, 9, 1), 0, 392),
            (date(2011, 8, 26), date(2024, 12, 1), 4, 212),
            (date(2012, 10, 18), date(2028, 4, 1), 2, 270),
            (date(2018, 7, 13), date(2023, 8, 1), 0, 80),
        ],
    )
    def test_num_art98_media_zero(
        self,
        data_inicio_art98: date,
        data: date,
        usufruto: int,
        num_art98: int,
    ):
        art98 = Art98(data_inicio_art98, usufruto)

        assert art98.obtem_num_art98_para(data) == num_art98

    @pytest.mark.parametrize(
        "data_inicio_art98, data, usufruto, num_art98",
        [
            (date(2005, 4, 4), date(2020, 2, 1), 76, 148),
            (date(2005, 4, 4), date(2020, 5, 1), 76, 196),
            (date(2005, 4, 4), date(2023, 2, 1), 76, 197),
            (date(2005, 4, 4), date(2023, 5, 1), 76, 221),
            (date(2012, 10, 26), date(2020, 2, 1), 77, 35),
            (date(2012, 10, 26), date(2030, 2, 1), 77, 101),
        ],
    )
    @freeze_time("2020-02-01")
    def test_num_art98_media_maior_zero(
        self,
        data_inicio_art98: date,
        data: date,
        usufruto: int,
        num_art98: int,
    ):
        art98 = Art98(data_inicio_art98, usufruto)

        assert art98.obtem_num_art98_para(data) == num_art98

    @freeze_time("2020-01-01")  # Função irá usar a média informada
    def test_num_art98_nunca_menor_que_0(self):
        art98 = Art98(date(2020, 2, 1), 0, media_usufruto_cmbh=11)

        assert art98.obtem_num_art98_para(date(2020, 2, 1)) == 0
        assert art98.obtem_num_art98_para(date(2021, 2, 1)) == 0
        assert art98.obtem_num_art98_para(date(2022, 2, 1)) == 0
        assert art98.obtem_num_art98_para(date(2023, 2, 1)) == 7
        assert art98.obtem_num_art98_para(date(2024, 2, 1)) == 4

    @freeze_time("2020-01-01")
    def test_calcula_media_usufruto_art98_cmbh(self):
        dados_art98 = [
            DadosArt98(date(2010, 1, 1), 10),  # 1 por ano
            DadosArt98(date(2010, 1, 1), 20),  # 2 por ano
            DadosArt98(date(2015, 1, 1), 30),  # 6 por ano
        ]

        assert Art98.calcula_media_usufruto_art98_cmbh(dados_art98) == 3

    def test_calcula_media_usufruto_art98_cmbh_sem_dados(self):
        dados_art98 = []

        assert Art98.calcula_media_usufruto_art98_cmbh(dados_art98) == 0

    def test_calcula_media_usufruto_art98_cmbh_none(self):
        assert Art98.calcula_media_usufruto_art98_cmbh(None) == 0
