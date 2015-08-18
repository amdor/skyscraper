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
    $IsPath,
    [switch]
    $UseSaved
 ) 

 #This function walks through all urls, downloads its data, saves it into xmls and returns 
 #the sum of the data downloaded.
Function ScrapeWebPages{
     Param
     (
        [String]
        $InnerUri = $Uri,
        [switch]
        $InnerIsPath = $IsPath
     ) 

     #The folder for the xmls, if doesn't exist, we create it
     $outFolder = '.\output\data\'

     If(!(Test-Path $outFolder))
     {
        New-Item $outFolder -ItemType directory > $null
     }

     #Test if Uri points at a valid file
     $uris = @()
     If($InnerIsPath){
        If(!(Test-Path $InnerUri -PathType Leaf)){
            Throw "File not found at $InnerUri"
        }
        $uris = Get-Content $InnerUri
     }
     Else{
        $uris += $InnerUri 
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
        Write-Host "$url"
        $ie.Navigate($url)
        $i = 0
        while ($ie.busy) {
	        Start-Sleep -Milliseconds 600
            Write-Host "Navigating to URI $i"
            $i++
            if($i -ge 32)
            {
                Write-Error "Navigation timed out"
                Continue
            }
        }
            Write-Host "Navigating to URI is done"
        $doc=$ie.Document
        #Parse data
        Write-Host "Parsing data..."
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
        Write-Host "Saving data to .\output\data\$xmlName.xml"
        Export-Clixml -Path ".\output\data\$xmlName.xml" -InputObject $dataTable[$carIndex]

        $carIndex++
    }
    #return data
    $dataTable
    #ie is no more needed
    get-process iexplore | stop-process

    Return
}

#This function loads the car datas (previously saved) and gives it back as
Function GetData-FromFiles{

      Param
     (
        [String]
        $Path = ".\output\data\"
     )

     If( !(Test-Path $Path -PathType Container) ){
        Write-Error 'The given path is not correct, not pointing at a folder, or the folder does not exist'
        Return
     }

     $outputData = @()

     Get-ChildItem $Path | ForEach{
        Write-Host "Reading $_"
        $currentCarData = Import-Clixml -Path "$Path$_"
        $outputData += $currentCarData        
     }

     $outputData
     Return
}



#Main
$data
If($UseSaved){
    $data = GetData-FromFiles
} Else{
    $data = ScrapeWebPages -InnerUri $Uri -InnerIsPath $Path
}

Write-Host "Creating output html"
& .\compare.ps1 -Data $data

Write-Host 'Done'
Exit