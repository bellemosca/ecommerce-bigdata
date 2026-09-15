#!/bin/bash
echo "🛑 PARANDO OS SERVIÇOS DO PROJETO..."

echo "Parando MongoDB..."
pkill -f "mongod --dbpath .mongodb_data"

echo "Parando Prometheus..."
pkill -f "prometheus --config.file=prometheus.yml"

echo "Parando OpenSearch (Homebrew)..."
brew services stop opensearch

echo "Parando Grafana (Homebrew)..."
brew services stop grafana

echo "✅ Todos os serviços foram desligados com sucesso!"
