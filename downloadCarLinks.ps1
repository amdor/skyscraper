<#.
.SYNOPSIS

.PARAMETER Uri
The starting page of links.
Author: Zsolt Deak, 2015.08.25
#>


Param
 (
    [Parameter(Mandatory=$true, ParameterSetName = "Online")]
    [String]
    $Uri
 ) 


Function Gather-Links{
    Param
    (
        [String]
        $url = $Uri
    )

    Write-Host "Navigating to url"
    [Microsoft.PowerShell.Commands.HtmlWebResponseObject]$script:doc = Try { Invoke-WebRequest -Uri $url -Method Get } Catch { $_.Exception.Response }
    #Response is OK, and yet to be html
    if(($doc.StatusCode -ne 200) -or !($doc.Headers['Content-Type'] -like '*text/html*') )
    {
        Throw "Inproducable server response" #exit
    }

     #Parse data
    Write-Host "Parsing results page..."
    Try{
        $elements = $script:doc.ParsedHtml.GetElementsByTagName("DIV") | Where-Object className -contains "talalati_lista_head"
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

    Write-Host "Done gathering the links"
}



#MAIN

$scriptStartTime = (Get-Date)

$outfile = '.\src\scrapedLinks.txt'
If(Test-Path $outfile){
    Remove-Item $outfile
}

Gather-Links
While($nextPage = $doc.ParsedHtml.GetElementsByTagName("A") | Where-Object title -eq "Következõ oldal"){
    $nextPage = ([regex]"href=(.*/.*)+`"").Match($nextPage[0].outerHtml).Value
    Gather-Links -url "www.hasznaltauto.hu$($nextPage.Substring(6, $nextPage.Length-2))"
}

Write-Host $(((Get-Date) - $scriptStartTime).totalseconds) 'seconds elapsed'