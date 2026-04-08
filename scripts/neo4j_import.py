from neo4j import GraphDatabase
import pandas as pd

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j","password"))


def run(q):
    with driver.session() as s:
        s.run(q)

# Load data
drugs = pd.read_csv("../data/drugs.csv")
diseases = pd.read_csv("../data/diseases.csv")
genes = pd.read_csv("../data/genes.csv")
drug_disease = pd.read_csv("../data/drug_disease.csv")
gene_disease = pd.read_csv("../data/gene_disease.csv")

# Clear old data
run("MATCH (n) DETACH DELETE n")

# Create nodes
for _, r in drugs.iterrows():
    run(f"CREATE (:Drug {{id:'{r.id}', name:'{r.name}'}})")

for _, r in diseases.iterrows():
    run(f"CREATE (:Disease {{id:'{r.id}', name:'{r.name}'}})")

for _, r in genes.iterrows():
    run(f"CREATE (:Gene {{id:'{r.id}', name:'{r.name}'}})")

# Create relationships
for _, r in drug_disease.iterrows():
    run(f"""
    MATCH (d:Drug {{id:'{r.drug_id}'}}),(ds:Disease {{id:'{r.disease_id}'}})
    CREATE (d)-[:TREATS]->(ds)
    """)

for _, r in gene_disease.iterrows():
    run(f"""
    MATCH (g:Gene {{id:'{r.gene_id}'}}),(ds:Disease {{id:'{r.disease_id}'}})
    CREATE (g)-[:ASSOCIATED_WITH]->(ds)
    """)

print("Graph Imported Successfully!")