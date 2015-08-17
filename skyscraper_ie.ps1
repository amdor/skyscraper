<#.
.SYNOPSIS
This script is for scraping hasznaltauto.hu using the Internet Explorer for parsing html and navigating
on DOM objects.

If using with a source file containing the urls to scrape, each url has to be in a new line, the Uri parameter
must be the file's path and IsPath parameter must be set.
Otherwise just give in the url of the car and the script collects its data.
.PARAMETER Uri
The uri of the targeted webpage or the path to the text file containing the URIs of the webpages
we seek to scrape.
.PARAMETER IsPath
Determines if the Uri is path, if present, it means Uri is a path to a file.
Explores the network
.NOTES
Author: Zsolt Deak, 2015.07.09
#>

Param
 (
    [Parameter(Mandatory=$true)]
    [String]
    $Uri,
    [switch]
    $IsPath
 ) 

 #the folder for the xmls, if doesn't exist, we create it
 $outFolder = '.\output\data\'

 If(!(Test-Path $outFolder))
 {
    New-Item $outFolder -ItemType directory > $null
 }

 #Test if Uri points at a valid file
 $uris = @()
 If($IsPath){
    If(!(Test-Path $Uri -PathType Leaf)){
        Throw "File not found at $Uri"
    }
    $uris = Get-Content $Uri
 }
 Else{
    $uris += $Uri 
 }

#For saving data, we make an array of hashtables. Each hashtable contains a car's data
$dataTable = @()

$carIndex = 0
ForEach($url in $uris){
    #Protection against wrong websites
    If(!( ($url -Split '/' | Select -Index 2) -like 'www.hasznaltauto.hu')){
        Write-Error "$url is not pointing at www.hasznaltauto.hu, skipping"
        Continue
    }
    $ie=New-Object -ComObject InternetExplorer.Application
    Write-Output "$url"
    $ie.Navigate($url)
    $i = 0
    while ($ie.busy) {
	    Start-Sleep -Milliseconds 600
        Write-Output "Navigating to URI $i"
        $i++
        if($i -ge 32)
        {
            Write-Error "Navigation timed out"
            Continue
        }
    }
        Write-Output "Navigating to URI is done"
    $doc=$ie.Document
    #Parse data
    Write-Output "Parsing data..."
    $dataTable += @{}
    $elements = $doc.GetElementsByTagName("TABLE") | where {$_.className -eq "hirdetesadatok"}

    $elements.innerText.split(“`r`n”) | ForEach-Object{
        # process line
        if($_ -like "*:*")
        {
            $tmp = $_ -Split ":"
            $dataTable[$carIndex].Add($tmp[0], $tmp[1])
        }
    }
    $dataTable[$carIndex].Add('CarUri', $url)

    $xmlName = $url -Split '/' | Select -Last 1
    #Saving the data obtained from the html page, comparing it with the already saved data
    Write-Output "Saving data to .\output\data\$xmlName.xml"
    Export-Clixml -Path ".\output\data\$xmlName.xml" -InputObject $dataTable

    $carIndex++
}
Write-Output "Creating output html"
& .\compare.ps1 -Data $dataTable
#ie is no more needed
get-process iexplore | stop-process

Write-Output 'Done'

Exit