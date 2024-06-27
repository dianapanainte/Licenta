# read from F:\GithubCloning\Licenta\NeuralNetwork\csv_folder\data_all.csv
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('F:/GithubCloning/Licenta/NeuralNetwork/csv_folder/data_all.csv')
# print(data.head())

# data['Surface'] = data['Surface'].apply(lambda x: x if x in ['Clay', 'Hard', 'Grass'] else 'Other')
#
# print(data.groupby('Surface').size())
# data.groupby('Surface').size().plot(kind='bar')
# plt.show()

data['Tournament'] = data['Tournament'].apply(
    lambda x: x if x in ['Wimbledon', 'US Open', 'French Open', 'Australian Open', 'Olympics'] else 'Other')
print(data.groupby('Tournament').size())

tournament_counts = data.groupby('Tournament').size()
tournament_counts.plot(kind='pie', autopct='%1.1f%%', figsize=(8, 6))
plt.title('Distribution of Tournaments')
plt.ylabel('')
plt.show()

target_tournaments = ['Wimbledon', 'US Open', 'Australian Open', 'French Open', 'Olympics']

filtered_data = data[data['Tournament'].isin(target_tournaments)]
print(filtered_data.groupby('Tournament').size())
filtered_data.groupby('Tournament').size().plot(kind='pie', autopct='%1.1f%%')
plt.title('Distribution of Target Tournaments')
plt.ylabel('')
plt.show()
