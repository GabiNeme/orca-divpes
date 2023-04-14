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

## Rodar os testes
Execute:
```
pytest
```
