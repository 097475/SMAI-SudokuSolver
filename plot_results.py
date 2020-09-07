import matplotlib.pyplot as plt
import pandas as pd

name_of_run = "easy_arc"

output_file = "output_" + name_of_run + ".txt"

# This probably is not the best way to do read the file but it works
df = pd.read_csv(output_file, delim_whitespace=True, header=None)
df['Solution'] = ''
for i in range(4, 85):
    df['Solution'] += df[i]
    df = df.drop(columns=i)

# T
plt.bar(list(range(50)), df[2].iloc[0:50], label='BT')
plt.bar(list(range(50)), df[2].iloc[50:100], label='BJ')
plt.bar(list(range(50)), df[2].iloc[100:150], label='CBJ')

plt.xlabel('Sudoku No.')
plt.ylabel('# nodes')
plt.legend()
plt.tight_layout()
plt.savefig(name_of_run + '_nodes')

plt.clf()

plt.bar(list(range(50)), df[3].iloc[0:50], label='BT')
plt.bar(list(range(50)), df[3].iloc[50:100], label='BJ')
plt.bar(list(range(50)), df[3].iloc[100:150], label='CBJ')

plt.xlabel('Sudoku No.')
plt.ylabel('Time (s)')
plt.legend()
plt.tight_layout()
plt.savefig(name_of_run + '_time')
