import os

from skyscraper.utils.constants import SPEEDOMETER_KEY

VALIDATION_DATA = {
	'bmw_530xd_automata-12119695.html': {
		SPEEDOMETER_KEY: '98 100 km'
	},
	'audi_a4_avant.html': {
		SPEEDOMETER_KEY: '56,488 km'
	}
}

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