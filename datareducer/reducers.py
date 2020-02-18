from datareducer.datareducer import ShaderArray as pyArray


try:
  from datareducer.npArray import Shader as npArray
except:
  pass

try:
  from datareducer.datareducer import SparseShader as sparseArray
except:
  pass

try:
  from datareducer.tree_reducer import exports as tree
except:
  pass
