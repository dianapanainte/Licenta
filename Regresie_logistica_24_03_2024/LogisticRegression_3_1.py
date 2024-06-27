import pandas as pd
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import Features_3_0 as features


def one_hot_encoding(data):
    encoder = OneHotEncoder()
    surface_encoded = encoder.fit_transform(data[['Hand']])
    surface_encoded_df = pd.DataFrame(surface_encoded.toarray(), columns=encoder.get_feature_names_out(['Hand']))
    data.drop('Hand', axis=1, inplace=True)
    data = pd.concat([data, surface_encoded_df], axis=1)
    # -----------------------------------------------------------for opponent hand
    encoder = OneHotEncoder()
    surface_encoded = encoder.fit_transform(data[['Opponent_Hand']])
    surface_encoded_df = pd.DataFrame(surface_encoded.toarray(),
                                      columns=encoder.get_feature_names_out(['Opponent_Hand']))
    data.drop('Opponent_Hand', axis=1, inplace=True)
    data = pd.concat([data, surface_encoded_df], axis=1)
    return data


# prepare and scale data
feature_cols = ['Difference_in_ranks', 'Different_hand', 'Age', 'Rank', 'Height', 'Wins_semester',
                'Losses_semester',
                "Wins_year", "Losses_year", "Wins_clay", "Wins_hard", "Wins_grass", "Losses_clay", "Losses_hard",
                "Losses_grass", "Opponent_Age", "Opponent_Rank", "Opponent_Height", "Opponent_Wins_semester",
                "Opponent_Losses_semester", "Opponent_Wins_year", "Opponent_Losses_year", "Opponent_Wins_clay",
                "Opponent_Wins_hard", "Opponent_Wins_grass", "Opponent_Losses_clay", "Opponent_Losses_hard",
                "Opponent_Losses_grass"]

data_training = pd.DataFrame(features.training_data())
data_training = one_hot_encoding(data_training)
X_train = data_training[feature_cols]
y_train = data_training.Outcome

n_samples, n_features = X_train.shape
print(f'number of samples: {n_samples}, number of features: {n_features}')

value_counts = y_train.value_counts()

print("Value counts:")
print(value_counts)

data_testing = pd.DataFrame(features.testing_data())
data_testing = one_hot_encoding(data_testing)
X_test = data_testing[feature_cols]
y_test = data_testing.Outcome

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

X_train = torch.from_numpy(X_train.astype(np.float32))
X_test = torch.from_numpy(X_test.astype(np.float32))
y_train = torch.from_numpy(y_train.to_numpy().astype(np.float32))
y_test = torch.from_numpy(y_test.to_numpy().astype(np.float32))

y_train = y_train.view(y_train.shape[0], 1)
y_test = y_test.view(y_test.shape[0], 1)


class LogisticRegression(nn.Module):

    def __init__(self, n_input_features):
        super(LogisticRegression, self).__init__()
        self.linear = nn.Linear(n_input_features, 1)

    def forward(self, x):
        y_predicted = torch.sigmoid(self.linear(x))
        return y_predicted


model = LogisticRegression(n_features)

learning_rate = 0.01
criterion = nn.BCELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

num_epochs = 1000

for epoch in range(num_epochs):
    y_predicted = model(X_train)
    loss = criterion(y_predicted, y_train)
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

    if (epoch + 1) % 100 == 0:
        print(f'epoch: {epoch + 1}, loss = {loss.item():.4f}')

with torch.no_grad():
    y_predicted = model(X_test)
    y_predicted_cls = y_predicted.round()
    acc = y_predicted_cls.eq(y_test).sum() / float(y_test.shape[0])
    print(f'accuracy = {acc:.4f}')
    #########################
    y_true = np.array(y_test)
    y_pred = np.array(y_predicted_cls)

    cm = metrics.confusion_matrix(y_true, y_pred)
    # cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[0, 1])
    # cm_display.plot()
    # plt.show()
    # plt.savefig('plots/confusion_matrix_features_3_0_2004-2010_pytorch.png')

    # sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    # plt.title('Confusion Matrix')
    # plt.xlabel('Predicted')
    # plt.ylabel('True')
    # plt.show()
    # plt.savefig('plots/confusion_matrix_features_3_0_2004-2010_pytorch.jpg')

    # fig = plt.figure()
    # plt.matshow(cm)
    # plt.title('Confusion Matrix')
    # plt.colorbar()
    # plt.ylabel('True Label')
    # plt.xlabel('Predicted Label')
    # plt.show()
    # plt.savefig('plots/confusion_matrix_features_3_0_2004-2010_pytorch.jpg')

    # the only way I found to actually save this, not just show it
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    tick_marks = np.arange(len(np.unique(y_true)))
    plt.xticks(tick_marks, np.unique(y_true))
    plt.yticks(tick_marks, np.unique(y_true))
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], 'd'),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > cm.max() / 2. else "black")
    plt.tight_layout()
    plt.savefig('plots/try1.png')
    plt.show()
