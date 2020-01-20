from array import array

def run(m, ut):

  class tests(ut.TestCase):
    def test_array_1_initialize_1D(self):
      container = m.container([4])
      container.set([3], 2)
      self.assertEqual(container.__buffer__.tolist(), [0.0, 0.0, 0.0, 2.0])
      self.assertEqual(container.get([3]), 2.0)
      self.assertEqual(container[3], 2.0)

    def test_array_2_initialize_2D(self):
      container = m.container([2, 2])
      container.set([1, 1], 2)
      self.assertEqual(container.__buffer__.tolist(), [0.0, 0.0, 0.0, 2.0])
      self.assertEqual(container.get([1, 1]), 2.0)
      self.assertEqual(container[1, 1], 2.0)

    def test_array_3_initialize_3D(self):
      container = m.container([2, 2, 2])
      container.set([1, 1, 1], 1)
      container.set([0, 0, 0], 2)
      container.set([0, 0, 1], 3)
      self.assertEqual(container.__buffer__.tolist(), [2.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0])

      self.assertEqual(container.get([1, 1, 1]), 1.0)
      self.assertEqual(container[1, 1, 1], 1.0)
      self.assertEqual(container.get([0, 0, 0]), 2.0)
      self.assertEqual(container.get([0, 0, 1]), 3.0)

    def test_array_4_toIterable(self):
      container = m.container([4])
      container.set([3], 2)
      for i in container.toIterable()():
        pass
      self.assertEqual(i, 2.0)

    def test_array_5_initialize_larger_container(self):
      container = m.container([500, 500])
      container.set([3, 3, 3], 2)

    def test_array_6_toMatrix(self):
      container = m.container([2, 2, 2])
      container.set([1, 1, 1], 1)
      container.set([0, 0, 0], 2)
      container.set([0, 0, 1], 3)
      matrix = container.toMatrix()
      
      self.assertEqual(matrix, [[[2.0, 3.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 1.0]]])

      self.assertEqual(matrix[1][1][1], 1)
      self.assertEqual(matrix[0][0][0], 2)
      self.assertEqual(matrix[0][0][1], 3)


  try:
    import immutables

    class testsSparseContainer(ut.TestCase):
      def test_sparse_1_initialize_1D(self):
        container = m.sparseContainer([4])
        container.set([3], 2)
        self.assertEqual(container.get([3]), 2.0)
        self.assertEqual(container[3], 2.0)

      def test_sparse_2_initialize_2D(self):
        container = m.sparseContainer([2, 2])
        container.set([1, 1], 2)
        self.assertEqual(container.get([1, 1]), 2.0)
        self.assertEqual(container[1, 1], 2.0)

      def test_sparse_3_initialize_3D(self):
        container = m.sparseContainer([2, 2, 2])
        container.set([1, 1, 1], 1)
        container.set([0, 0, 0], 2)
        container.set([0, 0, 1], 3)

        self.assertEqual(container.get([1, 1, 1]), 1.0)
        self.assertEqual(container[1, 1, 1], 1.0)
        self.assertEqual(container.get([0, 0, 0]), 2.0)
        self.assertEqual(container.get([0, 0, 1]), 3.0)
  except ImportError:
    class testsSparseContainer(ut.TestCase):
      pass

  return tests, testsSparseContainer
