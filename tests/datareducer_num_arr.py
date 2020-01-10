def run(m, data, ut):

  class tests(ut.TestCase):
    

    def test_1_test_lin_data(self):
      shader = m().setLimits(0, 10, 10, scale_type='lin').initialize()
      shader.apply([1])
      # shader.apply([2])
      # shader.apply([3])
      # shader.apply([4])
      # shader.apply(5)
      # shader.apply(6)

      print(shader.__data__)
      # self.assertEqual(shader.getAgg('cnt'), [1., 1, 4, 0, 0, 0, 0, 0, 0, 0])

  return tests