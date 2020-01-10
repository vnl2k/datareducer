from array import array

def run(m, ut):

  class tests(ut.TestCase):
    def test_1_initialize(self):
      container = m.container([4])
      container.set([3], 2)
      self.assertEqual(container.__buffer__.tolist(), [ 0.0,  0.0, 0.0, 2.0])

      container = m.container([2, 2])
      container.set([1, 1], 2)
      self.assertEqual(container.__buffer__.tolist(), [ 0.0, 0.0, 0.0, 2.0])

      container = m.container([2, 2, 2])
      container.set([1, 1, 1], 2)
      self.assertEqual(container.__buffer__.tolist(), [ 0.0,  0.0, 0.0,  0.0, 0.0, 0.0, 0.0, 2.0])

    def test_2_initialize_large_container(self):
      container = m.container([5000, 5000])
      container.set([3, 3, 3], 2)
      

  return tests