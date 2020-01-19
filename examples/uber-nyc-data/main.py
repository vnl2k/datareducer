import csv
import os
from typing import Generator, List
from funkpy import Collection as _
import numpy as np
import time

from matplotlib import colors
from matplotlib.cm import ScalarMappable
from matplotlib.pyplot import imshow, savefig, axis, matshow
from matplotlib.animation import FuncAnimation


import datareducer

shader = datareducer \
  .shader() \
  .setLimits(40.4, 41.0, 2000) \
  .setLimits(-74.1, -73.7, 2000, scale_type='lin')


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

def fileStream(file_name: str, bathcSize: int = 700) -> Generator[List[List[float]], None, List[List[float]]]:
  with open(file_name, newline="\n") as file:
    data = csv.reader(file, delimiter=",")

    headers = next(data)
    # yield headers;

    j = 0
    queue = []
    for i in data:
      if j < bathcSize:
        queue.append(_.map(float, i[1:3]))
        j += 1

      else:
        j = 0
        yield queue
        queue = []

    if len(queue) > 0:
      return queue

def streamFromFiles(files: List[str])-> Generator[List[List[float]], None, None]:
  streamList = _.map(lambda f: fileStream(f), files)

  for stream in streamList:
    while stream:
      s = next(stream, None)
      if s == None:
        break
      else:
        yield s

  return None

norm = colors.LogNorm(1, 500, clip=True)
cmap = colors.Colormap('gray_r').set_under(color=[0, 0, 0], alpha=None)
# color_map converts count to RGB
# color_map is very slow if used on python list
color_map = ScalarMappable(norm=norm, cmap=cmap).to_rgba

def getShapshot(shader, color_map):
  # map the count to RGB colors
  # this is necessary for imshow to work
  return _.map(lambda i: color_map(i), shader.getAgg('cnt'))

def writeImg(colorData):
  # plot the count matrix as an image
  f = imshow(colorData)
  axis('off')
  savefig('figure .png', dpi=500, format="png", transparent=True)


stream = streamFromFiles(FILES)
ind = 0

startTime = time.monotonic()

batch = next(stream, None)
while batch:
  shader.applyOnBatches(batch)
  batch = next(stream, None)


CNT_MATRIX = shader.getAgg('cnt')
MAX_CNT = max(max(CNT_MATRIX))

print("Maximun count of Uber rides in NYC: {0}".format(MAX_CNT))

# total count
TOTAL_CNT = sum(_.map(sum, CNT_MATRIX))
print("Total number of Uber rides in NYC: {0}".format(TOTAL_CNT))


writeImg(_.map(lambda i: color_map(i), CNT_MATRIX))

endTime = time.monotonic() - startTime
print(f"   Processing time:\t\t\t{endTime:.4f}s")