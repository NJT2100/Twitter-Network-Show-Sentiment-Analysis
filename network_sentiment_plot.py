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
# Sort on the fourth column (compond)
sentiment = sorted(sentiment.items(), key=lambda v: v[1][3], reverse=True)
sentiment = sentiment[:10]
x = np.arange(len(sentiment))  # the label locations
width = 0.55  # the width of the bars

figure, ax = plot.subplots()

neg = [float(item[1][0]) for item in sentiment]
neu = [float(item[1][1]) for item in sentiment]
pos = [float(item[1][2]) for item in sentiment]

pos_bar = ax.bar(x, pos, color='#b5ffb9', edgecolor='white', width=width, label='pos')
neu_bar = ax.bar(x, neu, color='#f9bc86', edgecolor='white', width=width, label='neu', bottom=pos)
neg_bar = ax.bar(x, neg, color='#a3acff', edgecolor='white', width=width, label='neg', bottom=[i+j for i, j in zip(pos, neu)])

ax.set_title('Network Sentiment Based on Series')
ax.set_ylabel('Sentiment')
ax.set_xticks(x)
ax.set_xticklabels([item[0] for item in sentiment])
ax.legend()

#figure.tight_layout()

plot.setp(ax.xaxis.get_majorticklabels(), rotation=315)
plot.savefig('figure_3-1.png', bbox_inches='tight')
plot.show()

# https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py