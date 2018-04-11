def run(m, data, ut):

	class tests(ut.TestCase):
		def test_1_setLimits(self):
			shader = m().setLimits(0,5,5).setLimits(0,5,5)

			self.assertEqual(shader.__min__, [0,0])
			self.assertEqual(shader.__max__, [5,5])
			self.assertEqual(shader.__bin_number__, [5,5])
			self.assertEqual(shader.binW, [1,1])
			self.assertEqual(shader.binType, ['lin', 'lin'])

		def test_2_setLimits_wrong_scale_type(self):
			shader = m().setLimits(0,5,5, scale_type='wrong')

		def test_3_apply_linear_data(self):
			shader = m().setLimits(0,4,4).setLimits(0,4,4).initialize()
			shader.apply([[0,0],[1,1],[2,2],[3,3]])

			self.assertEqual(shader.getAgg('cnt'), [[1, 0, 0, 0],
			 [0, 1, 0, 0],
			 [0, 0, 1, 0],
			 [0, 0, 0, 1]])

		def test_4_data_min_max(self):
			shader = m().setLimits(0,4,4).setLimits(0,4,4).initialize()
			shader.apply([[0,0],[1,1],[2,2],[3,3]])

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
			shader.apply([[0,0],[1,1],[2,2],[2,2]])

			self.assertEqual(shader.getAgg('sum'), [[0, 0, 0, 0],
			 [0, 1, 0, 0],
			 [0, 0, 4, 0],
			 [0, 0, 0, 0]])
			
			self.assertEqual(shader.getAgg('sum2'), [[0, 0, 0, 0],
			 [0, 1, 0, 0],
			 [0, 0, 8, 0],
			 [0, 0, 0, 0]])		

		def test_6_apply_linlog_data(self):
			shader = m().setLimits(0,4,4).setLimits(1,10000,4, scale_type='log10').initialize()
			shader.apply([[0,1],[1,10],[2,100],[3,1000]])

			self.assertEqual(shader.getAgg('cnt'), [[1, 0, 0, 0],
			 [0, 1, 0, 0],
			 [0, 0, 1, 0],
			 [0, 0, 0, 1]])

			shader = m().setLimits(0,4,4).setLimits(1,1000,3, scale_type='log10').initialize()
			shader.apply([[0,2],[1,20],[2,200],[3,1000]])
			self.assertEqual(shader.getAgg('cnt'), [[1, 0, 0],
			 [0, 1, 0],
			 [0, 0, 1],
			 [0, 0, 1]])


	return tests