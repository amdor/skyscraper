<#.
.SYNOPSIS
This script is for scraping hasznaltauto.hu using the Internet Explorer for parsing html and navigating
on DOM objects.

The script funcionates in 3 modes:
-If Uri parameter is set, then scrapes one car's page, saves its data and creates an html from it into the .\output folder

-If the Path parameter is set, does tha same as if Uri is set but with all the urls given in the file marked by the path.
NOTE: The file has to be simple text file and every url must be in a separate line

-If UseSaved parameter is set, it means the script uses all previously saved car data and generates the output html from them.
NOTE: All data is saved under .\output\data
.PARAMETER Uri
The uri of the targeted webpage we seek to scrape. Might be array.
.PARAMETER Path
Path to a file containing url's of cars at hasznaltauto.hu
Explores the network
.PARAMETER UseSaved
Offline mode's switch, neither other parameters are allowed nor processed
.NOTES
Author: Zsolt Deak, 2015.07.09
#>


Param
 (
    [Parameter(Mandatory=$true, ParameterSetName = "Online")]
    [String[]]
    $Uri,
    [Parameter(Mandatory=$true, ParameterSetName = "MultiOnline")]
    [string]
    $Path,
    [Parameter(ParameterSetName = "Offline")]
    [switch]
    $UseSaved
 ) 

$Script:TESTMODE = $true #testmode alters behavior, doesn't use cached data for instance, or saves car pages

#The folder for the xmls, if doesn't exist, we create it
$Script:outFolder = '.\output\data\'

#The folder for the car pages if TESTMODE is enabled
$Script:outPageFolder = '.\output\pages\'


<#Navigating to the given url with IE object or with
the newer PS method Invoke-Webrequest
#>
Function Navigate{

    Param
    (
        [Parameter(Mandatory=$true)]
        [String]
        $Url,
        [switch]
        $IsCompatibilityMode = $false
    )

     If($compatibilityMode){
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
        } Else{
            #$doc = & .\feature\skyscraper.ps1 -Uri $url
            #GET request to the given uri, the results are saved to dest and returned to the pipeline as well
            $doc = Try { Invoke-WebRequest -Uri $url -Method Get <#-OutFile $Dest -PassThru -UseBasicParsing#> } Catch { $_.Exception.Response }
            #Response is OK, and yet to be html
            if(($doc.StatusCode -ne 200) -or !($doc.Headers['Content-Type'] -like '*text/html*') )#$IndexPage.Headers -contains 'text/html') )
            {
                Write-Host "Wrong response: $($doc.StatusCode), url $url"
                Start-Sleep -Milliseconds 1000
                Continue
            }

            Write-Host 'Done downloading page data'
        }
        $doc
}

 <#This function walks through all urls, downloads their data, saves them into xmls and returns 
 the sum of the data downloaded.
 This does the main functionalities.
 In compatibility mode uses IE to navigate to the webpage, else uses PS Invoke-WebRequest
 #>
Function ScrapeWebPages{
     Param
     (
        [String[]]
        $InnerUri,
        [String]
        $InnerPath,
        [switch]
        $compatibilityMode
     ) 

     If($Path -and !$InnerPath){
        $InnerPath = $Path
     } ElseIf($Uri -and !$InnerUri){
        $InnerUri = $Uri
     }

     If(!(Test-Path $outFolder))
     {
        New-Item $outFolder -ItemType directory > $null
     }

     #Test if Uri points at a valid file
     $uris = @()
     If($InnerPath){
        If(!(Test-Path $InnerPath -PathType Leaf)){
            Throw "File not found at $InnerPath"
        }
        $uris = Get-Content $InnerPath
     }
     Else{
        If($InnerUri.GetType() -eq $uris.GetType()){
            $uris = $InnerUri
        } Else {            
            $uris += $InnerUri 
        }
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
        #Searching for matching saved car data A.K.A. caching, if not in testmode, there is cached data
        #and the cached data was cached today
        $xmlName = $url -Split '/' | Select -Last 1
        $xmlPath = "$outFolder$xmlName.xml"
        If(!$TESTMODE -and (Test-Path $xmlPath)){
            If((Get-Item -Path $xmlPath).CreationTime.Date -eq (Get-Date).Date)
            {
                Write-Host "Reading $xmlName"
                $currentCarData = Import-Clixml -Path $xmlPath
                $dataTable += @{}
                $dataTable[$carIndex] = $currentCarData
                $carIndex++
                Continue
            }
        }
        #Else
        Write-Host "Navigating to "$url
        #Distinguish between compatibility mode and normal
        If($compatibilityMode){ $doc = Navigate -Url $url -IsCompatibilityMode }
        Else{ $doc = Navigate -Url $url } 
        
        #in test mode, the pages are saved
        If( $TESTMODE ) {
            $htmlName = $xmlName
            Out-File -FilePath "$Script:outPageFolder$htmlName.html" -InputObject $doc.Content
            Write-Host "HTML content is saved to $outPageFolder$htmlName.html"
        }       
        
        #Parse data
        Write-Host "Parsing data..."
        Try{
            $elements = $null
            If( $compatibilityMode ) {
                $elements = $doc.GetElementsByTagName("TABLE") | Where-Object {$_.outerHTML -like '*class="hirdetesadatok"*'}
            } Else {
                $elements = $doc.ParsedHtml.GetElementsByTagName("TABLE") | Where-Object className -eq "hirdetesadatok"
            }
        } Catch{
            Write-Error "Parsing failed badly"
            Continue
        }
        If($elements -eq $null -or $elements.innerText -eq ''){
            Write-Host "Parsing succeeded but not valueable data found"
            Continue
        }
        $dataTable += @{}
        $elementText = ""
        If( $compatibilityMode ) {
            $elementText = $elements.outerText
        } Else {
            $elementText = $elements.innerText
        }
        $elementText.split(“`r`n”) | ForEach-Object{
            # process line
            if($_ -like "*:*")
            {
                $tmp = $_ -Split ":"
                For( $index = 0; $index -lt 2; $index++ ) {
                    $tmp[$index] = $tmp[$index].Trim()#remove leading and trailing spaces
                }
                $dataTable[$carIndex].Add($tmp[0], $tmp[1])
            }
        }
        $dataTable[$carIndex].Add('CarUri', $url)

        #Saving the data obtained from the html page, comparing it with the already saved data
        Write-Host "Saving data to $xmlPath"
        Export-Clixml -Path $xmlPath -InputObject $dataTable[$carIndex]

        $carIndex++
    }
    #return data
    $dataTable
    If($compatibilityMode){
        #ie is no more needed
        get-process iexplore | stop-process
    }

    Return
}

<#This function loads the car datas (previously saved) and gives it back as
.PARAMETER Path
The path to the folder where the xml files are, containing car data.
Defaults to .\output\data\
#>
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
        Write-Host "Reading in $_"
        $currentCarData = Import-Clixml -Path "$Path$_"
        $outputData += $currentCarData        
     }

     $outputData
     Return
}



#Main

# Get Start Time
$scriptStartTime = (Get-Date)
$data
If($UseSaved){
    $data = GetData-FromFiles
} Else{
    If($PSVersionTable.PSVersion.Major -ge 3){
        $data = ScrapeWebPages
    } Else{
        $data = ScrapeWebPages -compatibilityMode
    }
}

If(!$data){
    Write-Error "No data to process."
    Exit
}
Write-Host "Processing and creating output"
& .\compare.ps1 -Data $data #returns html

Write-Host 'Done'
Write-Host $(((Get-Date) - $scriptStartTime).totalseconds) 'seconds elapsed'
Exit