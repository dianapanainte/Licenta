import torch
import pandas as pd
import dgl

node_features = torch.tensor(pd.read_csv('csv_my_data/gnn_features.csv').values, dtype=torch.float)
edge_indices = torch.tensor(pd.read_csv('csv_my_data/gnn_edge_indices.csv').values, dtype=torch.long).t().contiguous()
labels = torch.tensor(pd.read_csv('csv_my_data/gnn_labels.csv').values, dtype=torch.float)
edge_attributes = torch.tensor(pd.read_csv('csv_my_data/gnn_edge_attributes.csv').values, dtype=torch.float)

print(edge_indices)
src_nodes = edge_indices[0]
dst_nodes = edge_indices[1]

graph = dgl.graph((src_nodes, dst_nodes))
print(graph)
print(f"Number of nodes: {graph.num_nodes()}")
print(f"Number of edges: {graph.num_edges()}")

print(type(graph))
