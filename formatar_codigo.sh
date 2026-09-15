#!/bin/bash
echo "🖌️  Formatando o código Python..."
uv run ruff format .

echo "🛠️  Verificando e corrigindo problemas de Linting (se houver)..."
uv run ruff check --fix .

echo "✅ Código formatado com sucesso!"
