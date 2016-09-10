Param(
    [String]
    $Uri
)

$scriptStartTime = (Get-Date)

$parseSumTime = 0;
$doc = $null


$doc = Invoke-WebRequest -Uri $uri -Method Get
$maxIter = 10

For($i = 0; $i -lt $maxIter; $i++){
    $beforeTime = (Get-Date)
    $tables = $doc.ParsedHtml.GetElementsByTagName("TABLE")
    ForEach($item in $tables){
        if($item.className -eq "hirdetesadatok"){
            $elements = $item
        }
    }
    $parseSumTime += (Get-Date) - $beforeTime
}

Write-Host "Non-pipe parsing average time = $($parseSumTime.totalseconds / $maxIter)"

$parseSumTime = 0
For($i = 0; $i -lt $maxIter; $i++){
    $beforeTime = (Get-Date)
    $elements = $doc.ParsedHtml.GetElementsByTagName("TABLE") | Where-Object className -eq "hirdetesadatok"
    $parseSumTime += (Get-Date) - $beforeTime
}

Write-Host "Pipe parsing average time = $($parseSumTime.totalseconds / $maxIter)"


Write-Host 'Done'
Write-Host $(((Get-Date) - $scriptStartTime).totalseconds) 'seconds elapsed'
Exit