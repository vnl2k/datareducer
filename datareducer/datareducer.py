import math
from numbers import Number
from array import array

from numpy import empty, vectorize, arange
from funkpy import Collection as _
from typing import List, overload, Callable

from datareducer.data_container import DataContainer, SparseDataContainer

try:
  # pyximport imports directly .pyx files which have no external C-dependencies
  # It is used for dev purposes only!
  import pyximport
  pyximport.install()
  
  # helpers written in Cython
  from datareducer.utils import cLinearIndex as linearIndex, cLog10Index as log10Index

except ImportError as e:
  from datareducer.utils_py import linearIndex, log10Index


def _log10(val: float) -> float:
  return math.log10(math.fabs(val))


NO_INITIALIZATION = 'Please run `shader.init() before applying it on values'


class shader:
  def __init__(self):
    self.__data__ = None
    self.__min__ = list()
    self.__max__ = list()
    self.__bin_number__ = list()
    self.__bin_width__ = list()
    self.func = list()
    self.binType = list()
    self.__dimLength__ = None
    self.__lastDimInd__ = None
    self.__exec_params__ = None

  def __setLinLimits__(self, min_val, max_val, bin_count):
    if min_val > max_val:
      return self

    self.__min__.append(float(min_val))
    self.__max__.append(float(max_val))
    self.__bin_number__.append(bin_count)
    self.__bin_width__.append((max_val-min_val)/bin_count)
    self.func.append(linearIndex)
    self.binType.append('lin')
    return self

  def __setLog10Limits__(self, min_val, max_val, bin_count):
    if min_val > max_val:
      print('\nMin cannot be larger than max.')
      return self

    if min_val == 0:
      print('\nLog min cannot equal zero.')
      return self

    if bin_count == 0:
      return self

    self.__min__.append(float(math.fabs(min_val)))
    self.__max__.append(float(math.fabs(max_val)))
    self.__bin_number__.append(bin_count)
    self.__bin_width__.append(_log10(max_val/min_val)/bin_count)
    self.func.append(log10Index)
    self.binType.append('log10')
    return self

  def setLimits(self, min_value: float, max_value: float, bin_number: int, scale_type: ('lin', 'log10')='lin'):
    if scale_type == 'lin':
      return self.__setLinLimits__(min_value, max_value, bin_number)
    elif scale_type == 'log10':
      return self.__setLog10Limits__(min_value, max_value, bin_number)
    else:
      print("\nWrong scale type: \"{0}\". The permitted values are \"lin\" and \"log10\".".format(scale_type))
      return self

  def initialize(self):
    self.__data__ = empty(self.__bin_number__, dtype='object')

    self.__dimLength__ = len(self.func)

    self.__lastDimInd__ = self.__dimLength__ - 1 

    return self

  # shorter name than initialize
  def init(self):
    self.initialize()
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

class shaderArray(shader):
  def initialize(self, typecode: str = 'd'):
    self.__data__ = DataContainer(self.__bin_number__, typecode)
    
    self.__dimLength__ = len(self.func)

    self.__lastDimInd__ = self.__dimLength__ - 1

    self.__exec_params__ = _.map( \
      lambda f, ind: (f, self.__min__[ind], self.__max__[ind], self.__bin_width__[ind], self.__bin_number__[ind]-1), \
      self.func, range(self.__dimLength__))
    return self

  @overload
  def apply(self, arr: Number, lmbd: Callable, yValueIndex: int = None):
    pass
  def apply(self, arr: List[Number], lmbd: Callable, yValueIndex: int = None):
    """
      arr = [x1, x2, x3, ...]
    """

    if self.__data__ is None:
      raise Exception(NO_INITIALIZATION)

    if self.__dimLength__ == 1:
      func, *args = self.__exec_params__[0]
      ind = func(*args, arr)
      if ind is None:
        return self
      self.__data__.set([ind], lmbd(self.__data__.get([ind]), arr))

    else:
      inds = [func(*args, val) for ((func, *args), val) in zip(self.__exec_params__, arr)]

      # Points outside the set limits are ignored.
      if None in inds:
        return self
      y_val_ind = yValueIndex or self.__lastDimInd__
      y_val = arr[y_val_ind]
      self.__data__.set(inds, lmbd(self.__data__.get(inds), y_val))

    return self

  def getAgg(self):
    return self.__data__.toMatrix()


class sparseShader(shader):
  def initialize(self):
    self.__data__ = SparseDataContainer(self.__bin_number__)
    self.__exec_params__ = _.map( \
      lambda ind, f: (f, self.__min__[ind], self.__max__[ind], self.__bin_width__[ind], self.__bin_number__[ind]-1), \
      enumerate(self.func))
    return self