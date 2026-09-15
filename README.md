# E-commerce Big Data

Este projeto é parte da Atividade Prática 14 – Distribuída e Bancos de Dados em Big Data. O objetivo é implementar uma solução eficiente para buscar e analisar dados de um e-commerce em tempo real, utilizando bancos de dados distribuídos (NoSQL) e pipelines de processamento.

---

## Passo a passo de configuração

Siga os passos abaixo **na ordem apresentada** para configurar o ambiente do zero.

---

### Passo 1 – Instalar as dependências Python

Após clonar o repositório, instale o ambiente virtual e todas as dependências Python (PySpark, PyMongo, Elasticsearch, etc.) com o `uv`:

```bash
uv sync
```

> **Pré-requisito:** o `uv` precisa estar instalado. Caso não tenha, instale com:
> ```bash
> curl -LsSf https://astral.sh/uv/install.sh | sh
> ```

---

### Passo 2 – Extrair os dados

Os dados sintéticos do projeto (produtos, clientes, transações e avaliações) pesam centenas de megabytes e estão compactados. Extraia o arquivo ZIP na raiz do projeto — ele criará a pasta `dados/` automaticamente:

```bash
unzip ecommerce_bigdata_1_65_milhao_documentos.zip
```

---

### Passo 3 – Instalar os serviços via Homebrew

O projeto roda nativamente no **macOS e Linux**. Em ambos os sistemas, utilizamos o **Homebrew** como gerenciador de pacotes.

> **Pré-requisito:** o **Homebrew** precisa estar instalado. Ele funciona tanto no macOS quanto no Linux. Caso não tenha, instale com:
> ```bash
> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
> ```
> No Linux, após instalar, adicione o Homebrew ao PATH conforme instruído no terminal.

> **Usuários Linux (alternativa):** se preferir usar o gerenciador de pacotes nativo da sua distro (apt, dnf, pacman, etc.), os serviços abaixo também estão disponíveis nos repositórios oficiais. Consulte a documentação de cada um para a instalação via pacote nativo.

#### 3.1 MongoDB (Armazenamento NoSQL)
Utilizado para gerenciar os grandes volumes de dados brutos do e-commerce.

```bash
# Adicionar o repositório do MongoDB
brew tap mongodb/brew

# Instalar a versão Community
brew install mongodb-community

# Iniciar o serviço em segundo plano
brew services start mongodb-community
```

#### 3.2 OpenSearch (Busca Distribuída)
Utilizado para o sistema de busca rápida de produtos e avaliações. (Substituto compatível do Elasticsearch)

```bash
# Instalar o OpenSearch
brew install opensearch

# Iniciar o serviço em segundo plano
brew services start opensearch
```

#### 3.3 Prometheus (Coletor de Métricas)
Utilizado para monitoramento e coleta de métricas do sistema e da API.

```bash
# Instalar o Prometheus
brew install prometheus
```

#### 3.4 Grafana (Dashboard de Monitoramento)
Utilizado para visualizar as métricas coletadas pelo Prometheus.

```bash
# Instalar o Grafana
brew install grafana

# Iniciar o serviço em segundo plano
brew services start grafana
```

---

## Passo 4 – Iniciar o projeto

Com os serviços instalados e os dados extraídos, basta rodar o script de inicialização:

```bash
./iniciar_projeto.sh
```

**Na primeira execução**, o script detecta que os dados ainda não foram carregados e faz tudo automaticamente:
1. Importa os dados no MongoDB
2. Indexa os produtos no OpenSearch
3. Roda a análise com Apache Spark

**Nas execuções seguintes**, essas etapas são puladas e a API sobe direto.

*A API ficará disponível em `http://localhost:8000/docs`.*

---

## Encerrando o projeto

Quando terminar, rode em outro terminal:

```bash
./parar_projeto.sh
```

*Isso garante que nenhum serviço fique rodando oculto em segundo plano.*
