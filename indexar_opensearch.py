import sys

from opensearchpy import OpenSearch, helpers
from pymongo import MongoClient

# Config MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "ecommerce_bigdata"

# Config OpenSearch
OS_URI = "http://localhost:9200"


def main():
    print("🔌 Conectando ao MongoDB...")
    try:
        mongo_client = MongoClient(MONGO_URI)
        db = mongo_client[DB_NAME]
        produtos_col = db["produtos"]
        total_produtos = produtos_col.count_documents({})
        print(f"✅ Encontrados {total_produtos} produtos no MongoDB.")
    except Exception as e:  # noqa: BLE001
        print(f"❌ Erro ao conectar no MongoDB: {e}")
        sys.exit(1)

    print("\n🔌 Conectando ao OpenSearch...")
    es = OpenSearch([OS_URI])

    if not es.ping():
        print(
            "❌ Erro: Não foi possível conectar ao OpenSearch. O serviço está rodando?"
        )
        sys.exit(1)
    print("✅ Conectado ao OpenSearch.")

    index_name = "produtos_ecommerce"

    # Recria o índice para garantir que está zerado
    if es.indices.exists(index=index_name):
        print(f"🗑️  Removendo índice antigo '{index_name}'...")
        es.indices.delete(index=index_name)

    print(f"✨ Criando novo índice '{index_name}'...")
    es.indices.create(index=index_name)

    print("\n⏳ Gerando lotes de indexação a partir do MongoDB...")
    produtos = produtos_col.find()

    # Função geradora para não carregar todos os 100 mil produtos na memória RAM de uma vez
    def gerador_produtos():
        for p in produtos:
            doc_id = str(
                p.pop("_id")
            )  # Remove o _id original do mongo e usa como id do documento no opensearch
            yield {"_index": index_name, "_id": doc_id, "_source": p}

    print("🚀 Enviando para o OpenSearch (isso levará alguns instantes)...")
    success, _ = helpers.bulk(
        es, gerador_produtos(), chunk_size=5000, request_timeout=60
    )

    print(
        f"\n🎉 Sucesso! {success} produtos indexados no OpenSearch e prontos para busca rápida."
    )


if __name__ == "__main__":
    main()
