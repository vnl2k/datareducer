import csv
import os
import math
from typing import Dict, List, Any
from matplotlib import pyplot as plt
from matplotlib import rcParams
from matplotlib import font_manager as fontm
from datareducer import tree
from funkpy import Collection as _
from funkpy.utils import curry, compose

from colors import ZBW, Blue


GREY = ZBW.Z800
BACKGROUND = ZBW.Z25
DARK = ZBW.Z900

rcParams.update({
  'savefig.facecolor': BACKGROUND,
  'axes.facecolor': BACKGROUND,
  'axes.labelcolor': DARK,
  'axes.edgecolor': GREY,
  'xtick.color': GREY,
  'ytick.color': GREY,

  'xtick.labelsize': 'large',
  'ytick.labelsize': 'large',
  'axes.labelsize': 'large',

  'ytick.major.width': .3,
  'ytick.minor.width': .3,
  'xtick.major.width': .3,
  'xtick.minor.width': .3,
  'axes.linewidth': .3,

  'axes.spines.top': False,
  'axes.spines.right': False,

  # stops the renderer from embedding the font
  'svg.fonttype': 'none',

  'font.family': 'sans-serif',
  'font.sans-serif': 'Source Sans Pro'
  })

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = 'Source Sans Pro'

FILES = _.map(os.path.realpath, [
  './matrix_data.csv'
])

def readFile(file_name: str) -> None:
  with open(file_name, newline="\n") as file:
    data = csv.reader(file, delimiter=",")

    headers = next(data)

    return tree.apply(data, lambda i: [i[3], i[1], i[0]])

PIPE = compose(
  lambda i: i.sort() or i,
  curry(_.strictMap)(float),
  curry(_.filter)(lambda i: i != "cnt"),
  list)

# NOT IN USE AT THE MOMENT
def generateBarChart(leaf: Dict, names: List) -> None:
  x_keys = PIPE(leaf.keys())
  y_cnt = _.map(lambda i: math.log10(leaf[str(i)]['cnt']), x_keys)

  plt.bar(x_keys, y_cnt, width=0.1)
  ax = plt.gca()

  ax.set_xlabel("log val2")
  ax.set_ylabel("log Frequency")
  ax.set_xlim([-5, 5])

  plt.savefig('_'.join(names) + ".svg")

def generateHist(leaf: Dict, names: List) -> None:
  x_keys = PIPE(leaf.keys())
  y_cnt = _.concat(*_.map(lambda i: [i]*leaf[str(i)]['cnt'], x_keys))

  n, bins, patches = plt.hist(y_cnt, rwidth=0.8, log=True, range=(-5, 5), color=Blue.A700)
  ax = plt.gca()

  ax.set_xlabel("val2")
  ax.set_ylabel("log Frequency")

  plt.savefig('_'.join(names) + ".svg")
 

tree_dict = readFile(FILES[0])
branch = tree_dict['aa']['NA']

generateHist(branch, ['aa', 'NA'])
