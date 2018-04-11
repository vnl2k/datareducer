# Datashader


## API

```python
from datashader import datashader

data = [[1,1], [2,2], [3,4]]

shader = datashader().setLimits(-20, 20, 100).setLimits(1e-12, 1e-3, 100, scale_type='log10').initialize()



```

## References
* http://stackoverflow.com/questions/4515874/searching-for-a-fast-efficient-histogram-algorithm-with-pre-specified-bins#4516105
* http://stackoverflow.com/questions/6824122/mapping-a-numpy-array-in-place
