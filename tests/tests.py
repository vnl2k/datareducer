def run(m, data, ut):

  class tests(ut.TestCase):
    def test_1_setLimits(self):
      shader = m().setLimits(0,5,5).setLimits(0,5,5)

      self.assertEqual(shader.__min__, [0,0])
      self.assertEqual(shader.__max__, [5,5])
      self.assertEqual(shader.__bin_number__, [5,5])
      self.assertEqual(shader.__bin_width__, [1,1])
      self.assertEqual(shader.binType, ['lin', 'lin'])

    def test_2_setLimits_wrong_scale(self):
      shader = m().setLimits(0,5,5, scale_type='wrong') # scale_type is wrong
      shader = m().setLimits(0,5,5, scale_type='log10') # log scale cannot start at 0

    def test_3_apply_linear_data(self):
      shader = m().setLimits(0,4,4).setLimits(0,4,4).initialize()
      shader.applyOnBatches([[0,0],[1,1],[2,2],[3,3]])

      self.assertEqual(shader.getAgg('cnt'), [[1, 0, 0, 0],
       [0, 1, 0, 0],
       [0, 0, 1, 0],
       [0, 0, 0, 1]])

    def test_4_data_min_max(self):
      shader = m().setLimits(0,4,4).setLimits(0,4,4).initialize()
      shader.applyOnBatches([[0,0],[1,1],[2,2],[3,3]])

      self.assertEqual(shader.getAgg('min'), [[0, 0, 0, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]])
      
      self.assertEqual(shader.getAgg('max'), [[0, 0, 0, 0],
       [0, 1, 0, 0],
       [0, 0, 2, 0],
       [0, 0, 0, 3]])   

    def test_5_data_sum_sum2(self):
      shader = m().setLimits(0,4,4).setLimits(0,4,4).initialize()
      shader.applyOnBatches([[0,0],[1,1],[2,2],[2,2]])

      self.assertEqual(shader.getAgg('sum'), [[0, 0, 0, 0],
       [0, 1, 0, 0],
       [0, 0, 4, 0],
       [0, 0, 0, 0]])
      
      self.assertEqual(shader.getAgg('sum2'), [[0, 0, 0, 0],
       [0, 1, 0, 0],
       [0, 0, 8, 0],
       [0, 0, 0, 0]])   

    def test_6_apply_linlog_data(self):
      shader = m().setLimits(0, 4, 4).setLimits(1, 10000, 4, scale_type='log10').initialize()
      shader.applyOnBatches([[0, 1], [1, 10], [2, 100], [3, 1000]])


      self.assertEqual(shader.getAgg('cnt'), [[1, 0, 0, 0],
       [0, 1, 0, 0],
       [0, 0, 1, 0],
       [0, 0, 0, 1]])

      shader = m().setLimits(0,4,4).setLimits(1,1000,3, scale_type='log10').initialize()
      shader.applyOnBatches([[0,2],[1,20],[2,200],[3,1000]])
      self.assertEqual(shader.getAgg('cnt'), [[1, 0, 0],
       [0, 1, 0],
       [0, 0, 1],
       [0, 0, 1]])

    def test_7_get_dimension(self):
      shader = m().setLimits(0,4,4).setLimits(1,10000,4, scale_type='log10')

      self.assertEqual(shader.getDimension(0), [0.0, 1.0, 2.0, 3.0])
      self.assertEqual(shader.getDimension(1), [1.0, 10.0, 100.0, 1000.0])

    def test_8_test_log_data(self):
      shader = m().setLimits(1e-10, 1, 10, scale_type='log10').initialize()
      shader.apply([1e-10])
      shader.apply([1e-9])
      shader.apply([1e-8])
      shader.apply([3e-8])
      shader.apply(9.9e-8)
      shader.apply(9.9999e-8)
      # shader.apply([1e-10, 1e-9, 1e-8, 3e-8, 9.9e-8, 9.9999e-8])

      self.assertEqual(shader.getAgg('cnt'), [1., 1, 4, 0, 0, 0, 0, 0, 0, 0])

  return tests