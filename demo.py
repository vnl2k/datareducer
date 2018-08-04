import sys
import functools as ft
from itertools import repeat
sys.path.append("/home/nemo/Documents/SourceControl/BlackBoxData/PythonModulesClasses")
sys.path.append("/home/nemo/Documents/SourceControl/BlackBoxData/fileDB")
sys.path.append("/home/nemo/Documents/SourceControl/Datashader/datashader")

import numpy as np
from matplotlib import colors
from matplotlib.cm import ScalarMappable

from doc_db import doc, docDB
from datashader import datashader as dsh
import fig

def generate_data(y_order):
  """Generates dummy data for the demo."""
  x_data = list(range(-10, 10, 1))
  y_data = list(map(lambda i: i*y_order, range(0, 100, 10)))
  y_data.reverse()
  rev_y_data = y_data.copy()
  rev_y_data.reverse()
  y_data.extend(rev_y_data)
  return list(zip(x_data, y_data))



shader = dsh().setLimits(-10, 10, 50).setLimits(1, 100, 50, scale_type='log10').initialize()
shader.apply(generate_data(1))
# shader.apply(generate_data(1e-12))



def _xdata(bin, reps):
  return ft.reduce(lambda agg, i: agg.extend(repeat(i, reps)) or agg, bin, [])

def _ydata(bin, reps):
  return ft.reduce(lambda agg, i: agg.extend(bin) or agg, range(reps), [])


xBins = shader.getDimension(0)
yBins = shader.getDimension(1)


f = fig.newFig()
ax = fig.newAxes(f)
norm = colors.LogNorm(1, max(max(shader.getAgg('cnt'))), clip=False)
cmap = colors.Colormap('gray_r').set_under(color=[0,0,0], alpha=None)
color_map = ScalarMappable(norm=norm, cmap=cmap).to_rgba

color_data = ft.reduce(lambda agg, i: agg.extend(i) or agg, shader.getAgg('cnt'), [])
# color_data = ft.reduce(lambda agg, i: agg.extend(color_map(i)) or agg, shader.getAgg('cnt'), [])
# ax.scatter(_xdata(xBins, len(yBins)),
#   _ydata(yBins, len(xBins)), 
#   c=color_data,
#   marker='s',
#   s=1)

# color_data = ft.reduce(lambda agg, i: agg.append(color_map(i)) or agg, np.array(shader.getAgg('cnt')).transpose(), [])
# ax.imshow(color_data, extent=(-10,10,100,0))

# ax.set_xlim(-10, 10)
ax.set_ylim(0.1, 1000)
ax.set_yscale('log')
fig.savefig('JVcurves', path='./', extn='pdf')