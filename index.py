import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Sample data (replace with your actual data or load from files)
drug_target_data = pd.DataFrame({
    'Drug': ['Drug1', 'Drug2', 'Drug3'],
    'Target': ['TargetA', 'TargetB', 'TargetC']
})

disease_gene_data = pd.DataFrame({
    'Disease': ['Disease1', 'Disease2', 'Disease3'],
    'Gene': ['GeneA', 'GeneB', 'GeneC']
})

# Function to construct drug-disease network
def construct_network(drug_target_data, disease_gene_data):
    G = nx.Graph()

    # Add drugs and diseases as nodes
    G.add_nodes_from(drug_target_data['Drug'], bipartite='drug')
    G.add_nodes_from(disease_gene_data['Disease'], bipartite='disease')

    # Add edges between drugs and targets, and diseases and genes
    G.add_edges_from([(row['Drug'], row['Target']) for _, row in drug_target_data.iterrows()])
    G.add_edges_from([(row['Disease'], row['Gene']) for _, row in disease_gene_data.iterrows()])

    return G

# Function to identify drugs with connections to multiple disease nodes
def identify_multi_disease_drugs(graph):
    multi_disease_drugs = set()

    for drug in graph.nodes:
        if graph.nodes[drug]['bipartite'] == 'drug':
            diseases = {neighbor for neighbor in graph.neighbors(drug) if graph.nodes[neighbor]['bipartite'] == 'disease'}
            
            if len(diseases) > 1:
                multi_disease_drugs.add(drug)

    return multi_disease_drugs

# Construct the network
drug_disease_network = construct_network(drug_target_data, disease_gene_data)

# Identify drugs with connections to multiple disease nodes
multi_disease_drugs = identify_multi_disease_drugs(drug_disease_network)
print("Drugs connected to multiple disease nodes:", multi_disease_drugs)

# Visualize the network (optional)
pos = {node: (1, i) if graph.nodes[node]['bipartite'] == 'drug' else (2, i) for i, node in enumerate(drug_disease_network.nodes)}
nx.draw(drug_disease_network, pos, with_labels=True, font_weight='bold', node_color='skyblue', node_size=800, font_size=10)
plt.show()
