#!/bin/bash
echo "=========================================="
echo "🚀 INICIANDO O AMBIENTE BIG DATA E-COMMERCE"
echo "=========================================="

echo "📦 1. Iniciando Banco NoSQL (MongoDB)..."
# Roda o mongo em background na pasta local (silenciosamente)
nohup mongod --dbpath .mongodb_data > mongod.log 2>&1 &
sleep 2

echo "🔍 2. Iniciando Motor de Busca (OpenSearch)..."
brew services start opensearch

echo "📈 3. Iniciando Monitoramento (Grafana)..."
brew services start grafana

echo "📊 4. Iniciando Coletor de Métricas (Prometheus)..."
# Roda o prometheus lendo o arquivo local (silenciosamente)
nohup prometheus --config.file=prometheus.yml > prometheus.log 2>&1 &

echo "=========================================="
echo "✅ SERVIÇOS DE INFRAESTRUTURA NO AR!"
echo " - Grafana: http://localhost:3000"
echo " - Prometheus: http://localhost:9090"
echo " - OpenSearch: http://localhost:9200"
echo "=========================================="

# ── Carga de dados (roda apenas na primeira vez) ───────────────────────────

if [ ! -f .flag_dados_importados ]; then
    echo "📥 Importando dados no MongoDB (primeira execução)..."
    uv run importar_dados.py && touch .flag_dados_importados
else
    echo "✅ MongoDB já populado — pulando importação."
fi

if [ ! -f .flag_opensearch_indexado ]; then
    echo "🔎 Indexando produtos no OpenSearch (primeira execução)..."
    echo "⏳ Aguardando OpenSearch inicializar..."
    until curl -s http://localhost:9200 > /dev/null 2>&1; do
        printf "."
        sleep 2
    done
    echo " ✓ OpenSearch pronto!"
    uv run indexar_opensearch.py && touch .flag_opensearch_indexado
else
    echo "✅ OpenSearch já indexado — pulando indexação."
fi

if [ ! -f .flag_spark_analisado ]; then
    echo "⚡ Rodando análise com Apache Spark (primeira execução)..."
    uv run analise_spark.py && touch .flag_spark_analisado
else
    echo "✅ Análise Spark já realizada — pulando."
fi

echo "=========================================="

echo "🌐 Subindo a API do E-commerce (FastAPI)..."
echo "Pressione CTRL+C a qualquer momento para parar a API."
echo "Para acessar a aplicação abra: http://localhost:8000"

# Mata qualquer processo que tenha ficado travado na porta 8000
kill -9 $(lsof -t -i:8000) 2>/dev/null

uv run uvicorn api:app --reload
