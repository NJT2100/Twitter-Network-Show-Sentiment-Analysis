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

count = {}
with open(args.filename, mode='r') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)
    total = 0
    for row in reader:
        total += int(row[1])

    csv_file.seek(0)
    next(reader)
    for row in reader:
        if int(row[1]) / total > 0.01:
            count[row[0]] = int(row[1])
        else:
            if 'Other' in count.keys():
                count['Other'] += int(row[1])
            else:
                count['Other'] = int(row[1])

other = count.pop('Other')
# Sort on index 1, which contains the value which is a list
# Sort on the fouths column (compond)
count = sorted(count.items(), key=lambda v: float(v[1]), reverse=True)
count.append(['Other', other])
x = np.arange(len(count))  # the label locations
width = 0.55  # the width of the bars

#explode = [0] * len(count)
#explode[-5:] = [1 for x in explode[-5:]]

figure, ax = plot.subplots()

values = [float(item[1]) for item in count]
labels = [item[0] for item in count]

comp_bar = ax.pie(values, autopct='%1.1f%%', labels=labels, shadow=True, startangle=90)

ax.set_title('Twitter Mentions by Series')
ax.axis('equal')
ax.legend()

#figure.tight_layout()

#plot.legend(labels=labels)
plot.setp(ax.xaxis.get_majorticklabels(), rotation=270)
plot.savefig('figure_3-1.png')
plot.show()

# https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py