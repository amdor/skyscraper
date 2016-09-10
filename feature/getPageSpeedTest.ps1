Param(
    [String]
    $Uri
)

$scriptStartTime = (Get-Date)

$parseSumTime = 0
$doc = $null
$doc2 = $null


$maxIter = 100

#webrequest
For($i = 0; $i -lt $maxIter; $i++){
    $beforeTime = (Get-Date)
    $doc = Invoke-WebRequest -Uri $uri -Method Get
    $parseSumTime += (Get-Date) - $beforeTime
}

Write-Host "Invoke-WebRequest average time = $($parseSumTime.totalseconds / $maxIter)"

#restmethod
$parseSumTime = 0
For($i = 0; $i -lt $maxIter; $i++){
    $beforeTime = (Get-Date)
    $doc2 = Invoke-RestMethod -Uri $uri -Method Get
    $parseSumTime += (Get-Date) - $beforeTime
}

Write-Host "Rest average time = $($parseSumTime.totalseconds / $maxIter)"

#webrequest without IE
$parseSumTime = 0
For($i = 0; $i -lt $maxIter; $i++){
    $beforeTime = (Get-Date)
    $doc2 = Invoke-WebRequest -Uri $uri -Method Get -UseBasicParsing
    $parseSumTime += (Get-Date) - $beforeTime
}

Write-Host "WebRequest non-IE average time = $($parseSumTime.totalseconds / $maxIter)"


Write-Host 'Done'
Write-Host $(((Get-Date) - $scriptStartTime).totalseconds) 'seconds elapsed'
Exit