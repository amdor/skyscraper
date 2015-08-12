<#.
.SYNOPSIS
This script is for scraping webpages using the Internet Explorer for parsing html and navigating
on DOM objects.
.PARAMETER Uri
The uri of the targeted webpage
Explores the network
.NOTES
Author: Zsolt Deak, 2015.07.09
#>

Param
 (
    [Parameter(Mandatory=$true)]
    [String[]]
    $Uri
 ) 

 #the folder for the xmls, if doesn't exist, we create it
 $outFolder = '.\output\data\'

 If(!(Test-Path $outFolder))
 {
    New-Item $outFolder -ItemType directory > $null
 }


$ie=New-Object -ComObject InternetExplorer.Application
Write-Output "$Uri"
$ie.Navigate($Uri)
$i = 0
while ($ie.busy) {
	Start-Sleep -Milliseconds 600
    Write-Output "Navigating to URI $i"
    $i++
    if($i -ge 32)
    {
        Throw "Local request timed out, explorer is busy, or file not exists"
    }
}
    Write-Output "Navigating to URI is done"
$doc=$ie.Document
$elements = $doc.GetElementsByTagName("TABLE") | where {$_.className -eq "hirdetesadatok"}

#Save data
[System.Collections.ArrayList]$dataTable = @()
$dataTable += @{}
$elements.innerText.split(“`r`n”) | ForEach-Object{
    # process line
    if($_ -like "*:*")
    {
        $tmp = $_ -Split ":"
        $dataTable[0].Add($tmp[0], $tmp[1])
    }
}
$dataTable[0].Add('CarUri', $Uri)

$xmlName = $Uri -Split '/' | Select -Last 1
#Saving the data obtained from the html page, comparing it with the already saved data
Export-Clixml -Path ".\output\data\$xmlName.xml" -InputObject $dataTable
Write-Output "Creating output html"
& .\compare.ps1 -Data $dataTable
#ie is no more needed
get-process iexplore | stop-process

Write-Output 'Done'

Exit