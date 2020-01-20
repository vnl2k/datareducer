def run(m, data, ut):

  class tests(ut.TestCase):

    def test_1_test_lin_data(self):
      shader = m().setLimits(0, 10, 10, scale_type='lin').initialize()
      shader.apply([1])
      shader.apply([2])
      shader.apply([3])
      shader.apply([4])
      shader.apply(5)
      shader.apply(6)

      self.assertEqual(shader.getAgg(),\
        [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0])

    def test_2_apply_linear_data(self):
      shader = m().setLimits(0, 4, 4).setLimits(0, 4, 4).init()
      shader.apply([0, 0])
      shader.apply([1, 1])
      shader.apply([2, 2])
      shader.apply([3, 3])

      self.assertEqual(shader.getAgg(), [[1, 0, 0, 0],
       [0, 1, 0, 0],
       [0, 0, 1, 0],
       [0, 0, 0, 1]])
  return tests
