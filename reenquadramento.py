import argparse
import sys

from reenquadramento.trajetoria_simulada import TrajetoriasSimuladas


def reenquadramento(
    caminho_projecao_excel: str,
    caminho_saida_reenquadramento: str = "resultado_reenquadramento.xlsx",
):
    """Executa a lógica principal do reenquadramento."""

    calculadora = TrajetoriasSimuladas.from_excel(caminho_projecao_excel)
    print("Calculando trajetórias simuladas...")
    calculadora.calcula()
    calculadora.exporta_para_excel(caminho_excel=caminho_saida_reenquadramento)


def run_from_argv(argv=None):
    """Analisa os argumentos da CLI e executa.

    Retorna 0 em caso de sucesso, um número diferente de zero em caso de falha.
    Este helper pode ser testado passando uma lista de argumentos em `argv`
    (excluindo o nome do programa).
    """
    parser = argparse.ArgumentParser(
        description="Exporta projeções a partir de planilha e parâmetros"
    )
    parser.add_argument(
        "caminho_projecao_excel", help="Caminho do arquivo de projeção (xlsx)"
    )
    parser.add_argument(
        "caminho_saida_reenquadramento",
        help="Caminho e nome do arquivo que conterá os resultados de reenquadramento",
    )

    args = parser.parse_args(argv)

    reenquadramento(
        args.caminho_projecao_excel,
        args.caminho_saida_reenquadramento,
    )
    return 0


if __name__ == "__main__":
    rv = run_from_argv(sys.argv[1:])
    sys.exit(rv)
