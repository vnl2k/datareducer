from setuptools import setup
from datashader import __version__, __name__

SETUP_VARS = dict(
  name="Datashader",
  version=__version__,
  url='https://github.com/vnl2k/Datashader',
  packages=['datashader'],
  install_requires=['numpy>=1.14.0'],
  author="vnl2k",
  license='MIT',
  python_requires='>=3.5'
)

try:
  from Cython.Build import cythonize
  
  SETUP_VARS["install_requires"].append("cython>=0.28")
  SETUP_VARS.update("ext_modules", cythonize("./datashader/utils.pyx"))

  setup(SETUP_VARS)

except ImportError as e:
  setup(SETUP_VARS)
