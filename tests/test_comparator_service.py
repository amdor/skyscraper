import unittest
from services.comparator_service import compare_cars, WORTH_KEY


class TestHappyPaths(unittest.TestCase):
	defaultInput = [
		{
			'CarUri': 'http://hasznaltauto.hu/auto'
		}
	]

	def setUp(self):
		return

	def test_null_worth(self):
		compare_cars(self.defaultInput)
		self.assertEqual(self.defaultInput[0][WORTH_KEY], 0)
