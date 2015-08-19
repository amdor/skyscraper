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


Function Get-ValueOfCars{
    
  #Value marker
  #carWorthTable is to hold the sum value numbers of the car, keys are the CarUri-s
  $carWorthTable = @{}

  ForEach($carData in $Data){
    
  }

  $carWorthTable
  Return

}

<#
    /\    /\        /\    ||    /\   //
   //\\  //\\      //\\   ||   //|| //
  //  \\//  \\    //  \\  ||  // ||// 
 //    \/    \\  //____\\ || //  |//  
//            \\//      \\||//   |/   
#>

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

#Get ALL keys(uniquely)
#WARNING: we massively rely on the fact that ForEach enumerates arrays sequentially!!!! This is for the sake of clean code
[System.Collections.ArrayList]$dataKeys = @()
$tableHeader = "`n        <thead>`n"
$tableHeader += "          <tr><td></td>`n"
ForEach($carData in $Data){
    ForEach($key in $carData.Keys){
        if(!$dataKeys.Contains($key)){
            [void]$dataKeys.Add($key)
        }
    }
    #Making the table header
    $carName = ($carData['CarUri'].split('/') | Select -Last 1).split('_') | Select -First 2
    $tableHeader += "         <td><a href=$($carData['CarUri'])>" + ([string]$carName[0]).ToUpper() + " $($($carName[1]).ToUpper())</td>"
}
$tableHeader += "        </tr>`n     </thead>`n"

$htmlContent += $tableHeader + "        <tbody>`n"

#Make rows and columns (row by row filling with every car's data)
$dataKeys.Remove('CarUri')
ForEach($key in $dataKeys){

    $htmlContent += "          <tr>`n"
    $htmlContent += "           <td id=`"key`">$key</td>`n"
    #First we save data in an array for the comparing
    $rowDataColumns = @()
    ForEach($carData in $Data){
        $rowDataColumns += "           <td >$($carData[$key])</td>`n"
    }
    #Second, we add the prepared (formatted) lines to the html content
    ForEach($column in $rowDataColumns){
        $htmlContent += $column
    }
    
    $htmlContent += "          </tr>`n"
}

#Last row is calculated from the data
#First column is always the key for the row, it's identifier
$htmlContent += "          <tfoot><tr>`n"
$htmlContent += "           <td id=`"key`">Calculated value</td>`n"
$valueTable = Get-ValueOfCars
ForEach($carData in $Data){
    $htmlContent += "           <td>$($value)</td>"
}
$htmlContent += "          </tfoot></tr>`n"

#Finish up
$htmlContent+= "`t</table>`n</body>`n</html>"
$htmlContent | Out-File ".\output\compare.html"
Exit