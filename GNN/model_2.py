import pandas as pd
import torch
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader
from torch_geometric.nn import GCNConv
import torch.nn as nn
import torch.optim as optim
from torch_geometric.nn import MessagePassing
from torch_geometric.utils import add_self_loops, degree


class GraphConvolution(MessagePassing):
    def __init__(self, in_channels, out_channels):
        super(GraphConvolution, self).__init__(aggr='add')
        self.lin = nn.Linear(in_channels, out_channels)

    def forward(self, x, edge_index, edge_attr):
        x = self.lin(x)
        return self.propagate(edge_index, size=(x.size(0), x.size(0)), x=x, edge_attr=edge_attr)

    def message(self, x_j, edge_attr):
        return x_j * edge_attr.view(-1, 1)


class GNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(GNN, self).__init__()

        self.conv1 = GraphConvolution(input_dim, hidden_dim)
        self.conv2 = GraphConvolution(hidden_dim, output_dim)

    def forward(self, x, edge_index, edge_attr):
        x = F.relu(self.conv1(x, edge_index, edge_attr))
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv2(x, edge_index, edge_attr)
        return F.log_softmax(x, dim=1)



input_dim = 16
hidden_dim = 64
output_dim = 2

model = GNN(input_dim, hidden_dim, output_dim)

node_features = torch.tensor(pd.read_csv('csv_my_data/gnn_features.csv').values, dtype=torch.float)
num_nodes = node_features.size(0) + 1

edge_indices = torch.tensor(pd.read_csv('csv_my_data/gnn_edge_indices.csv').values, dtype=torch.long).t().contiguous()
labels = torch.tensor(pd.read_csv('csv_my_data/gnn_labels.csv').values, dtype=torch.float)
edge_attributes = torch.tensor(pd.read_csv('csv_my_data/gnn_edge_attributes.csv').values, dtype=torch.float)

num_edges = edge_indices.size(1)
split_idx = int(0.75 * num_edges)

train_edge_indices = edge_indices[:, :split_idx]
test_edge_indices = edge_indices[:, split_idx:]

train_edge_attributes = edge_attributes[:split_idx]
test_edge_attributes = edge_attributes[split_idx:]

train_labels = labels[:split_idx]
test_labels = labels[split_idx:]

train_data = Data(x=node_features, edge_index=train_edge_indices, edge_attr=train_edge_attributes, y=train_labels,
                  num_nodes=num_nodes)
test_data = Data(x=node_features, edge_index=test_edge_indices, edge_attr=test_edge_attributes, y=test_labels,
                 num_nodes=num_nodes)

train_loader = DataLoader(train_data, batch_size=64, shuffle=False)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)


def train_model(model, train_loader, optimizer, criterion, num_epochs=10):
    model.train()
    for epoch in range(num_epochs):
        running_loss = 0.0
        for data in train_loader:
            optimizer.zero_grad()
            out = model(data.x, data.edge_index, data.edge_attr)
            loss = criterion(out, data.y)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * data.num_graphs
        print(f"Epoch {epoch + 1}, Loss: {running_loss / len(train_loader.dataset)}")


train_model(model, train_loader, optimizer, criterion)


def test_model(model, test_loader):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for data in test_loader:
            out = model(data.x, data.edge_index, data.edge_attr)
            _, predicted = torch.max(out, 1)
            total += data.y.size(0)
            correct += (predicted == data.y).sum().item()
    print(f"Test Accuracy: {100 * correct / total}%")


test_model(model, test_loader)
