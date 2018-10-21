import unittest as ut
from datareducer import shader
from datareducer import tree

DATA = []

from tests.tests import run
tests = ut.TestLoader().loadTestsFromTestCase(run(shader, DATA, ut))
ut.TextTestRunner(verbosity=2).run(tests)


from tests.tree_reducer import run as run_tree
tests = ut.TestLoader().loadTestsFromTestCase(run_tree(tree, ut))
ut.TextTestRunner(verbosity=2).run(tests)