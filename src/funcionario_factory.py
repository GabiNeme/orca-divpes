from datetime import date
from src.carreira import Carreira, Progressao
from src.classe import Classe
from src.funcionario import Aposentadoria, Funcionario, DadosFolha, TipoPrevidencia
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
        grupo_de_controle: int,
    ) -> Funcionario:
        
        if grupo_de_controle == 1:
            tipo_previdencia = TipoPrevidencia.Fufin
        elif grupo_de_controle == 3:
            tipo_previdencia = TipoPrevidencia.BHPrev
        elif grupo_de_controle == 13:
            tipo_previdencia = TipoPrevidencia.BHPrevComplementar

        dados_folha = DadosFolha(
            classe=classe,
            data_anuenio=data_anuenio,
            num_ats=num_ats,
            procurador=procurador,
            tipo_previdencia=tipo_previdencia,
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
            cm=cm,
            dados_folha=dados_folha,
            aposentadoria=aposentadoria,
            ultima_progressao=ultima_progressao,
            carreira=carreira,
        )
