from datareducer.datareducer import shaderArray as pyArray


try:
  from datareducer.npArray import shader as npArray
except:
  pass

try:
  from datareducer.datareducer import sparseShader as sparseArray
except:
  pass

try:
  from datareducer.tree_reducer import exports as tree
except:
  pass
