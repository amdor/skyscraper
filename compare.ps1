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
   <script src=`"https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js`">
            `$(`"table`").width(`$(window).width());
   </script>
   <style>
        table {
            text-align: left;
            font-size: 12px;
            font-family: verdana;
            background: #c0c0c0;
        }

        table thead, #key, table thead a {
            text-align: center;
            vertical-align: middle;
            background: #c0c0c0;
            color: white;
        }

        table tbody tr {
            background: #f0f0f0;
        }

        td, thead {
            border: 1px solid white;
            word-wrap: break-word;
            min-width: 50px
        }

        #key {
            width: 50px;
        }
   </style>
</head>

<body>
    <table>"

#get ALL keys
#Also, making the table header.(first columnt is the other "header" axis for the property names
[System.Collections.ArrayList]$dataKeys = @()
$tableHeader = "`n        <thead>`n"
$tableHeader += "          <tr><td></td>`n"
For($i = 0; $i -lt $Data.Count; $i++){
    $carData = $Data[$i]
    ForEach($key in $carData.Keys){
        if(!$dataKeys.Contains($key)){
            [void]$dataKeys.Add($key)
        }
    }
    $carName = ($carData['CarUri'].split('/') | Select -Last 1).split('_') | Select -First 2
    $tableHeader += "         <td><a href=$($carData['CarUri'])>" + ([string]$carName[0]).ToUpper() + " $($($carName[1]).ToUpper())</td>"
    $Data[$i].Remove('CarUri')
}
$tableHeader += "        </tr>`n     </thead>`n"
$htmlContent += $tableHeader + "        <tbody>`n"

#Make rows and columns (row by row filling with every car's data)
ForEach($key in $dataKeys){
    $htmlContent += "          <tr>`n      <td id=`"key`">$key</td>`n"
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