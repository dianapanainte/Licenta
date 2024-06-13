import pandas as pd
import torch
import torch.nn.functional as F
import torch_geometric
from torch_geometric.data import Data
from tensorflow import data
from torch_geometric.loader import DataLoader
from torch_geometric.nn import GCNConv
import torch.nn as nn

in_channels = 16
hidden_channels = 16


class TennisMatchGNN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels):
        super(TennisMatchGNN, self).__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.linear = torch.nn.Linear(hidden_channels, 1)
        self.dropout = torch.nn.Dropout(p=0.5)

    def forward(self, data):
        print(data)
        x, edge_index, edge_attr = data.x, data.edge_index, data.edge_attr
        x = self.conv1(x, edge_index, edge_attr)
        x = F.relu(x)
        x = self.dropout(x)
        x = self.conv2(x, edge_index, edge_attr)
        x = F.relu(x)
        x = self.dropout(x)
        x = self.linear(x).squeeze()
        return x


node_features = torch.tensor(pd.read_csv('csv_my_data/gnn_features.csv').values, dtype=torch.float)
edge_indices = torch.tensor(pd.read_csv('csv_my_data/gnn_edge_indices.csv').values, dtype=torch.long).t().contiguous()
labels = torch.tensor(pd.read_csv('csv_my_data/gnn_labels.csv').values, dtype=torch.float)
edge_attributes = torch.tensor(pd.read_csv('csv_my_data/gnn_edge_attributes.csv').values, dtype=torch.float)

num_nodes = node_features.size(0)
num_edges = edge_indices.size(1)

split_idx = int(0.75 * num_edges)

train_edge_indices, test_edge_indices = torch.split(edge_indices, split_idx, dim=1)
train_edge_attributes, test_edge_attributes = torch.split(edge_attributes, split_idx, dim=0)
train_labels, test_labels = torch.split(labels, split_idx, dim=0)

train_data = Data(x=node_features, edge_index=train_edge_indices, edge_attr=train_edge_attributes, y=train_labels)
test_data = Data(x=node_features, edge_index=test_edge_indices, edge_attr=test_edge_attributes, y=test_labels)

model = TennisMatchGNN(in_channels, hidden_channels)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

criterion = torch.nn.MSELoss()

# train_loader = DataLoader(train_data, batch_size=64, shuffle=False)
# test_loader = DataLoader(test_data, batch_size=64)
# train_dataset = data.Dataset.from_tensor_slices(train_data)
# test_dataset = data.Dataset.from_tensor_slices(test_data)


def train(model, optimizer, criterion, train_loader):
    model.train()
    print(train_loader)
    for data in train_loader:
        print(data)
        optimizer.zero_grad()
        out = model(data)
        loss = criterion(out, data.y)
        loss.backward()
        optimizer.step()


def test(model, criterion, test_loader):
    model.eval()
    test_loss = 0
    with torch.no_grad():
        for data in test_loader:
            out = model(data)
            test_loss += criterion(out, data.y).item()
    test_loss /= len(test_loader.dataset)
    return test_loss


for epoch in range(100):
    # train(model, optimizer, criterion, train_loader.dataset)
    train(model, optimizer, criterion, train_data)
    print(f"Epoch {epoch + 1}")

# test_loss = test(model, criterion, test_loader.dataset)
test_loss = test(model, criterion, test_data)
print(f"Test Loss: {test_loss:.4f}")
