from random import gauss
from matplotlib import colors
from matplotlib.cm import ScalarMappable
from matplotlib.pyplot import bar, savefig

# imports class datareducer from module datareducer
from datareducer import datareducer


shader = datareducer().setLimits(-15, 15, 25)

i = 0
while i < 10000:
  shader.apply(gauss(0, 5))
  i += 1

print(shader.getDimension(0))
print(shader.getAgg('cnt'))
bar(shader.getDimension(0), shader.getAgg('cnt'), align="edge")

savefig('histogram.jpg', dpi=200, format="jpg", transparent=True)
