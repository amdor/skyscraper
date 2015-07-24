<#.
.SYNOPSIS
This script is for scraping webpages using the Internet Explorer for parsing html and navigating
on DOM objects.
.PARAMETER Data
Data of the cars
Explores the network
.NOTES
Author: Zsolt Deak, 2015.07.23
#>

Param
 (
    [Parameter(Mandatory=$true)]
    [hashtable]
    $Data
 ) 

 $highlight = "style=`"background-color:yellow`""

 $htmlContent = "<!DOCTYPE html>
<head>
    <style>
        table, th, td {
         border: 1px solid black;
        }
    </style>
</head>
<body>
    <table>
        <tr $highlight><td>Uri</td><td>$($Data['CarUri'])</td> "


#Finish up
$htmlContent+= "`n`t</table>`n</body>`n</html>"
$htmlContent
