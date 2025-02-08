from google.cloud import bigquery

client = bigquery.Client()

# Definicao de projeto e tabelas de exemplo
projeto = "meu_projeto"
dataset = "meu_dataset"
tabela_pesquisa = "tabela_pesquisa"
tabela_fases = "tabela_fases"

# Query SQL para buscar a fase correspondente e, caso não exista, definir como 'Fase 1'
query = f"""
SELECT 
    p.*, 
    COALESCE(f.fase, 'Fase 1') AS fase 
FROM `{projeto}.{dataset}.{tabela_pesquisa}` p
LEFT JOIN `{projeto}.{dataset}.{tabela_fases}` f
ON p.numero_pergunta = f.numero_pergunta
"""

# Executar a consulta e armazenar os resultados em um DataFrame Pandas
df = client.query(query).to_dataframe()

# Exibir os primeiros resultados
print(df.head())