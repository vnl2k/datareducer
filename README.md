# Datareducer

# Installation
```bash
pip install datareducer

# with optional Cython support
pip install datareducer[Cython]

# with optional Numpy support
pip install datareducer[numpy]

# or with both
pip install datareducer[Cython, numpy]

```
## Quick start

```python
from datareducer.reducers import pyArray as shader
# OR
from datareducer import shader 

data = [[1, 1e-6], [2,2e-5], [3,4e-4]]

# set limits for 2 dimensions for the shader
data_store = shader().setLimits(0, 20, 21).setLimits(1e-12, 1e-3, 100, scale_type="log10").init()
# The shader can have arbitrary number of dimensions. It can be used to construct a simple histogram if only one dimension is defined, i.e. 
oneD_store = shader().setLimits(0, 20, 21)
# or multiple dimensions
multi_store = shader() \
    .setLimits(0, 20, 21) \
    .setLimits(-10, 100, 200) \
    .setLimits(1, 1e6, 7, scale_type="log10")

# map a single pair of values to a bin of SUM
data_store.apply([4, 1e-7], lambda a, i: a + i, yValueIndex=1)
```


## API

### Reducers

#### pyArray (default)

#### npArray
```python
from datareducer.reducers import npArray as shader

data = [[1, 1e-6], [2,2e-5], [3,4e-4]]

# set limits for 2 dimensions for the shader
data_store = shader().setLimits(0, 20, 21).setLimits(1e-12, 1e-3, 100, scale_type="log10").init()
# The shader can have arbitrary number of dimensions. It can be used to construct a simple histogram if only one dimension is defined, i.e. 
oneD_store = shader().setLimits(0, 20, 21)
# or multiple dimensions
multi_store = shader() \
    .setLimits(0, 20, 21) \
    .setLimits(-10, 100, 200) \
    .setLimits(1, 1e6, 7, scale_type="log10")\
    .init()

# map values to bins
data_store.applyOnBatches(data, yValueIndex=1)
# named parameter yValueIndex refers to the position of the y-value in each pair

# map a single pair of values to a bin
data_store.apply([4, 1e-7], yValueIndex=1)

print(data_store.getAgg("cnt"))
```

In the example above `data_store` is an _aggregator_ or also know as a _sink_ in the context of data streams. This approach can be used on arbitrarily big dataset and each value or value-pairs can be efficiently streamed and aggregated in the shader. The shader stored the aggregates in a matrix or tensor whose size is determined by the number of bins for each dimension.

Aggregates can be extracted from the shader container:
```python
# Get value count per bin in a 2D matrix, because two dimensions were defined above
print(data_store.getAgg("cnt"))
# Assuming the right-most value is of interest
print(data_store.getAgg("min"))
# returns the min value for each bin
# or the max value
print(data_store.getAgg("max"))
print(data_store.getAgg("sum"))
print(data_store.getAgg("sum2"))

```
#### Tree
Based on Python `Dict`...

#### Sparse (under construction)
Based on `Immutables` module, which can be found here...


### JITs
Try with openai [triton](https://openai.com/blog/triton/).

## References
* http://stackoverflow.com/questions/4515874/searching-for-a-fast-efficient-histogram-algorithm-with-pre-specified-bins#4516105
