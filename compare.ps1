<#.
.SYNOPSIS
This script compares the properties of the cars and generates an html file presenting the properties and
the real worth of the cars as well.
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

<#
This function enumerates through parameters of every cars' primary parameters
and generates their worth from them.
Orders the values descendingly, returns the ordered array, in which each element has a Name and Value property
#>
Function Get-ValueOfCars{
    
  #Value marker
  #carWorthTable is to hold the sum value(worth) numbers of the car, one number for each 
  #and keys are the CarUri-s for these values
  $carWorthTable = @{}

  ForEach($carData in $Data){
    Write-Host "Getting value of $($carData['CarUri'])"
    #Gets numeric value
    [regex]$wantedExpression = "^\d+"
    $localWorthsTable = @{}

    #Power in kW
    [Int32]$power = 14
    If(($carData['Teljesítmény'] -replace " ","") -match $wantedExpression){
        $power = $Matches[0]
    }
    $localWorthsTable.Add('Power', $power/14)

    #Condition
    Switch -regex ($carData['Állapot']){
        'Normál|Kitûnõ|Sérülésmentes|Megkímélt|Újszerû' { $localWorthsTable.Add('Condition', 0); break }
        Default { $localWorthsTable.Add('Condition', -20); break }
    }

    #Trunk space
     If(($carData['Csomagtartó'] -replace " ","") -match $wantedExpression){
        $localWorthsTable.Add('Trunk', $Matches[0]/150)
    } Else{
        $localWorthsTable.Add('Trunk', 0)
    }

    #Own mass, -3 is the penalty if sy leaves this field (1500 kg, average car weight)
     If(($carData['Saját tömeg'] -replace " ","") -match $wantedExpression){
        $localWorthsTable.Add('Mass', -$Matches[0]/500)
    } Else{
        $localWorthsTable.Add('Mass', -3)
    }

    #Speedometer: first 100 000 is 0-10 proportianately, the part from 100 000 to 200 000 is plus 1-5 penalty point similarily
    #from 200 000 it's 2.5 penalty for every 100 000 (proportianately) 
     If(($carData['Kilométeróra állása'] -replace " ","") -match $wantedExpression){
        $speedo = $Matches[0]/10000
        If($speedo -gt 10 -and $speedo -le 20){
            $speedo = 10 + (($speedo - 10) / 2)
        } ElseIf($speedo -gt 20){
            $speedo = 15 + (($speedo - 20) / 4)
        }
        $localWorthsTable.Add('Speedometer', -$speedo)
    } Else{
        $localWorthsTable.Add('Speedometer', -12)
    }

    #Price is calculated from the price and the power if there is no problem (like no power or price data), NOTE: max cap
    $carPrice = 1
    If($power -gt 14){
        If($carData['Akciós ár']){
            $carPrice = $carData['Akciós ár'] -replace '\.',''
        } Else{
            $carPrice = $carData['Vételár'] -replace '\.',''
        }
        If($carPrice -match $wantedExpression){
            $carPrice = ($power * 500000) / $Matches[0]
            $carPrice = Measure-Object -Maximum @($carPrice, 10)
        } Else{
            $carPrice = 1
        }
    } Else{
        $carPrice = 1
    }
    $localWorthsTable.Add('Price', $carPrice)

    #Date involved components
    If($carData['Évjárat']){
        $dateOfProd = $carData['Évjárat']
        If(($dateOfProd -split "/").Count -lt 2){
            $dateOfProd = [datetime] ($dateOfProd + "/01")
        } Else{
            $dateOfProd = [datetime] $dateOfProd
        }
        $currentDate = Get-Date
        $yearsOld = $currentDate.Year - $dateOfProd.Year
        $monthsOld = $currentDate.Month - $dateOfProd.Month
        #The base poit of car worth loss was http://www.edmunds.com/car-buying/how-fast-does-my-new-car-lose-value-infographic.html
        $priceLossPercent = $monthsOld
        If(($yearsOld -le 0) -and ($monthsOld -le 0)){
            $priceLossPercent = 0
        } ElseIf($yearsOld -le 5){
            $priceLossPercent += 11 * ($yearsOld - 1) + 19
        } ElseIf($yearsOld -le 30){
            $priceLossPercent += [math]::Log10($yearsOld - 3) * 10 + 60
        } ElseIf($yearsOld -gt 30){
            $priceLossPercent += 192 * [math]::Pow([math]::E, (-0.03 * $yearsOld))
        }
        $localWorthsTable.Add('AgeLoss', -$priceLossPercent / 3)
    }

    #Add up the values to get a car's worth
    $key = $carData['CarUri']
    $carWorthTable.Add($key, 0)
    ForEach($valueKey in $localWorthsTable.Keys){
        $carWorthTable[$key] += $localWorthsTable[$valueKey]
    }
    $carWorthTable[$key] += 70#making it positive in MOST cases and giving it non null value in every case
  }#end of foreach Data

  $carWorthTable.GetEnumerator() | Sort -Property Value -Descending
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

#Get ALL keys(uniquely) and make the table head with car names and their links
#NOTE: valueArray is ordered and that is why everywhere this array is used for the iteration.
[System.Collections.ArrayList]$carParameterNames = @()
[Object[]]$valueArray = Get-ValueOfCars

#we need an indexer object for accessing by uri the cars in $Data (otherwise the array structure is well enough satisfactory, this is the only excpetion)
$carDataIndexerTable = @{}
For($i = 0; $i -lt $Data.Count; $i++){
    $car = $Data[$i]
    $carDataIndexerTable.Add($car['CarUri'], $i)
}

$tableHeader = "`n        <thead>`n"
$tableHeader += "          <tr><td></td>`n"
$i = 0;
For($i = 0; $i -lt $valueArray.Count; $i++){
     $carUri = $valueArray[$i].Name
     $carData = $Data[$carDataIndexerTable[$carUri]]
    ForEach($key in $carData.Keys){
        if(!$carParameterNames.Contains($key)){
            [void]$carParameterNames.Add($key)
        }
    }
    #Making the table header
    $carName = ($carData['CarUri'].split('/') | Select -Last 1).split('_') | Select -First 2
    $tableHeader += "         <td><a href=$($carData['CarUri'])>" + ([string]$carName[0]).ToUpper() + " $($([string]$carName[1]).ToUpper())</td>`n"
}
$tableHeader += "        </tr>`n     </thead>`n"


#Make rows and columns (column by column so car by car filling the rows) for table body
#First culomn is for the parameters others for the cars
#TABLE BODY
$carParameterNames.Remove('CarUri')
$htmlContent += $tableHeader + "        <tbody>`n"
ForEach($paramName in $carParameterNames){
    $htmlContent += "          <tr>`n"
    $htmlContent += "           <td id=`"key`">$paramName</td>`n"
    #for every car
    For($i = 0; $i -lt $valueArray.Count; $i++){
        $carUri = $valueArray[$i].Name
        $carData = $Data[$carDataIndexerTable[$carUri]]
        $htmlContent += "           <td>$($carData[$paramName])</td>`n"
    }
    $htmlContent += "          </tr>`n"
}
$htmlContent += "        </tbody>`n"

    

#Last row is calculated from the data
#First column is always the key for the row, it's identifier
$htmlContent += "          <tfoot><tr>`n"
$htmlContent += "           <td id=`"key`">Calculated value</td>`n"

For($i = 0; $i -lt $valueArray.Count; $i++){
    $htmlContent += "           <td>{0:N0}" -f $($valueArray[$i].Value) + "</td>"
}
$htmlContent += "          </tfoot></tr>`n"

#Finish up
$htmlContent+= "`t</table>`n</body>`n</html>"
$htmlContent | Out-File ".\output\compare.html"
Exit