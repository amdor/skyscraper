import unittest
import os

import re

import time
from bs4 import BeautifulSoup
from common_test_utils import gather_extension_files, VALIDATION_DATA


def parse_html(content, parser):
	car_soup = BeautifulSoup(content, parser)
	mileage = car_soup.find(text=re.compile('^((\d{1,3}[\.| |,]?){1,3})km|miles$'))
	print(mileage)


class TestParseSpeed(unittest.TestCase):
	files_under_test = set()
	file_contents = []

	@classmethod
	def setUpClass(cls):
		path = os.path.dirname(os.path.realpath(__file__))
		cls.files_under_test = gather_extension_files(path)
		for path in cls.files_under_test:
			with open(path, 'rb') as html_file:
				content = html_file.read()
				content = str(content, encoding='utf-8')
				content = content.replace('\xa0', ' ')
				cls.file_contents.append(content)

	def test_lxml_parsing(self):
		print('lxml parser')
		start_time = time.clock()
		for content in self.file_contents:
			parse_html(content, 'lxml')
		print(time.clock() - start_time, "seconds")

	def test_html_parser_parsing(self):
		print('html.parser')
		start_time = time.clock()
		for content in self.file_contents:
			parse_html(content, 'html.parser')
		print(time.clock() - start_time, "seconds")

	def test_html5lib_parsing(self):
		print('html5lib')
		start_time = time.clock()
		for content in self.file_contents:
			parse_html(content, 'html5lib')
		print(time.clock() - start_time, "seconds")
