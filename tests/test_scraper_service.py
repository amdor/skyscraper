import os
import unittest

from skyscraper.scraper_service import ScraperServiceFactory


def gather_extension_files(root):
	"""
	Traverses through all subdirectories of root collecting *.js filenames. Recursive.
	:param root: the basepoint of search
	:rtype: set
	:return: all found js filenames
	"""
	extension_files = set()
	for child in os.listdir(root):
		abs_path = os.path.join(root, child)
		if os.path.isdir(abs_path):
			extension_files |= gather_extension_files(abs_path)
		elif child.endswith(".html"):
			extension_files.add(abs_path)
	return extension_files


class TestBasicPaths(unittest.TestCase):
	html_files = set()

	@classmethod
	def setUpClass(cls):
		path = os.path.dirname(os.path.realpath(__file__))
		cls.html_files = gather_extension_files(path)

	def test_scraping(self):
		html_dict: dict = {}
		for file_name in self.html_files:
			with open(file_name, 'rb') as html_file:
				file_content = html_file.read()
				html_dict[file_name] = file_content
		scraper = ScraperServiceFactory.get_for_dict(html_dict)
		car_data = scraper.get_car_data()
		print('done')
