import unittest as ut
from datashader import datashader

DATA = []

from tests.tests import run
tests = ut.TestLoader().loadTestsFromTestCase(run(datashader, DATA, ut))
ut.TextTestRunner(verbosity=2).run(tests)
