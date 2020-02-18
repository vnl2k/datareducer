from typing import List, overload
from numbers import Number
import math

from numpy import empty, vectorize, arange
from funkpy import Collection as _

from datareducer.datareducer import baseClass, NO_INITIALIZATION, _log10



class shader(baseClass): # aka npArray

  def initialize(self):
    self.__data__ = empty(self.__bin_number__, dtype='object')

    self.__dimLength__ = len(self.func)

    self.__lastDimInd__ = self.__dimLength__ - 1 

    return self

  @overload
  def apply(self, arr: float, yValueIndex: int=None):
    pass
  def apply(self, arr: List[float], yValueIndex: int=None):
    """
      arr = [x1, x2, x3, ...]
    """

    if self.__data__ is None:
      raise Exception(NO_INITIALIZATION)

    if self.__dimLength__ == 1:
      arr = [arr]

    inds = tuple(_.map(lambda val, ind: self.func[ind](self.__min__[ind], self.__max__[ind], self.__bin_width__[ind], self.__bin_number__[ind]-1, val), arr, range(len(arr)) ))

    # Points outside the set limits are ignored.
    if None in inds:
      return self

    agg = self.__data__[inds]

    if agg is None:
      agg = self.__data__[inds] = {'cnt': 0, 'sum': 0, 'sum2': 0, 'min': 0, 'max': 0}

    agg['cnt'] += 1

    y_val_ind = yValueIndex or self.__lastDimInd__
    y_val = arr[y_val_ind]

    agg['sum'] += y_val
    agg['sum2'] += y_val*y_val

    if agg['min'] > y_val:
      agg['min'] = y_val
    if agg['max'] < y_val:
      agg['max'] = y_val

    return self

  def applyOnBatches(self, matrix: List[List[float]], yValueIndex: int=None):
    """
      matrix =
      [
        [x1, x2, x3, ...],
        [x1, x2, x3, ...],
        [x1, x2, x3, ...],
        ...
      ]
    """
    if self.__data__ is None:
      raise Exception(NO_INITIALIZATION)

    if isinstance(matrix[0], Number):
      print("Argument \"matrix\" can only be List[List[float]]!")
      return self


    zipMatrix = _.zip(*matrix)
    new_matrix = []

    for ind, f in enumerate(self.func):
      min_val = self.__min__[ind]
      max_val = self.__max__[ind]
      bin_width = self.__bin_width__[ind]
      bin_number = self.__bin_number__[ind]-1

      new_matrix.append(_.map(lambda val: f(min_val, max_val, bin_width, bin_number, val), zipMatrix[ind]))


    y_val_ind = yValueIndex or len(matrix[0]) - 1
    for item in _.zip(*new_matrix):
      inds = tuple(item)

      # Points outside the set limits are ignored.
      if None in inds:
        break
      agg = self.__data__[inds]

      if agg is None:
        agg = self.__data__[inds] = {'cnt': 0, 'sum': 0, 'sum2': 0, 'min': 0, 'max': 0}

      agg['cnt'] += 1

      y_val = item[y_val_ind]

      agg['sum'] += y_val
      agg['sum2'] += y_val*y_val

      if agg['min'] > y_val:
        agg['min'] = y_val
      if agg['max'] < y_val:
        agg['max'] = y_val

    return self


  def getAgg(self, agg: str = 'cnt') -> List:
    # vectorize() is a for-loop which can be replaced with a more optimised expression if needed.
    return vectorize(lambda i: i.get(agg) if i is not None else 0)(self.__data__).tolist()

  type_lookup = {
    'lin': lambda mn, mx, w: arange(mn,mx,w).tolist(),
    'log10': lambda mn, mx, w: list(map(lambda i: mn*math.pow(10,i), arange(0, _log10(mx/mn), w))),
  }

  def getDimension(self, ind: int):
    result = self.type_lookup.get(self.binType[ind])(self.__min__[ind], self.__max__[ind], self.__bin_width__[ind])
    return result
