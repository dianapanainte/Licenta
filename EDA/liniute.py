import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv('data_all.csv', delimiter=',')

def get_rank_age(data, tennis_player):
    rank = []
    age = []
    for line in data.iloc:
        if line.iloc[0] == tennis_player:
            age = np.append(age, line.iloc[8])
            rank = np.append(rank, line.iloc[9])
        elif line.iloc[1] == tennis_player:
            age = np.append(age, line.iloc[22])
            rank = np.append(rank, line.iloc[23])
    return age, rank

age1, rank1 = get_rank_age(data, 'Simona Halep')
age2, rank2 = get_rank_age(data, 'Serena Williams')

plt.plot(age1, rank1, 'bo', label='Simona Halep')
plt.plot(age2, rank2, 'ro', label='Serena Williams')
plt.legend()
plt.title("Rank by age")
plt.yscale('log')

plt.xlabel("Age")
plt.ylabel("Rank")

plt.show()
