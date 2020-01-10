from typing import List, Tuple, Iterable
from array import array
from math import floor
from funkpy import Collection as _

try:
  from immutables import Map
except ImportError as import_err:
  pass


def calcPos1(dimLens: Iterable[int], indices: Iterable[int]):
  return indices[0]

def calcPos2(dimLens: Iterable[int], indices: Iterable[int]) -> int:
  return indices[0]*dimLens[1] + indices[1]

def calcPos3(dimLens: Iterable[int], indices: Iterable[int]) -> int:
  return indices[0]*(dimLens[1] * dimLens[2]) + indices[1]*dimLens[2] + indices[2]

class DataContainer:
  def __init__(self, dims: List[int], typecode: str = 'd'):
    length = _.reduce(lambda agg, i: agg*i, dims, 1)
     
    ls = array(typecode, range(length))
    
    dimsLen = len(dims)
    
    self.__buffer__ = ls
    print('Container size in memory: {0} KB'.format(len(ls)*ls.itemsize / 1024))

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
    return self.get(indices)

  def set(self, indices, val):
    self.__buffer__[self.__calcPos__(self.__dims__, indices)] = val
    return self

  def tolist(self):
    return self.__buffer__.tolist()

  def toIterable(self):
    def it():
      for i in self.__buffer__:
        yield i

    return it

class SparseDataContainer:
  def __init__(self, dims: List[int], typecode: str = 'd'):
    length = _.reduce(lambda agg, i: agg*i, dims, 1)
     
    sparseLS = Map().mutate()
    
    dimsLen = len(dims)
    
    self.__buffer__ = sparseLS
    # print('Container size in memory: {0} KB'.format(len(ls)*ls.itemsize / 1024))

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
    return self.get(indices)

  def set(self, indices, val):
    self.__buffer__[self.__calcPos__(self.__dims__, indices)] = val
    return self

class exports:
  container = DataContainer
  sparseContainer = SparseDataContainer