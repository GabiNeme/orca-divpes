from datetime import date
from src.carreira import Carreira, Progressao
from src.classe import Classe
from src.funcionario import Aposentadoria, Funcionario, Registro
from src.nivel import Nivel


class FuncionarioFactory:
    @staticmethod
    def cria_funcionario(
        cm: int,
        classe: Classe,
        data_anuenio: date,
        num_ats: int,
        procurador: bool,
        data_aposentadoria: date,
        num_art_98_data_aposentadoria: int,
        data_ult_progressao: date,
        nivel: Nivel,
        progs_sem_especial: int,
        carreira: Carreira,
    ) -> Funcionario:
        registro = Registro(
            cm=cm,
            classe=classe,
            data_anuenio=data_anuenio,
            num_ats=num_ats,
            procurador=procurador,
        )
        aposentadoria = Aposentadoria(
            data_aposentadoria=data_aposentadoria,
            num_art_98_data_aposentadoria=num_art_98_data_aposentadoria,
        )
        ultima_progressao = Progressao(
            data=data_ult_progressao,
            nivel=nivel,
            progs_sem_especial=progs_sem_especial,
        )
        return Funcionario(
            registro=registro,
            aposentadoria=aposentadoria,
            ultima_progressao=ultima_progressao,
            carreira=carreira,
        )
