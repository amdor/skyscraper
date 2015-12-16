<#.
.SYNOPSIS
This script outputs a list of urls. Gets every cars' link from the page given and every page after
that(until depth is reached), navigating with the next page button amongst them.
Depth parameter tells how many pages should the script scrape before stoping. If there is no more following pages, 
but depth number of pages are not yet visited, the script stops.
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
    [Microsoft.PowerShell.Commands.HtmlWebResponseObject]$Script:doc = Try { Invoke-WebRequest -Uri $url -Method Get } Catch { $_.Exception.Response }
    #Response is OK, and yet to be html
    if(($Script:doc.StatusCode -ne 200) -or !($Script:doc.Headers['Content-Type'] -like '*text/html*') )
    {
        Throw "Inproducable server response" #exit
    }

     <#Parse data and get the links
    Write-Host "Parsing results page..."
    Try{
        $elements = $Script:doc.ParsedHtml.GetElementsByTagName("DIV") | Where-Object className -contains "talalati_lista_head"
    } Catch{
        Write-Host "Parsing failed"
        Continue
    }

    #Use only needed divs and get their link
    Write-Host "Finding and saving links to $outfile..."
    [regex]$regExpression = "http.*`""
    ForEach($element in $elements){
        $link = $regExpression.Match($element.innerHtml).Value
        If($link){
            Out-File $outfile -InputObject $link.Substring(0,$link.Length-1) -Append
        }
        $link = $null   
    }
    #>
    #Grab the links from the page with regex
    [regex]$linkRegex = "http://www.hasznaltauto.hu/auto/(.*/.*)*`">"
    Write-Host "Finding and saving links to $outfile..."
    $links = $linkRegex.Matches($Script:doc.Content)
    $link = $links[0]
    For($i = 1; $i -lt $links.Count; $i++){
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

Gather-Links
$loopCounter = 1
$nextPageRegex = [regex]"class=`"lapozas`".{160,250}Következõ oldal"
While(($loopCounter -lt $Depth) -and ($nextPage = (($nextPageRegex.Match($Script:doc.Content).Value -Split "href=`"")[1] -Split "`" title")[0])){#($Script:doc.ParsedHtml.GetElementsByTagName("A") | Where-Object title -eq "Következõ oldal").href)){
    Try{
        Write-Host "Depth $loopCounter done"
        Gather-Links -url "www.hasznaltauto.hu$nextPage"#$($nextPage[0].Substring(6, $nextPage[0].Length-6))"
        $loopCounter++
        Write-Host "Getting next page's url"
    } Catch{
        Write-Host "Something went wrong.`nInner exception: $($_.Exception)"
        Break
    }
}

Write-Host $(((Get-Date) - $scriptStartTime).totalseconds) 'seconds elapsed'