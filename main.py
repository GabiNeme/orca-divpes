import sys

import config
from src.banco_de_dados import BancoDeDados
from src.cmbh import CMBH


def main(
    caminho_projecao_excel,
    ano_inicio,
    ano_fim,
    diretorio_resultado,
    recalcula_projecao=False,
):
    # Necessário para garantir que o módulo use os parâmetros carregados do banco de dados
    config.param = config.Parametros.from_aeros(BancoDeDados())

    cmbh: CMBH = CMBH.from_excel(
        caminho_projecao_excel, importa_folhas=not recalcula_projecao
    )
    if recalcula_projecao:
        cmbh.calcula_projecao(ano_inicio, ano_fim)
        cmbh.exporta_progressoes(diretorio_resultado)

    cmbh.exporta(diretorio_resultado, ano_inicio, ano_fim)
    print(
        f"Exportação concluída para {diretorio_resultado} "
        f"dos anos {ano_inicio} a {ano_fim}."
    )


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(
            f"Uso: python main.py <caminho_projecao_excel> <ano_inicio> <ano_fim> "
            f"<diretorio_resultado> [--recalcula-projecao]"
        )
        sys.exit(1)
    caminho_projecao_excel = sys.argv[1]
    diretorio_resultado = sys.argv[4]
    try:
        ano_inicio = int(sys.argv[2])
        ano_fim = int(sys.argv[3])
    except ValueError:
        print("ano_inicio e ano_fim devem ser números inteiros.")
        sys.exit(1)

    recalcula_projecao = "--recalcula-projecao" in sys.argv
    main(
        caminho_projecao_excel,
        ano_inicio,
        ano_fim,
        diretorio_resultado,
        recalcula_projecao,
    )
