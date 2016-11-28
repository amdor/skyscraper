# Skyscraper

## Overview
This skyscraper app is basically (yet) a Powershell project for automated comparison of [hasznaltauto.hu](http://hasznaltauto.hu) site's cars. It is widely configurable though in its simplicity.

## Version 1.0
V1.0 is capable of comparing cars, saving their data, computing a value index (using my algorithm) and showing the results on a generated HTML page with a link refering to the original cars.
### Usage
See .ps1 file usages help (Get-Help), or the comment at the start of the files.

### Run
To enable unsigned script running, open the PowerShell shell and run the following

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
```
