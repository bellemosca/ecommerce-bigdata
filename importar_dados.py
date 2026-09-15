import json
import os
import sys

from pymongo import MongoClient

# Configurações do MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "ecommerce_bigdata"
DATA_DIR = "dados"

BATCH_SIZE = 10000


def carregar_colecao(db, nome_arquivo, nome_colecao):
    caminho_arquivo = os.path.join(DATA_DIR, nome_arquivo)
    if not os.path.exists(caminho_arquivo):
        print(f"⚠️  Arquivo {caminho_arquivo} não encontrado. Pulando...")
        return

    colecao = db[nome_colecao]

    # Limpa a coleção antes de importar para garantir que não haja duplicação em múltiplos testes
    colecao.drop()
    print(f"⏳ Iniciando importação para a coleção '{nome_colecao}'...")

    batch = []
    total_inserido = 0

    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue

            try:
                documento = json.loads(linha)
                batch.append(documento)

                if len(batch) >= BATCH_SIZE:
                    colecao.insert_many(batch)
                    total_inserido += len(batch)
                    batch = []
                    print(f"  ... {total_inserido} documentos inseridos.")
            except json.JSONDecodeError:
                print("❌ Erro ao decodificar linha JSON.")
                continue

    if batch:
        colecao.insert_many(batch)
        total_inserido += len(batch)
        print(f"  ... {total_inserido} documentos inseridos.")

    print(
        f"✅ Importação concluída para '{nome_colecao}'. Total: {total_inserido} documentos.\n"
    )


def main():
    print("🔌 Conectando ao MongoDB...")
    try:
        client = MongoClient(MONGO_URI)
        # Testa a conexão
        client.admin.command("ping")
    except Exception as e:  # noqa: BLE001
        print(
            f"❌ Erro ao conectar no MongoDB. Certifique-se de que o serviço está rodando. Erro: {e}"
        )
        sys.exit(1)

    db = client[DB_NAME]

    arquivos_para_importar = [
        ("produtos.jsonl", "produtos"),
        ("clientes.jsonl", "clientes"),
        ("transacoes.jsonl", "transacoes"),
        ("avaliacoes.jsonl", "avaliacoes"),
    ]

    for arquivo, colecao in arquivos_para_importar:
        carregar_colecao(db, arquivo, colecao)

    print("🎉 Todas as coleções do MongoDB foram importadas com sucesso!")


if __name__ == "__main__":
    main()
