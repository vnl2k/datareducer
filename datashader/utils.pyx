
from libc cimport math

def _log10(double val):
  return math.log10(math.fabs(val))


def cLinearIndex(float min_val, float max_val, float bin_width, long max_ind, float val):
  #   """Calculates the linear index of a bin.

  #   Arguments:
  #     min_val -- The minimum value of the scale
  #     max_val -- The maxomum value of the scale
  #     bin_width -- The number of bins of the scale
  #     max_ind -- The index of the last bin for that scale
  #     val -- The value to be mapped to bin index
  #   """
 
  if val <= min_val:
    return 0
  if val >= max_val:
    return max_ind

  return int(math.floor((val-min_val)/bin_width))

def cLog10Index(float min_val, float max_val, float bin_width, int max_ind, float val):
  #   """Calculates the log10 index of a bin.

  #   Arguments:
  #     min_val -- The minimum value of the scale
  #     max_val -- The maxomum value of the scale
  #     bin_width -- The number of bins of the scale
  #     max_ind -- The index of the last bin for that scale
  #     val -- The value to be mapped to bin index
  #   """

  if val <= min_val:
    return 0
  if val >= max_val:
    return max_ind
  return int(math.floor(_log10(val/min_val)/bin_width))

