def run(m, ut):

  class tests(ut.TestCase):
    def test_1_traverse(self):
      self.assertEqual(m.apply([], lambda i: None), {})

    def test_2_traverse_data(self):
      self.assertEqual(m.apply([[1], [2], [3]], lambda i: i), {1: {'cnt': 1}, 2: {'cnt': 1}, 3: {'cnt': 1}})

    def test_3_traverse_data2(self):
      self.assertEqual(m.apply([[1], [1], [1], [2], [3]], lambda i: i), {1: {'cnt': 3}, 2: {'cnt': 1}, 3: {'cnt': 1}})

  return tests
