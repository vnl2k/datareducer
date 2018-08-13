import unittest as ut
from datareducer import shader

DATA = []

from tests.tests import run
tests = ut.TestLoader().loadTestsFromTestCase(run(shader, DATA, ut))
ut.TextTestRunner(verbosity=2).run(tests)
