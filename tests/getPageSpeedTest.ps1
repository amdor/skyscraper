Param(
    [String]
    $Uri,
    [string]
    $Path
)

$scriptStartTime = (Get-Date)

$getPageSumTime = New-TimeSpan (Get-Date) (Get-Date) 
$doc = $null


$maxIter = 1
$uris = $Uri

if($Path -and (Test-Path $Path -PathType Leaf)){
    $uris = Get-Content $Path
}

ForEach($uri in $uris){
    #webrequest
    For($i = 0; $i -lt $maxIter; $i++){
        $beforeTime = (Get-Date)
        $doc = Invoke-WebRequest -Uri $uri -Method Get
        $getPageSumTime += (Get-Date) - $beforeTime
        Start-Sleep -Milliseconds 1000
    }
}

Write-Host "Invoke-WebRequest average time = $($getPageSumTime.totalseconds / ($maxIter*$uris.Count) )"

#restmethod
$getPageSumTime = 0
$doc = $null
Start-Sleep -Milliseconds 1000
ForEach($uri in $uris){
    For($i = 0; $i -lt $maxIter; $i++){
        $beforeTime = (Get-Date)
        #this doc's gonna be string
        $doc = Invoke-RestMethod -Uri $uri -Method Get
        $getPageSumTime += (Get-Date) - $beforeTime
        Start-Sleep -Milliseconds 1000
    }
}

Write-Host "Rest average time = $($getPageSumTime.totalseconds / ($maxIter*$uris.Count) )"

#webrequest without IE
$getPageSumTime = 0
$doc = $null
Start-Sleep -Milliseconds 1000
 ForEach($uri in $uris){
    For($i = 0; $i -lt $maxIter; $i++){
        $beforeTime = (Get-Date)
        #doc.ParsedHtml is gonna be empty
        $doc = Invoke-WebRequest -Uri $uri -Method Get -UseBasicParsing
        $getPageSumTime += (Get-Date) - $beforeTime
        Start-Sleep -Milliseconds 1000
    }
}
Write-Host "WebRequest non-IE average time = $($getPageSumTime.totalseconds / ($maxIter*$uris.Count) )"


#IE object
$getPageSumTime = 0
$doc = $null
$ie = New-Object -ComObject InternetExplorer.Application
$ie.silent = $true
ForEach($uri in $uris) {
    $beforeTime = (Get-Date)
    $ie.Navigate($uri)
    $i = 0
    while ($ie.busy) {
    	Start-Sleep -Milliseconds 10
        $i++
        if($i -ge 300)
        {
            Write-Host "Navigation timed out" -ForegroundColor Red
            Continue
        }
    }
    $doc=$ie.Document
    #$elements = $doc.GetElementsByTagName("TABLE") | Where-Object {$_.outerHTML -like '*class="hirdetesadatok"*'}
    $getPageSumTime += (Get-Date) - $beforeTime
    Start-Sleep -Milliseconds 1000
}
$ie.Quit()
$ie = $null
Write-Host "IE navigate average time = $($getPageSumTime.totalseconds / ($maxIter*$uris.Count) )"

Write-Host 'Done'
Write-Host $(((Get-Date) - $scriptStartTime).totalseconds) 'seconds elapsed'
Exit