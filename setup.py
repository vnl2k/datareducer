from setuptools import setup
from datashader import __version__

from Cython.Build import cythonize


setup(
  name="Datashader",
  version=__version__,
  url='https://github.com/vnl2k/Datashader',
  packages=['datashader'],
  install_requires=['numpy>=1.14.0'],
  author="vnl2k",
  license='MIT',
  python_requires='>=3.4',
  ext_modules=cythonize("./datashader/utils.pyx")
)
