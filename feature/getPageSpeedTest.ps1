Param(
    [String]
    $Uri,
    [string]
    $Path
)

$scriptStartTime = (Get-Date)

$parseSumTime = 0
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
        $tables = $doc.ParsedHtml.GetElementsByTagName("TABLE")
        ForEach($item in $tables){
            if($item.className -eq "hirdetesadatok"){
                $elements = $item
            }
        }
        $parseSumTime += (Get-Date) - $beforeTime
    }
}

Write-Host "Invoke-WebRequest average time = $($parseSumTime.totalseconds / ($maxIter*$uris.Count) )"

#restmethod
$parseSumTime = 0
$doc = $null
Start-Sleep -Milliseconds 1000
ForEach($uri in $uris){
    For($i = 0; $i -lt $maxIter; $i++){
        $beforeTime = (Get-Date)
        #this doc's gonna be string
        $doc = Invoke-RestMethod -Uri $uri -Method Get
        $parseSumTime += (Get-Date) - $beforeTime
    }
}

Write-Host "Rest average time = $($parseSumTime.totalseconds / ($maxIter*$uris.Count) )"

#webrequest without IE
$parseSumTime = 0
$doc = $null
Start-Sleep -Milliseconds 1000
 ForEach($uri in $uris){
    For($i = 0; $i -lt $maxIter; $i++){
        $beforeTime = (Get-Date)
        #doc.ParsedHtml is gonna be empty
        $doc = Invoke-WebRequest -Uri $uri -Method Get -UseBasicParsing
        $parseSumTime += (Get-Date) - $beforeTime
    }
}
Write-Host "WebRequest non-IE average time = $($parseSumTime.totalseconds / ($maxIter*$uris.Count) )"

Write-Host 'Done'
Write-Host $(((Get-Date) - $scriptStartTime).totalseconds) 'seconds elapsed'
Exit