from datetime import date

from dateutil.relativedelta import relativedelta


class Anuenio:
    def __init__(self, data_inicio: date) -> None:
        self.data_inicio = data_inicio

    def obtem_numero_anuenios_para(self, data: date) -> int:
        return relativedelta(data, self.data_inicio).years
