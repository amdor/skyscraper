<#.
.SYNOPSIS
This script is for scraping webpages.
The output format is fixed yet. 
.PARAMETER Uri
The uri of the targeted webpage
.PARAMETER Dest
The destination file the results (html) should be written to. Defaults to
scraperOutput.html. Dest also determines where other info will be saved.
.PARAMETER UseSaved
If used, the script gets data from Dest's folder
.PARAMETER ParseHTML
If set, the script uses Internet Explorer to parse the html content taken as
response for the request sent to the Uri
.NOTES
Author: Zsolt Deak, 2015.07.09
#>

Param
 (
    [Parameter(Mandatory=$true)]
    [String]
    $Uri,
    [String]
    $Dest = ".\src\",
    [switch]
    $UseSaved,
    [switch]
    $ParseHTML
 ) 

 function Save-Response($Response)
 {
    $DestFolder = Split-Path $Dest -Parent
    Set-Content -Path $Dest -Value $Response.Content -Force
    Set-Content -Path $($DestFolder+'\Links') -Value $Response.Links
    Set-Content -Path $($DestFolder+'\forms') -Value $Response.Forms
    Set-Content -Path $($DestFolder+'\inputfields') -Value $Response.InputFields

 }

#Make path leaf
$Dest = If(Test-Path $Dest -PathType Leaf){  $Dest } Else { $Dest + "scraperOutput.html" }

#Check if the file's container exists, now that the path is sure to be leaf.
If(!(Test-Path (Split-Path -Path $Dest -Parent))) 
{
    Throw "Your destination file is either invalid or not exists."
    #exit...
}

#GET request to the given uri, the results are saved to dest and returned to the pipeline as well
if($ParseHTML)
{
    [Microsoft.PowerShell.Commands.HtmlWebResponseObject]$IndexPage = Try { Invoke-WebRequest -Uri $Uri -Method Get <#-OutFile $Dest -PassThru -UseBasicParsing#> } Catch { $_.Exception.Response }
}
else
{
    #no $IndexPage.ParsedHTML and AllElements
    [Microsoft.PowerShell.Commands.BasicHtmlWebResponseObject]$IndexPage = Try { Invoke-WebRequest -Uri $Uri -Method Get <#-OutFile $Dest -PassThru#> -UseBasicParsing } Catch { $_.Exception.Response }
}


#Response is OK, and yet to be html
if(($IndexPage.StatusCode -ne 200) -or !($IndexPage.Headers['Content-Type'] -like '*text/html*') )#$IndexPage.Headers -contains 'text/html') )
{
    Throw "Inproducable server response" #exit
}
#save content
#Save-Response($IndexPage)

#optional output
#Out-File -InputObject $IndexPage -FilePath $($(Split-Path $Dest -Parent) + '\response.txt')

#Get the columns from the page
#$Columns = $IndexPage.AllElements | Where { $_.tagName -eq 'TABLE' -and $_.class -eq 'hirdetesadatok'} | Select outerHTML 
$IndexPage.Content | Out-File '.\src\html.html'

Write-Output 'Done, success'
Exit