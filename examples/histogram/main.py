from random import gauss
from matplotlib import colors
from matplotlib.cm import ScalarMappable
from matplotlib.pyplot import bar, savefig

# imports class datareducer from module datareducer
from datareducer import shader


data_store = shader().setLimits(-15, 15, 25)

i = 0
while i < 10000:
  data_store.apply(gauss(0, 5))
  i += 1

bar(data_store.getDimension(0), data_store.getAgg('cnt'), align="edge")

savefig('histogram.jpg', dpi=200, format="jpg", transparent=True)
