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
$scriptStartTime = (Get-Date)

$outfile = '.\src\scrapedLinks.txt'
If(Test-Path $outfile){
    Remove-Item $outfile
}

$url = $Uri

[Microsoft.PowerShell.Commands.HtmlWebResponseObject]$doc = Try { Invoke-WebRequest -Uri $url -Method Get } Catch { $_.Exception.Response }
#Response is OK, and yet to be html
if(($doc.StatusCode -ne 200) -or !($doc.Headers['Content-Type'] -like '*text/html*') )
{
    Throw "Inproducable server response" #exit
}

 #Parse data
Write-Host "Parsing data..."
Try{
    $elements = $doc.ParsedHtml.GetElementsByTagName("DIV") | Where-Object className -contains "talalati_lista_head"
} Catch{
    Continue
}

Write-Host "Finding links..."
[regex]$regExpression = "http.*`""
ForEach($element in $elements){
    $link = $regExpression.Match($element.innerHtml).Value
    If($link){
        Out-File $outfile -InputObject $link.Substring(0,$link.Length-1) -Append
    }
    $link = $null   
}

Write-Host "Done"
Write-Host $(((Get-Date) - $scriptStartTime).totalseconds) 'seconds elapsed'