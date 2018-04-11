import numpy as np
import math


def _log10(val):
	return math.log10(math.fabs(val));
		
def _linInd(mn, mx, binW, maxInd):
	def ind(val):
		if (val<=mn): return 0
		if (val>=mx): return maxInd
		return math.floor((val-mn)/binW)
	return ind;

def _log10Ind(mn, mx, binW, maxInd):
	def ind(val):
		if (val<=mn): return 0
		if (val>=mx): return maxInd
		return math.floor(_log10(val/mn)/binW)
	return ind;


class datashader:
	def __init__(self):
		self.__data__ = None
		self.__min__ = list()
		self.__max__ = list()
		self.__bin_number__ = list()
		self.binW = list()
		self.func = list()
		self.binType = list()

	def __setLinLimits__(self, mn, mx, binLen):
		if (mn>mx): return self

		self.__min__.append(mn)
		self.__max__.append(mx)
		self.__bin_number__.append(binLen)
		self.binW.append((mx-mn)/binLen)
		self.func.append(_linInd)
		self.binType.append('lin')
		return self

	def __setLog10Limits__(self, mn, mx, binLen):
		if (mn>mx): return self
		if (mn==0): return self
		if (binLen==0): return self

		self.__min__.append(math.fabs(mn))
		self.__max__.append(math.fabs(mx))
		self.__bin_number__.append(binLen)
		self.binW.append(_log10(mx/mn)/binLen)
		self.func.append(_log10Ind)
		self.binType.append('log10')
		return self

	def setLimits(self, min, max, bin_number, scale_type='lin'):
		if scale_type == 'lin': return self.__setLinLimits__(min, max, bin_number)
		elif scale_type == 'log10': return self.__setLog10Limits__(min, max, bin_number)
		else: 
			print("Wrong scale type: \"{0}\". The permitted values are \"lin\" and \"log10\".".format(scale_type))
			return self

	def initialize(self):

		# np.vectorize() is a for-loop and can be replaced with a more optimised expression if needed.
		self.__data__= np.vectorize(lambda i: {'cnt': 0, 'sum': 0, 'sum2': 0, 'min': 0, 'max': 0})(np.empty(self.__bin_number__,dtype='object'))
		return self

	# matrix = 
	# [
	# 	[x1, x2, x3, ..., y],
	# 	[x1, x2, x3, ..., y],
	# 	[x1, x2, x3, ..., y]
	# ]
	def apply(self, matrix):
		if self.__data__ is None: return self

		# _values_to_index: an list of functions which calculates the corresponding indices
		_values_to_index = list(
			map(
				lambda _f,ind: _f(self.__min__[ind], self.__max__[ind], self.binW[ind], self.__bin_number__[ind]-1), 
				self.func, # _f
				range(len(self.func)) # ind 
			)
		)
		
		y_val_ind = len(matrix[0])-1
		for i in range(len(matrix)):
			inds = tuple(map(lambda _f, val: int(_f(val)), _values_to_index, matrix[i]))
			agg = self.__data__[inds]
			agg['cnt'] +=1
			y_val = matrix[i][y_val_ind]
			agg['sum'] += y_val
			agg['sum2'] += y_val*y_val
			if agg['min']>y_val: agg['min'] = y_val 
			if agg['max']<y_val: agg['max'] = y_val 

		return self

	def getAgg(self, agg):
		# np.vectorize() is essentially a for-loop and can be replaced with a more optimised expression if needed.
		return np.vectorize(lambda i: i.get(agg))(self.__data__).tolist()

	def getBin(self,ind):
		def _genBin(mn,mx,w,tp):
			_typeGen = {
				'lin': lambda mn,mx,w: np.arange(mn,mx,w),
				'log10': lambda mn,mx,w: list(map(lambda i: mn*math.pow(10,i), np.arange(0,_log10(mx/mn),w))),
				# 'log10': lambda mn,mx,w:  np.arange(mn,mx,math.pow(10,w)),
			}
			return _typeGen[tp](mn,mx,w)

		return _genBin(self.__min__[ind], self.__max__[ind], self.binW[ind], self.binType[ind])

	linInd = _linInd;
	log10Ind = _log10Ind;

