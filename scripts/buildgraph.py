import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

edges = pd.read_csv("../data/drug_disease.csv")
edges_gene = pd.read_csv("../data/gene_disease.csv")

G = nx.DiGraph()

for _, r in edges.iterrows():
    G.add_edge(r['drug_id'], r['disease_id'], relation='TREATS')

for _, r in edges_gene.iterrows():
    G.add_edge(r['gene_id'], r['disease_id'], relation='ASSOCIATED_WITH')

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)

labels = nx.get_edge_attributes(G,'relation')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

plt.savefig("../output/graph_visualization.png")
plt.show()