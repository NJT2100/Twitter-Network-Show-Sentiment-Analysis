import csv
import sys
import operator
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plot

parser = argparse.ArgumentParser(description="Create the plots")
parser.add_argument("filename")
args = parser.parse_args()

sentiment = {}
with open(args.filename, mode='r') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)
    for row in reader:
        sentiment[row[0]] = row[1:]

# Sort on index 1, which contains the value which is a list
# Sort on the fouths column (compond)
sentiment = sorted(sentiment.items(), key=lambda v: float(v[1][3]), reverse=True)
# sentiment = sentiment[:10]

x = np.arange(len(sentiment))  # the label locations
width = 0.55  # the width of the bars

figure, ax = plot.subplots()

comp_bar = ax.bar(x, [float(item[1][3]) for item in sentiment], color='#000080', edgecolor='white', width=width, label='Compound')

ax.set_title('Series Twitter Sentiment')
ax.set_ylabel('Sentiment (Compound)')
ax.set_xticks(x)
ax.set_xticklabels([item[0] for item in sentiment])
ax.legend()

#figure.tight_layout()

plot.setp(ax.xaxis.get_majorticklabels(), rotation=270)
plot.savefig('figure_3-1.png', bbox_inches='tight')
plot.show()

# https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py