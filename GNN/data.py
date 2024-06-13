import csv
import pandas as pd
import torch
from sklearn.preprocessing import StandardScaler, OneHotEncoder, MinMaxScaler
import numpy as np
import database as db


def get_node_features():
    with open('csv_my_data/data_gnn.csv', newline='') as csvfile:
        features = []
        labels = []
        edge_indices = []
        edge_attributes = []
        csvreader = csv.reader(csvfile)
        i = 0
        player_id = 0
        for row in csvreader:
            if i == 0:
                i += 1
                # print(row[19:21] + row[22:33] + row[21:22])
                continue

            player_name = row[0]
            opponent_name = row[1]
            if db.check_player(player_name) is None:
                db.insert_player(player_name, player_id)
                actual_player_id = player_id
                player_id += 1
                row_selected = row[5:7] + row[8:19] + row[7:8]
                features.append(row_selected)
            else:
                actual_player_id = db.check_player(player_name)
                # print(f"actual_player_id: {actual_player_id}")

            if db.check_player(opponent_name) is None:
                db.insert_player(opponent_name, player_id)
                opponent_player_id = player_id
                player_id += 1
                row_selected_opponent = row[19:21] + row[22:33] + row[21:22]
                features.append(row_selected_opponent)
            else:
                opponent_player_id = db.check_player(opponent_name)
                # print(f"opponent_player_id: {opponent_player_id}")

            edge_indices.append((actual_player_id, opponent_player_id))
            labels.append(row[33])
            # labels.append(1 - int(row[33]))
            i += 1
        file_name = 'csv_my_data/gnn_edge_indices.csv'
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in edge_indices:
                writer.writerow(row)
        print(f"Edge_indices has been written to {file_name} successfully.")

        np.savetxt('csv_my_data/gnn_labels.csv', np.array(labels, dtype=int), delimiter=',')
        print("Labels saved successfully")
        return features


def get_edge_attributes():
    with open('csv_my_data/tournament_data_gnn.csv') as csvfile:
        edge_attributes = []
        csvreader = csv.reader(csvfile)
        i = 0
        for row in csvreader:
            if i == 0:
                i += 1
                continue
            edge_attributes.append(row[0:4])
            i += 1
        one_hot_encoder = OneHotEncoder(sparse_output=False)  # Use sparse=False to get a dense array
        edge_attributes = one_hot_encoder.fit_transform(edge_attributes)
        file_name = 'csv_my_data/gnn_edge_attributes.csv'
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in edge_attributes:
                writer.writerow(row)
        print(f"Edge_indices has been written to {file_name} successfully.")
        print("Edge attributes saved successfully")
        return edge_attributes


# node_features = np.array(get_node_features())
# print(node_features)
# numerical_features = node_features[:, :-1]
# categorical_features = node_features[:, -1].reshape(-1, 1)
#
# one_hot_encoder = OneHotEncoder(sparse_output=False)  # Use sparse=False to get a dense array
# categorical_features_encoded = one_hot_encoder.fit_transform(categorical_features)

# numerical_features = numerical_features.reshape(numerical_features.shape[0], -1)
# combined_features = np.hstack((numerical_features, categorical_features_encoded))
# df = pd.DataFrame(combined_features)
# scaler = MinMaxScaler()
# node_features = scaler.fit_transform(combined_features)
# # np.savetxt('csv_my_data/gnn_features.csv', node_features, delimiter=',')
# file_name = 'csv_my_data/gnn_features.csv'
# with open(file_name, 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     for row in node_features:
#         writer.writerow(row)
# print(f"Edge_indices has been written to {file_name} successfully.")

get_edge_attributes()
