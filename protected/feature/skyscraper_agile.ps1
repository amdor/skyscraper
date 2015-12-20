<#.
.SYNOPSIS
This script is for scraping webpages.
The output format is fixed yet. 
.PARAMETER Uri
The uri of the targeted webpage
.NOTES
Author: Zsolt Deak, 2015.07.21
#>

Param
 (
    [Parameter(Mandatory=$true)]
    [String]
    $Uri
 ) 

Add-Type -Path '.\..\src\Net45\HtmlAgilityPack.dll'

Write-Output 'Done, success'
Exit