import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


def read_data(file_path):
    with open(file_path, 'r') as file:
        data = [float(line.strip()) for line in file]
    return data


def komma_formatter(x, pos):
    return f"{x:,.2f}".replace('.', ',')


# Dateien einlesen
data_file1 = "frame_times_method_2.txt"
data_file2 = "frame_times_method_3.txt"

data1 = read_data(data_file1)
data2 = read_data(data_file2)

# Erstelle zwei Subplots
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

plt.suptitle('Benötigte Zeit pro Frame')

# Erstes Subplot
ax1.boxplot(data1)
ax1.set_ylabel('Zeit (s)')
ax1.set_title('Verfahren 1')
ax1.set_xticks([])

# Zweites Subplot
ax2.boxplot(data2)
ax2.set_title('Verfahren 2')
ax2.set_xticks([])

# Formatierung der Achsenbeschriftung
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(komma_formatter))
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(komma_formatter))

plt.savefig('frame_times.svg', format='svg')
plt.show()
