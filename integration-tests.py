import unittest as ut
from datashader import datashader

data = []

from tests.tests import run
tests = ut.TestLoader().loadTestsFromTestCase(run(datashader, data, ut))
ut.TextTestRunner(verbosity=2).run(tests)
