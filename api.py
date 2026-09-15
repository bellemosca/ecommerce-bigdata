import json
import os

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from opensearchpy import OpenSearch
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="E-commerce Big Data API",
    description="API de Integração com OpenSearch e Spark para recomendações",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurações OpenSearch
OS_URI = "http://localhost:9200"
INDEX_NAME = "produtos_ecommerce"

# Instancia o cliente do OpenSearch
es = OpenSearch([OS_URI])

# Instrumentação para o Prometheus
Instrumentator().instrument(app).expose(app)

app.mount("/app", StaticFiles(directory="frontend", html=True), name="frontend")


@app.get("/")
def root():
    return RedirectResponse(url="/app")


@app.get("/buscar")
def buscar_produtos(q: str = Query(..., min_length=1, description="Termo de busca")):
    """
    Busca produtos no OpenSearch com suporte a erros de digitação (fuzziness).
    """
    if not es.ping():
        raise HTTPException(
            status_code=503, detail="Motor de busca (OpenSearch) está offline."
        )

    query = {
        "query": {
            "multi_match": {
                "query": q,
                # Presumindo campos comuns de produtos, ajuste caso o dataset tenha nomes diferentes
                "fields": [
                    "nome",
                    "categoria",
                    "descricao",
                    "name",
                    "category",
                    "description",
                ],
                "fuzziness": "AUTO",
            }
        },
        "size": 10,
    }

    try:
        response = es.search(index=INDEX_NAME, body=query)
        hits = response["hits"]["hits"]
        return {
            "termo_buscado": q,
            "total_encontrado": response["hits"]["total"]["value"],
            "resultados": [hit["_source"] for hit in hits],
        }
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Erro interno na busca: {e}")


@app.get("/recomendacoes")
def recomendacoes():
    """
    Retorna os Top 10 produtos que mais faturaram, pré-processados pelo Apache Spark.
    Busca os detalhes dos produtos no OpenSearch.
    """
    caminho_arquivo = "dados_processados/top_produtos.json"
    if not os.path.exists(caminho_arquivo):
        raise HTTPException(
            status_code=404,
            detail="Recomendações não encontradas. Rode o script do PySpark (analise_spark.py) primeiro.",
        )

    try:
        with open(caminho_arquivo, "r") as f:
            top_ids = json.load(f)

        # Busca no OpenSearch os detalhes de todos os produtos do ranking usando a lista de IDs
        query = {
            "query": {"terms": {"id": top_ids}},
            "size": len(top_ids),
        }

        response = es.search(index=INDEX_NAME, body=query)

        # Cria um dicionário para poder ordenar o resultado do OpenSearch
        # de acordo com a ordem exata gerada pelo Spark (do que mais faturou pro menor)
        produtos_dict = {
            hit["_source"]["id"]: hit["_source"] for hit in response["hits"]["hits"]
        }
        produtos_ordenados = [
            produtos_dict[int(pid)] for pid in top_ids if int(pid) in produtos_dict
        ]

        return {
            "origem": "Processamento Offline em Lote (Apache Spark)",
            "metrica": "Top Produtos por Faturamento",
            "recomendacoes": produtos_ordenados,
        }
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(e))
