import unittest as ut
from datareducer import datareducer

DATA = []

from tests.tests import run
tests = ut.TestLoader().loadTestsFromTestCase(run(datareducer, DATA, ut))
ut.TextTestRunner(verbosity=2).run(tests)
