from math import floor, log10, fabs

def _log10(val: float) -> float:
  return log10(fabs(val))


def linearIndex(min_val: float, max_val: float, bin_width: float, max_ind: int, val: float) -> int:
  """Calculates the linear index of the corresponding bin.

  Arguments:
    min_val -- The minimum value of the scale
    max_val -- The maxomum value of the scale
    bin_width -- The number of bins of the scale
    max_ind -- The index of the last bin for that scale
  """

  if val < min_val:
    return None
  if val >= max_val:
    return None
 
  return floor((val-min_val)/bin_width)

def log10Index(min_val: float, max_val: float, bin_width: float, max_ind: int, val: float) -> int:
  """Calculates the log-10 index of the corresponding bin.

  Arguments:
    min_val {number} -- The minimum value of the scale
    max_val {number} -- The maxomum value of the scale
    bin_width {number} -- The number of bins of the scale
    max_ind {integer} -- The index of the last bin for that scale
  """

  if val < min_val:
    return None
  if val >= max_val:
    return None
  return floor(_log10(val/min_val)/bin_width)