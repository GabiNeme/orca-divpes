# Orça DIVPES

O objetivo desse repositório é criar um sistema de orçamento com gastos de pessoal para a Câmara Municipal de Belo Horizonte, considerando diferentes critérios de aposentadoria, progressão, reajustes e os diversos tipos de servidores: efetivos, vereadores, amplos, à disposição.

Considerando a especificidade dos termos, seria inviável e pouco prático que esse repositório fosse em inglês, pois causaria mais confusão na tradução dos termos para quem for contribuir.

# (English) DIVPES Budget

This repository aims to estimate personnel expenses for the City Council of Belo Horizonte. It takes into account different criteria for retirement, progression, readjustments, and the different types of access: public tender, election, relocation, and recommendation.

Considering the used terms are very specific, it would be impracticable for this repository to be in English because we would likely have many misunderstoods and translation problems.

# Como executar

## A primeira vez
### Crie seu ambiente virtual
```
python -m venv venv
```
### Ative esse ambiente criado no passo anterior.

Para windows:
```
.\venv\Scripts\activate
```

Em Linux e Mac:
```
source venv/bin/activate
```
### Instale os pacotes necessários
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
## Da segunda vez em diante
Ative o ambiente virtual.

Para windows:
```
.\venv\Scripts\activate
```

Em Linux e Mac:
```
source venv/bin/activate
```


# Como executar a projeção

Para gerar a projeção, utilize o comando abaixo no terminal, estando no diretório do projeto e com o ambiente virtual ativado:

```
python main.py <caminho_projecao_excel> <ano_inicio> <ano_fim> <diretorio_resultado> [--recalcula-projecao] [--exporta-progressoes]
```

**Exemplo:**
```
python main.py dados/projecao.xlsx 2023 2025 resultados
```

- `<caminho_projecao_excel>`: Caminho para o arquivo Excel de projeção.
- `<ano_inicio>`: Ano inicial da projeção (ex: 2023).
- `<ano_fim>`: Ano final da projeção (ex: 2025).
- `<diretorio_resultado>`: Pasta onde os arquivos de resultado serão salvos.
- `--recalcula-projecao` (opcional): Recalcula as projeções antes de exportar.
- `--exporta-progressoes` (opcional): Exporta as progressões dos servidores.

Certifique-se de que o diretório de resultado existe e que você tem permissão de escrita nele.


## Rodar os testes
Execute:
```
pytest
```
Para executar os testes e medir sua cobertura, execute:
```
coverage run -m pytest
```
E para avaliar a cobertura dos testes:
```
coverage report -m
coverage html
```
