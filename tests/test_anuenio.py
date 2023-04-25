from datetime import date

import pytest

from src.anuenio import Anuenio


class TestAnuenio:
    @pytest.mark.parametrize(
        "data_inicio_anuenio, data, num_anuenio",
        [
            (date(2018, 7, 13), date(2019, 6, 1), 0),
            (date(2018, 7, 13), date(2019, 7, 1), 0),
            (date(2018, 7, 13), date(2019, 7, 13), 1),
            (date(2018, 7, 13), date(2022, 12, 1), 4),
            (date(1996, 9, 6), date(2020, 8, 1), 23),
        ],
    )
    def test_obtem_anuenio_para_data(
        self, data_inicio_anuenio: date, data: date, num_anuenio: int
    ):
        assert (
            Anuenio(data_inicio_anuenio).obtem_numero_anuenios_para(data) == num_anuenio
        )
