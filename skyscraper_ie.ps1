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
    [String]
    $Uri
 ) 

 $htmlPath = '.\src\html.html'

 if(!(Test-Path $htmlPath -PathType Leaf))
 {
    Throw "$htmlPath file is required, but not exists."
 }

$ie=New-Object -ComObject InternetExplorer.Application
$pathofhtml = Resolve-Path $htmlPath
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
$dataTable = @{}
$elements.innerText.split(“`r`n”) | ForEach-Object{
    # process line
    if($_ -like "*:*")
    {
        $tmp = $_ -Split ":"
        $dataTable.Add($tmp[0], $tmp[1])
    }
}
$dataTable.Add('CarUri', $Uri)

Out-File -InputObject $dataTable -FilePath '.\src\data.txt'

get-process iexplore | stop-process

Write-Output 'Done'

Exit