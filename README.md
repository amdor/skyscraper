# Skyscraper

[![Build Status](https://travis-ci.org/amdor/skyscraper.svg?branch=master)](https://travis-ci.org/amdor/skyscraper)
## Overview
This skyscraper app is basically (yet) a Powershell/Python 3.6 project for automated comparison of [hasznaltauto.hu](http://hasznaltauto.hu) site's cars.
 It is widely configurable despite its simplicity. In case of the python version, it is capable of parsing any html page containing car information.
### Usage
#### PowerShell
See .ps1 file usages help (Get-Help), or the comment at the start of the files.
**PowerShell only supports v1.0 capabilities, thus scraping only HaHu and generating HTML results for example.**
#### Python
Same with Python files, all files have extensive documentation in comments
For the Python version's setup run
```
$ pip install -r requirements.txt
```

Regarded keys for comparator service's input data (if used without scraping, as a standalone library): <br/>
*age* <br/>
*condition* <br/>
*mass* <br/>
*power* <br/>
*price* <br/>
*currency* <br/>
*speedometer* <br/>
*trunk* <br/>

The Python REST service's API see the [docs](https://github.com/amdor/skyscraper/tree/master/docs).

Run the rest_service as main to use, or
```gunicorn skyscraper.rest_service:app```
if using Unix system.

### Tests
Run
```
$ nosetests
```
This runs tests under *tests* folder. For further details see setup.cfg.
