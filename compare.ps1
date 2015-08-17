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
    [hashtable[]]
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
    <table>"

#get ALL keys
[System.Collections.ArrayList]$DataKeys = @()
ForEach($carData in $Data){
    ForEach($key in $carData.Keys){
        if(!$DataKeys.Contains($key)){
            [void]$DataKeys.Add($key)
        }
    }
}

#Make rows and columns (row by row filling with every car's data)
ForEach($key in $DataKeys){
    $htmlContent += "`n        <tr>`n"
    $htmlContent += "          <td>$key</td>`n"
    #First we save data in an array for the comparing
    $rowDataColumns = @()
    ForEach($carData in $Data){
        $rowDataColumns += "          <td >$($carData[$key])</td>`n"
    }
    #Second, we add the prepared (formatted) lines to the html content
    ForEach($column in $rowDataColumns){
        $htmlContent += $column
    }
    
    $htmlContent += "`n        </tr>`n"
}


#Finish up
$htmlContent+= "`t</table>`n</body>`n</html>"
$htmlContent | Out-File ".\output\compare.html"