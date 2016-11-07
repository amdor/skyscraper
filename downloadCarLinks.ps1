<#.
.SYNOPSIS
This script outputs a list of urls. Gets every cars' link from the page given and every page after
that(until depth is reached), navigating by url tampering.
Depth parameter tells how many pages should the script scrape before stoping. If there is no more following pages, 
but depth number of pages are not yet visited, the script stops.
Uses 10 results per page view
.PARAMETER Uri
The starting page of links.
.PARAMETER Depth
The maximum number of sequential pages to be scraped.
Author: Zsolt Deak, 2015.08.25
#>


Param
 (
    [Parameter(Mandatory=$true, ParameterSetName = "Online")]
    [String]
    $Uri,
    [int32]
    $Depth = 5
 ) 


Function Gather-Links{
    Param
    (
        [String]
        $url = $Uri
    )

    Write-Host "Navigating to url $url"
    $Script:doc = Try { Invoke-WebRequest -Uri $url -Method Get } 
    Catch { $_.Exception.Response }
    #Response is OK, and yet to be html
    if(($Script:doc.StatusCode -ne 200) -or !($Script:doc.Headers['Content-Type'] -like '*text/html*') )
    {
        Throw "Inproducable server response" #exit
    }

    #Guarantee noverflow (after the last page url tampering causes redirect to page 1)
    If($Script:doc.BaseResponse.ResponseUri.OriginalString -ne $nextPage) {
        Throw "Tampering overflow"
    }

    #Grab the links from the page with regex
    #Must be -le to save the 10th link as well
    [regex]$linkRegex = "http://www.hasznaltauto.hu/auto/(.*/.*)*`">"
    Write-Host "Finding and saving links to $outfile..."
    $links = $linkRegex.Matches($Script:doc.Content)
    $link = $links[0]
    For($i = 1; $i -le $links.Count; $i++){
        If($links[$i].Value -ne $link.Value){
            Out-File $outfile -InputObject $link.Value.Substring(0,$link.Length-2) -Append
        }
        $link = $links[$i]
    }

    Write-Host "Done gathering the links from the page"
}



#MAIN

$scriptStartTime = (Get-Date)

$outfile = '.\src\scrapedLinks.txt'
If(Test-Path $outfile){
    Remove-Item $outfile
}

#Gather-Links
$loopCounter = 0
$nextPage = $Uri

While( $loopCounter -lt $Depth){
    Try{
        Write-Host "Depth $loopCounter done"
        $loopCounter++
        Gather-Links -url $nextPage
        Write-Host "Getting next page's url"
        if( $nextPage -match '[1-9]{2}$') {
            $nextPage = $nextPage.Substring(0,$nextPage.Length-2) + ([convert]::ToInt32($nextPage.Substring($nextPage.Length-2, 2), 10 ) + 1 )
        } else {
            $nextPage = $nextPage.Substring(0,$nextPage.Length-1) + ([convert]::ToInt32($nextPage.Substring($nextPage.Length-1, 1), 10 ) + 1 )
        }
    } Catch {
        Switch -Wildcard ($Error[0].Exception) {
            '*Tampering overflow*' {
                Write-Host "Reached last page, stopping...."
                #Hack, since break cannot be used here
                $loopCounter = $Depth
            }
            Default {
                Write-Host "Something went wrong.`nInner exception: $($Error[0].Exception)"
            }
        }
    }
}

Write-Host $(((Get-Date) - $scriptStartTime).totalseconds) 'seconds elapsed'