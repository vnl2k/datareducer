import csv
from funkpy import Collection as _
import numpy as np

from matplotlib import colors
from matplotlib.cm import ScalarMappable
from matplotlib.pyplot import imshow, savefig, axis

import datareducer

shader = datareducer.shader().setLimits(40.4, 41.0, 5000).setLimits(-74.5, -73.5, 5000, scale_type='lin')


# The CSV data can be downloaded here:
#   https://github.com/fivethirtyeight/uber-tlc-foil-response/tree/master/uber-trip-data
FILES = [
  "uber-raw-data-sep14.csv",
  "uber-raw-data-apr14.csv",
  "uber-raw-data-aug14.csv",
  "uber-raw-data-jun14.csv",
  "uber-raw-data-jul14.csv",
  "uber-raw-data-may14.csv"
]

def readFile(file_name: str) -> None:
  with open(file_name, newline="\n") as file:
    data = csv.reader(file, delimiter=",")

    headers = next(data)

    # Processing the data in batches is slightly more efficient 
    # than calling shader.apply for each and every row.
    j = 0
    queue = []
    for i in data:
      if j < 700:
        queue.append(_.map(float, i[1:3]))
        j += 1

      else:
        j = 0
        shader.applyOnBatches(queue)
        queue = []

    if len(queue) > 0:
      shader.applyOnBatches(queue)

for f in FILES:
  readFile(f)

# trims the final data horizonally and vertically 
CNT_MATRIX = shader.getAgg('cnt')[2000:4000]
MAX_CNT = max(max(CNT_MATRIX))
CNT_MATRIX = _.zip(*CNT_MATRIX)[2000:4000]

# total count
TOTAL_CNT = sum(_.map(sum, CNT_MATRIX))
print("Total number of Uber rides in NYC: {0}".format(TOTAL_CNT))



norm = colors.LogNorm(1, MAX_CNT, clip=True)
cmap = colors.Colormap('gray_r').set_under(color=[0, 0, 0], alpha=None)

# color_map converts count to RGB
# color_map is very slow if used on python list
color_map = ScalarMappable(norm=norm, cmap=cmap).to_rgba

# reversed the numpy array with [::-1]
# converted bin count to RGB color using color_map
CNT_MATRIX = np.array(_.zip(*CNT_MATRIX), dtype=np.int)
color_data = _.map(lambda i: color_map(i), CNT_MATRIX[::-1])

# plot the count matrix as an image
f = imshow(color_data)
axis('off')
savefig('figure.jpg', dpi=500, format="jpg", transparent=True)
