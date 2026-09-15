# E-commerce Big Data

Este projeto é parte da Atividade Prática 14 – Distribuída e Bancos de Dados em Big Data. O objetivo é implementar uma solução eficiente para buscar e analisar dados de um e-commerce em tempo real, utilizando bancos de dados distribuídos (NoSQL) e pipelines de processamento.

## Pré-requisitos

O ambiente foi configurado para rodar nativamente no macOS. Certifique-se de ter os seguintes gerenciadores instalados:
- **Homebrew** (para serviços do sistema)
- **uv** (para gerenciamento de dependências Python)

## Instalação e Configuração

### 1. MongoDB (Armazenamento NoSQL)
Utilizado para gerenciar os grandes volumes de dados brutos do e-commerce.

```bash
# Adicionar o repositório do MongoDB
brew tap mongodb/brew

# Instalar a versão Community
brew install mongodb-community

# Iniciar o serviço em segundo plano
brew services start mongodb-community
```

*(Para parar o serviço futuramente, use: `brew services stop mongodb-community`)*

### 2. OpenSearch (Busca Distribuída)
Utilizado para o sistema de busca rápida de produtos e avaliações. (Substituto compatível do Elasticsearch)

```bash
# Instalar o OpenSearch
brew install opensearch

# Iniciar o serviço em segundo plano
brew services start opensearch
```

*(Para parar o serviço futuramente, use: `brew services stop opensearch`)*

### 3. Prometheus (Coletor de Métricas)
Utilizado para monitoramento e coleta de métricas do sistema e da API.

```bash
# Instalar o Prometheus
brew install prometheus
```

### 4. Grafana (Dashboard de Monitoramento)
Utilizado para visualizar as métricas coletadas pelo Prometheus.

```bash
# Instalar o Grafana
brew install grafana

# Iniciar o serviço em segundo plano
brew services start grafana
```

*(Para parar o serviço futuramente, use: `brew services stop grafana`)*

### 5. Ambiente Python
O projeto utiliza o `uv` para gerenciar dependências. Após clonar o projeto, instale o ambiente virtual e todas as dependências (PySpark, PyMongo, Elasticsearch, etc.) executando:

```bash
uv sync
```

## Dados
Os dados sintéticos do projeto (compostos de produtos, clientes, transações e avaliações) pesam em torno de centenas de megabytes. Por isso, eles foram compactados. 

Antes de rodar qualquer passo abaixo, certifique-se de extrair o arquivo ZIP na raiz do projeto (ele já criará a pasta `dados/` automaticamente):
```bash
# Extraia o arquivo zip antes de rodar os scripts
unzip ecommerce_bigdata_1_65_milhao_documentos.zip
```

Para popular o MongoDB com a massa de dados inicial, certifique-se de que o MongoDB esteja rodando e execute o script em Python incluído no projeto:

```bash
# Executar a ingestão no MongoDB
uv run importar_dados.py
```

### Motor de Busca (OpenSearch)
Após popular o MongoDB, você precisa indexar os produtos no OpenSearch para o sistema de busca rápida. Execute o script de indexação:

```bash
# Sincroniza os produtos do MongoDB com o OpenSearch
uv run indexar_opensearch.py
```

### Processamento Distribuído (Apache Spark)
Para processar e analisar o enorme volume de dados de transações, criamos um script utilizando o **PySpark**. O script lê os dados brutos e efetua agregações (ex: produtos que mais faturaram, volume de transações por meio de pagamento).

```bash
# Roda a análise de Big Data com PySpark
uv run analise_spark.py
```

## Subindo o Projeto (Modo Fácil)

Como a infraestrutura tem vários serviços (banco de dados, motor de busca, coletor de métricas, dashboard e API), eu criei dois scripts mágicos que você ou seu professor podem rodar na raiz do projeto:

### 1. Iniciar Tudo
Para ligar toda a infraestrutura e a API de uma vez só:
```bash
./iniciar_projeto.sh
```
*Ao final do script, ele já vai manter a API rodando no seu terminal (acesse `http://localhost:8000/docs`).*

### 2. Parar Tudo
Quando você terminar de apresentar ou testar o trabalho, abra outra aba do terminal e rode:
```bash
./parar_projeto.sh
```
*Isso vai garantir que nenhum serviço do banco de dados ou monitoramento fique rodando oculto no fundo e gastando bateria do seu Mac.*
