import unittest as ut
from datareducer import shader, shaderArray
from datareducer import tree
from datareducer import DataContainer

DATA = []

from tests.datareducer import run
tests = ut.TestLoader().loadTestsFromTestCase(run(shader, DATA, ut))
ut.TextTestRunner(verbosity=2).run(tests)

from tests.data_container import run
container, sparseContainer = run(DataContainer, ut)

tests = ut.TestLoader().loadTestsFromTestCase(container)
ut.TextTestRunner(verbosity=2).run(tests)

tests = ut.TestLoader().loadTestsFromTestCase(sparseContainer)
ut.TextTestRunner(verbosity=2).run(tests)

from tests.datareducer_array import run
tests = ut.TestLoader().loadTestsFromTestCase(run(shaderArray, [], ut))
ut.TextTestRunner(verbosity=2).run(tests)


from tests.tree_reducer import run as run_tree
tests = ut.TestLoader().loadTestsFromTestCase(run_tree(tree, ut))
ut.TextTestRunner(verbosity=2).run(tests)
