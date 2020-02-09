from typing import List, Tuple, Iterable
from array import array
from math import floor
import numbers
from funkpy import Collection as _


def calcPos1(dimLens: Iterable[int], indices: Iterable[int]):
  return indices[0]

def calcPos2(dimLens: Iterable[int], indices: Iterable[int]) -> int:
  return indices[0]*dimLens[1] + indices[1]

def calcPos3(dimLens: Iterable[int], indices: Iterable[int]) -> int:
  return indices[0]*(dimLens[1] * dimLens[2]) + indices[1]*dimLens[2] + indices[2]

class DataContainer:
  def __init__(self, dims: List[int], typecode: str = 'd', silent=False):
    length = _.reduce(lambda agg, i: agg*i, dims, 1)
     
    ls = array(typecode, map(lambda i: 0, range(length)))
    
    dimsLen = len(dims)
    
    self.__buffer__ = ls
    if silent is False:
      print('\nContainer size in memory: {0} KB'.format(len(ls)*ls.itemsize / 1024))

    self.__dims__ = dims

    if dimsLen == 1:
      self.__calcPos__ = calcPos1
    
    elif dimsLen == 2:
      self.__calcPos__ = calcPos2
    
    elif dimsLen == 3:
      self.__calcPos__ = calcPos3

  def get(self, indices: Tuple[int]):
    return self.__buffer__[self.__calcPos__(self.__dims__, indices)]

  def __getitem__(self, indices: Tuple[int]):
    if isinstance(indices, numbers.Number):
      indices = [indices]
    return self.get(indices)

  def set(self, indices: List[int], val):
    self.__buffer__[self.__calcPos__(self.__dims__, indices)] = val
    return self

  def tolist(self):
    return self.__buffer__.tolist()

  def toIterable(self):
    def it():
      for i in self.__buffer__:
        yield i

    return it

  def toMatrix(self):
    dimsLen = len(self.__dims__)
    if dimsLen == 1:
      return self.tolist()

    dimsReverse = self.__dims__.copy()
    dimsReverse.reverse()
    buffer = self.__buffer__.tolist()
    newBuffer = []
    ind = 0
    
    for size in dimsReverse:
      
      while ind < len(buffer):
        newBuffer.append(buffer[ind : ind + size])
        ind += size

      buffer = newBuffer
      newBuffer = []
      ind = 0

    return buffer[0]

try:
  from immutables import Map
  class SparseDataContainer:
    def __init__(self, dims: List[int]):
      length = _.reduce(lambda agg, i: agg*i, dims, 1)
       
      sparseLS = Map().mutate()
      
      dimsLen = len(dims)
      
      self.__buffer__ = sparseLS

      self.__dims__ = dims

      if dimsLen == 1:
        self.__calcPos__ = calcPos1
      
      elif dimsLen == 2:
        self.__calcPos__ = calcPos2
      
      elif dimsLen == 3:
        self.__calcPos__ = calcPos3

    def get(self, indices: Tuple[int]):
      return self.__buffer__[self.__calcPos__(self.__dims__, indices)]

    def __getitem__(self, indices: Tuple[int]):
      if isinstance(indices, numbers.Number):
        indices = [indices]

      return self.get(indices)

    def set(self, indices, val):
      self.__buffer__[self.__calcPos__(self.__dims__, indices)] = val
      return self

except ImportError as import_err:
  SparseDataContainer = None



class exports:
  container = DataContainer
  sparseContainer = SparseDataContainer