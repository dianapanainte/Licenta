import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data = pd.read_csv('data_all.csv', delimiter=',')

sns.set_style("whitegrid")
boxprops = dict(linestyle='-', linewidth=1.5, color='#00145A')
flierprops = dict(marker='o', markersize=1,
                  linestyle='none')
whiskerprops = dict(color='#00145A')
capprops = dict(color='#00145A')
medianprops = dict(linewidth=1.5, linestyle='-', color='#01FBEE')

plt.boxplot([data['Height']], tick_labels=['Height'], notch=False, boxprops=boxprops, whiskerprops=whiskerprops,capprops=capprops, flierprops=flierprops, medianprops=medianprops,showmeans=False)
plt.title("Height distribution")
plt.show()
