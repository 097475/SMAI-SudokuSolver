import matplotlib.pyplot as plt
import pandas as pd

charts_folder = 'charts/'

name_of_run = "easy_arc"

output_file = "output_" + name_of_run + ".txt"

length_of_run = 50

# This probably is not the best way to do read the file but it works
df = pd.read_csv(output_file, delim_whitespace=True, header=None)
df['Solution'] = ''
for i in range(4, 85):
    df['Solution'] += df[i]
    df = df.drop(columns=i)

# T
plt.bar(list(range(length_of_run)), df[2].iloc[0:length_of_run], label='BT')
plt.bar(list(range(length_of_run)), df[2].iloc[length_of_run:2*length_of_run], label='BJ')
plt.bar(list(range(length_of_run)), df[2].iloc[2*length_of_run:3*length_of_run], label='CBJ')

plt.xlabel('Sudoku No.')
plt.ylabel('# nodes')
plt.legend()
plt.tight_layout()
plt.savefig(charts_folder+name_of_run + '_nodes')

plt.clf()

plt.bar(list(range(length_of_run)), df[3].iloc[0:length_of_run], label='BT')
plt.bar(list(range(length_of_run)), df[3].iloc[length_of_run:2*length_of_run], label='BJ')
plt.bar(list(range(length_of_run)), df[3].iloc[2*length_of_run:3*length_of_run], label='CBJ')

plt.xlabel('Sudoku No.')
plt.ylabel('Time (s)')
plt.legend()
plt.tight_layout()
plt.savefig(charts_folder+name_of_run + '_time')


# charts for individual algorithms

for j, t in enumerate(['nodes', 'time']):
    for i, v in enumerate(['BT', 'BJ', 'CBJ']):
        plt.clf()
        plt.bar(list(range(length_of_run)), df[j + 2].iloc[0 + (i * length_of_run):length_of_run + (i * length_of_run)], label=v)
        plt.xlabel('Sudoku No.')
        ylabel = '# nodes' if j == 0 else 'Time (s)'
        plt.ylabel(ylabel)
        plt.legend()
        plt.tight_layout()
        plt.savefig(charts_folder+name_of_run + '_' + t + '_' + v)


#boxplots

plt.clf()
plt.boxplot([df[2].iloc[0:length_of_run], df[2].iloc[length_of_run:2*length_of_run],
             df[2].iloc[2*length_of_run:3*length_of_run]], labels=["BT", "BJ", "CBJ"])
plt.xlabel('Algorithm')
plt.ylabel('# nodes')
plt.tight_layout()
plt.savefig(charts_folder+name_of_run + '_nodes_boxplot')

plt.clf()
plt.boxplot([df[3].iloc[0:length_of_run], df[3].iloc[length_of_run:2*length_of_run],
             df[3].iloc[2*length_of_run:3*length_of_run]], labels=["BT", "BJ", "CBJ"])
plt.xlabel('Algorithm')
plt.ylabel('Time (s)')
plt.tight_layout()
plt.savefig(charts_folder+name_of_run + '_time_boxplot')
