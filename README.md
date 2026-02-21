# Analise-de-Dados-streamlit

## Sobre o projeto

Este projeto é um dashboard interativo desenvolvido em Python com Streamlit para análise de dados de vendas.

A proposta foi transformar um arquivo de vendas em informações estratégicas de forma visual e organizada, permitindo identificar padrões, crescimento mensal, desempenho de produtos e faturamento por cidade.

O sistema permite filtrar os dados por mês específico ou visualizar o ano completo.

---

## Tecnologias utilizadas

* Python
* Pandas
* Streamlit
* Plotly Express

---

## Funcionalidades

* Filtro por período (Ano todo ou mês específico)
* Cálculo de faturamento total
* Total de vendas e total de pedidos
* Crescimento percentual mês a mês
* Produto mais e menos vendido
* Produto com maior e menor faturamento
* Média de avaliação por produto
* Cidade com maior e menor volume de vendas
* Faturamento por categoria e cidade
* Visualização dos dados filtrados em tabela

---

## Estrutura do projeto

```
projeto/
│
├── app.py
├── vendas_loja.csv
└── README.md
```

---

## Como executar

1. Instale as dependências:

```
pip install streamlit pandas plotly
```

2. Execute o projeto:

```
streamlit run app.py
```

3. O navegador abrirá automaticamente com o dashboard.

---

## Objetivo

O foco deste projeto foi praticar:

* Manipulação de dados com Pandas
* Agrupamentos e métricas estratégicas
* Visualização de dados com Plotly
* Criação de dashboards interativos com Streamlit
* Organização e padronização de código seguindo boas práticas

---

## Melhorias futuras

* Comparação com período anterior
* Filtros adicionais (cidade, categoria, marca)
* Exportação de relatórios
* Deploy em nuvem

---

Projeto desenvolvido para fins de estudo e evolução na área de análise de dados.
