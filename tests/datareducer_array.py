def run(m, data, ut):

  class tests(ut.TestCase):

    def test_1_test_lin_data(self):
      shader = m().setLimits(0, 10, 10, scale_type='lin').init()
      lmbd = lambda prev, _: prev + 1
      shader.apply(1, lmbd)
      shader.apply(2, lmbd)
      shader.apply(3, lmbd)
      shader.apply(4, lmbd)
      shader.apply(5, lmbd)
      shader.apply(6, lmbd)

      self.assertEqual(shader.getAgg(),\
        [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0])

    def test_2_apply_linear_data(self):
      shader = m().setLimits(0, 4, 4).setLimits(0, 4, 4).init()
      lmbd = lambda prev, _: prev + 1
      shader.apply([0, 0], lmbd)
      shader.apply([1, 1], lmbd)
      shader.apply([2, 2], lmbd)
      shader.apply([3, 3], lmbd)

      self.assertEqual(shader.getAgg(), [[1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])

    def test_3_applyOnBatch_1D_data(self):
      shader = m().setLimits(0, 4, 4).init()
      lmbd = lambda prev, _: prev + 1
      
      shader.applyOnBatch([0, 1, 2, 3, 4], lmbd)
      self.assertEqual(shader.getAgg(), [1., 1., 1., 1.])
      
      shader.applyOnBatch([0, 1, 2, 3, 4], lmbd)
      self.assertEqual(shader.getAgg(), [2., 2., 2., 2.])

    def test_4_applyOnBatch_2D_data(self):
      shader = m().setLimits(0, 4, 4).setLimits(0, 4, 4).init()
      lmbd = lambda prev, _: prev + 1

      shader.applyOnBatch([[0, 0], [1, 1], [2, 2], [3, 3]], lmbd)

      self.assertEqual(shader.getAgg(), [[1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])
  return tests
