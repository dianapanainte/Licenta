# read from F:\GithubCloning\Licenta\NeuralNetwork\csv_folder\data_all.csv
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('F:/GithubCloning/Licenta/NeuralNetwork/csv_folder/data_all.csv')
# print(data.head())

# group surface by only clay, hard, grass, not carpet
# data['Surface'] = data['Surface'].apply(lambda x: x if x in ['Clay', 'Hard', 'Grass'] else 'Other')
#
#
# print(data.groupby('Surface').size())
# data.groupby('Surface').size().plot(kind='bar')
# plt.show()

# print(data.groupby('Hand').size())
# data.groupby('Hand').size().plot(kind='bar')
# plt.show()

# now for the tournaments
# a piechart just for the tournaments Wimbledon, US Open, French Open, Australian Open, Olympics, all the rest at other
data['Tournament'] = data['Tournament'].apply(
    lambda x: x if x in ['Wimbledon', 'US Open', 'French Open', 'Australian Open', 'Olympics'] else 'Other')
print(data.groupby('Tournament').size())

tournament_counts = data.groupby('Tournament').size()
tournament_counts.plot(kind='pie', autopct='%1.1f%%', figsize=(8, 6))
plt.title('Distribution of Tournaments')
plt.ylabel('')
plt.show()

target_tournaments = ['Wimbledon', 'US Open', 'Australian Open', 'French Open', 'Olympics']

# Filter the DataFrame to include only the target tournaments
filtered_data = data[data['Tournament'].isin(target_tournaments)]

# Print the size of each tournament group in the filtered data
print(filtered_data.groupby('Tournament').size())

# Plot the data as a pie chart
filtered_data.groupby('Tournament').size().plot(kind='pie', autopct='%1.1f%%')
plt.title('Distribution of Target Tournaments')
plt.ylabel('')
plt.show()
