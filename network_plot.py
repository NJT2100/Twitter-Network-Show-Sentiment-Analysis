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

x = np.arange(len(sentiment.keys()))  # the label locations
width = 0.35  # the width of the bars

figure, ax = plot.subplots()
neg_bar = ax.bar(x - width/3, [float(item[0]) for item in sentiment.values()], width/3, label='neg')
neu_bar = ax.bar(x, [float(item[1]) for item in sentiment.values()], width/3, label='neu')
neg_bar = ax.bar(x + width/3, [float(item[2]) for item in sentiment.values()], width/3, label='pos')

ax.set_title('Streaming Service Sentiment')
ax.set_ylabel('Sentiment')
ax.set_xticks(x)
ax.set_xticklabels(sentiment.keys())
ax.legend()

#figure.tight_layout()

plot.setp(ax.xaxis.get_majorticklabels(), rotation=270)
plot.savefig('figure_1-1.png', bbox_inches='tight')
plot.show()

# https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py