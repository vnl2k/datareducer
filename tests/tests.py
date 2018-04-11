import numpy as np

def run(m, data, ut):

	class tests(ut.TestCase):
		def test_1_setLimits(self):
			shader = m().setLimits(0,5,4).setLimits(0,5,4)

			self.assertEqual(shader.__min__, [0,0])
			self.assertEqual(shader.__max__, [5,5])
			self.assertEqual(shader.__bin_number__, [4,4])

		def test_2_setLimits_wrong_scale_type(self):
			shader = m().setLimits(0,5,5, scale_type='wrong')

		def test_3_apply_data(self):
			shader = m().setLimits(0,5,5).setLimits(0,5,5).initialize()
			shader.mapData(np.array([[1,1],[2,2],[3,3]]))

			# self.assertEqual(shader.__min__, [0,0])

	return tests