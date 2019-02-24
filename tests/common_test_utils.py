import os

from skyscraper.utils.constants import SPEEDOMETER_KEY, AGE_KEY, PRICE_KEY, POWER_KEY, CURRENCY_KEY

VALIDATION_DATA = {
    'hahu1.html': {
        SPEEDOMETER_KEY: '98 100 km',
        AGE_KEY: '2014/1',
        PRICE_KEY: '8300000',
        POWER_KEY: '190 kW',
        CURRENCY_KEY: 'HUF'
    },
    'hahu2.html': {
        SPEEDOMETER_KEY: '178 000 km',
        AGE_KEY: '2012/7',
        PRICE_KEY: '9200000',
        POWER_KEY: '230 kW',
        CURRENCY_KEY: 'HUF'
    },
    'mobile1.html': {
        SPEEDOMETER_KEY: '56,488 km',
        AGE_KEY: '08/2013',
        PRICE_KEY: '20444',
        POWER_KEY: '165 kW',
        CURRENCY_KEY: 'EUR'
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
