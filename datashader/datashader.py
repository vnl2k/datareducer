import math
import numpy as np


def _log10(val):
  return math.log10(math.fabs(val))

def _linInd(min_val, max_val, bin_count, max_ind):
  def ind(val):
    if val <= min_val:
      return 0
    if val >= max_val:
      return max_ind
    return math.floor((val-min_val)/bin_count)
  return ind

def _log10Ind(min_val, max_val, bin_count, max_ind):
  def ind(val):
    if val <= min_val:
      return 0
    if val >= max_val:
      return max_ind
    return math.floor(_log10(val/min_val)/bin_count)
  return ind


class datashader:
  def __init__(self):
    self.__data__ = None
    self.__min__ = list()
    self.__max__ = list()
    self.__bin_number__ = list()
    self.__bin_width__ = list()
    self.func = list()
    self.binType = list()

  def __setLinLimits__(self, min_val, max_val, bin_count):
    if min_val > max_val:
      return self

    self.__min__.append(min_val)
    self.__max__.append(max_val)
    self.__bin_number__.append(bin_count)
    self.__bin_width__.append((max_val-min_val)/bin_count)
    self.func.append(_linInd)
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

    self.__min__.append(math.fabs(min_val))
    self.__max__.append(math.fabs(max_val))
    self.__bin_number__.append(bin_count)
    self.__bin_width__.append(_log10(max_val/min_val)/bin_count)
    self.func.append(_log10Ind)
    self.binType.append('log10')
    return self

  def setLimits(self, min_value, max_value, bin_number, scale_type='lin'):
    if scale_type == 'lin':
      return self.__setLinLimits__(min_value, max_value, bin_number)
    elif scale_type == 'log10':
      return self.__setLog10Limits__(min_value, max_value, bin_number)
    else:
      print("\nWrong scale type: \"{0}\". The permitted values are \"lin\" and \"log10\".".format(scale_type))
      return self

  def initialize(self):

    # np.vectorize() is a for-loop and can be replaced with a more optimised expression if needed.
    # self.__data__ = np.vectorize(lambda i: {'cnt': 0, 'sum': 0, 'sum2': 0, 'min': 0, 'max': 0})(np.empty(self.__bin_number__, dtype='object'))
    self.__data__ = np.empty(self.__bin_number__, dtype='object')
    return self


  def apply(self, matrix):
    """
      matrix =
      [
        [x1, x2, x3, ..., y],
        [x1, x2, x3, ..., y],
        [x1, x2, x3, ..., y],
        ...
      ]
    """
    if self.__data__ is None:
      return self

    # _values_to_index: a list of functions which calculates the corresponding indices
    _values_to_index = list(
      map(
        lambda _f,ind: _f(self.__min__[ind], self.__max__[ind], self.__bin_width__[ind], self.__bin_number__[ind]-1),
        self.func, # _f
        range(len(self.func)) # ind
      )
    )

    y_val_ind = len(matrix[0]) - 1
    for i, val in enumerate(matrix):
      inds = tuple(map(lambda _f, val: int(_f(val)), _values_to_index, matrix[i]))
      agg = self.__data__[inds]

      if agg is None:
        agg = self.__data__[inds] = {'cnt': 0, 'sum': 0, 'sum2': 0, 'min': 0, 'max': 0}

      agg['cnt'] += 1

      y_val = val[y_val_ind]

      agg['sum'] += y_val
      agg['sum2'] += y_val*y_val

      if agg['min'] > y_val:
        agg['min'] = y_val
      if agg['max'] < y_val:
        agg['max'] = y_val

    return self

  def getAgg(self, agg):
    # np.vectorize() is a for-loop and can be replaced with a more optimised expression if needed.
    return np.vectorize(lambda i: i.get(agg) if i is not None else 0)(self.__data__).tolist()

  type_lookup = {
    'lin': lambda mn,mx,w: np.arange(mn,mx,w).tolist(),
    'log10': lambda mn,mx,w: list(map(lambda i: mn*math.pow(10,i), np.arange(0, _log10(mx/mn), w))),
  }

  def getDimension(self, ind):
    result = self.type_lookup.get(self.binType[ind])(self.__min__[ind], self.__max__[ind], self.__bin_width__[ind])
    result.append(self.__max__[ind])
    return result
