from setuptools import setup
from datashader.__init__ import __version__ as version, __name__ as name
import sys

SETUP_VARS = dict(
  name=name,
  version=version,
  url='https://github.com/vnl2k/Datashader',
  packages=['datashader'],
  install_requires=['numpy>=1.14.0'],
  author="vnl2k",
  license='MIT',
  python_requires='>=3.5'
)

# http://docs.cython.org/en/latest/src/reference/compilation.html#distributing-cython-modules
# https://stackoverflow.com/questions/32528560/using-setuptools-to-create-a-cython-package-calling-an-external-c-library#32537661
# https://stackoverflow.com/questions/9882447/cython-importerror-no-module-named-mymodule-how-to-call-a-cython-module-con
# https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html?highlight=cythonize
# read this!
# https://stackoverflow.com/questions/43163315/how-to-include-header-file-in-cython-correctly-setup-py

try:
  from setuptools.extension import Extension
  from Cython.Build import cythonize

 

  extensions = [
    Extension(
      "datashader.utils", 
      ["datashader/utils.c"]
    )
  ]

  # It is triggered only when building the installation package:
  #    python3 setup.py sdist
  # Otherwise, cythonize does NOT build the .c files from .pyx
  if "sdist" in sys.argv:
    cythonize("./datashader/utils.pyx")

  SETUP_VARS["install_requires"]
  SETUP_VARS.update({"zip_safe": False})
  SETUP_VARS.update({"ext_modules": cythonize(extensions)})

  setup(**SETUP_VARS)

except ImportError as e:
  setup(**SETUP_VARS)
