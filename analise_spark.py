from pyspark.sql import SparkSession
from pyspark.sql.functions import count, desc, sum


def main():
    print("🚀 Iniciando Apache Spark...")
    # Inicializa a sessão do Spark para rodar localmente usando todos os núcleos disponíveis
    spark = (
        SparkSession.builder.appName("EcommerceBigDataAnalysis")
        .master("local[*]")
        .getOrCreate()
    )

    # Reduz os logs do Spark apenas para WARN, para não poluir o terminal
    spark.sparkContext.setLogLevel("WARN")

    print("📂 Carregando dados de transações do arquivo JSONL...")
    # Em Big Data, o Spark consegue ler e inferir esquemas de arquivos imensos de forma distribuída.
    df_transacoes = spark.read.json("dados/transacoes.jsonl")

    print("\n--- Esquema Inferido dos Dados ---")
    df_transacoes.printSchema()

    print("\n--- Top 10 Produtos por Faturamento ---")
    # Realiza agregações distribuídas: conta transações e soma o valor total agrupado por produto
    faturamento = (
        df_transacoes.groupBy("produto_id")
        .agg(
            count("id").alias("total_vendas"),
            sum("valor_total").alias("faturamento_total"),
        )
        .orderBy(desc("faturamento_total"))
    )

    faturamento.show(10)

    print("\n--- Top 10 Clientes com Maior Volume de Compras ---")
    clientes = (
        df_transacoes.groupBy("cliente_id")
        .agg(count("id").alias("qtd_compras"))
        .orderBy(desc("qtd_compras"))
    )

    clientes.show(10)

    print("\n--- Resumo de Status de Entrega ---")
    status = df_transacoes.groupBy("status").count().orderBy(desc("count"))
    status.show()

    # Salvando os Top Produtos para o Motor de Recomendação da API
    print("💾 Exportando resultados para o motor de recomendação...")
    import os

    if not os.path.exists("dados_processados"):
        os.makedirs("dados_processados")

    # Pegamos apenas os IDs dos Top 10 para salvar como um JSON simples
    top_produtos = [row["produto_id"] for row in faturamento.limit(10).collect()]

    import json

    with open("dados_processados/top_produtos.json", "w") as f:
        json.dump(top_produtos, f)

    print("✅ Análise concluída e recomendações geradas! Encerrando Spark.")
    spark.stop()


if __name__ == "__main__":
    main()
