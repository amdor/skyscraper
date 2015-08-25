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

$url = $Uri

[Microsoft.PowerShell.Commands.HtmlWebResponseObject]$doc = Try { Invoke-WebRequest -Uri $url -Method Get <#-OutFile $Dest -PassThru -UseBasicParsing#> } Catch { $_.Exception.Response }
#Response is OK, and yet to be html
if(($doc.StatusCode -ne 200) -or !($doc.Headers['Content-Type'] -like '*text/html*') )#$IndexPage.Headers -contains 'text/html') )
{
    Throw "Inproducable server response" #exit
}

 #Parse data
Write-Host "Parsing data..."
Try{
    $elements = $doc.ParsedHtml.GetElementsByTagName("DIV") | where {$_.className -contains "talalati_lista_head"}
} Catch{
    Continue
}
