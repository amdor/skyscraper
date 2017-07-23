# Skyscraper

##Overview
This skyscraper app is basically (yet) a Powershell/Python 2.7 project for automated comparison of [hasznaltauto.hu](http://hasznaltauto.hu) site's cars. It is widely configurable despite its simplicity.
##Version 1.0
V1.0 is capable of comparing cars, saving their data, computing a value index (using my algorithm) and showing the results on a generated HTML page with a link referring to the original cars.
###Usage
See .ps1 file usages help (Get-Help), or the comment at the start of the files.
Same with Python files, all files have extensive documentation in comments
For the Python version's setup run
'''
$ pip install -r requirements.txt
'''
###Tests
Run
'''
$ nosetests tests
'''