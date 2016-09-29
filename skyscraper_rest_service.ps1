<#
.SYNOPSIS
Listens to localhost:8089. If hears any POST request, repsponse them with the proper html content 
given back by the other powershell function. Waits for car urls in the post body, separated by new
line character.
10 urls are processed at maximum.
.NOTES
Author: Zsolt Deak, 2015.12
#>


<#
.SYNOPSIS
Process requests (yet to be async) by sending them forward to the function
.PARAMETER Context
The HttpListenerContext from the request that is caught
#>
function Process-RequestsAsync{
     Param( 
        [System.Net.HttpListenerContext]
        $Context
     )
    $innerContext = $Context
    $response = $innerContext.Response

    #Check method
    If($Context.Request.HttpMethod -ne "POST") {
        Write-Host "Method not allowed"
        $response.StatusCode = 405
        $response.OutputStream.Close()
        Return
    }

    #Construct a response.
    If($innerContext.Request.HasEntityBody){
        [System.IO.Stream]$postBodyStream = $innerContext.Request.InputStream
        $encoding = $innerContext.Request.ContentEncoding
        [System.IO.StreamReader]$reader = New-Object System.IO.StreamReader($postBodyStream,$encoding)

        $readCounter = 0
        $uris = @()
        #if count is less than readCounter, it means las read was unsuccessfull
        While(($uris.Count -eq $readCounter) -and ($readCounter -lt 10)){
            $readCounter++
            $newLine = $reader.ReadLine()
            Write-Host "Line read " + $newLine
            if($newLine){
                $uris += $newLine
            }
        }
        Write-Host "Post body content reciever $uris"
        $responseString =  & .\skyscraper_ie.ps1 -Uri $uris
        $buffer = [System.Text.Encoding]::UTF8.GetBytes($responseString)

        #Get a response stream and write the response to it.
        $response.ContentLength64 = $buffer.Length
        [System.IO.Stream]$output = $response.OutputStream
        $output.Write($buffer,0,$buffer.Length)
        $response.StatusCode = 200

        #Must close the output stream.
        $output.Close()
    } Else{
        Write-Host "No content found"
        $response.StatusCode = 400
        $response.OutputStream.Close()
    }
}


function Process-Requests{
    $context = $listener.GetContext()
    Process-RequestsAsync -Context $context #TODO  Make it async in PS (does not work with powershell object and start-job)
}




#MAIN
try{
#stops one request after stop sign
    if($Host.UI.RawUI.KeyAvailable -and (3 -eq  
        [int]$Host.UI.RawUI.ReadKey("AllowCtrlC,IncludeKeyUp,NoEcho").Character)){
         Write-Host "CTRL+C read"
    }

    $url = 'http://+:8089/'
    $Script:listener = New-Object System.Net.HttpListener
    $listener.Prefixes.Add($url)
    $listener.Stop()
    $listener.Start()

    Write-Host "Started listening at $url"
    While($listener.IsListening){
        Try {
            <#[System.Management.Automation.PowerShell]$psInstance = [System.Management.Automation.PowerShell]::Create()
            [void]$psInstance.AddCommand("Process-Requests", $true)
            $psInstance.Invoke()#>
            Write-Host "Waiting for request"
            Process-Requests
        } Catch {
            Continue
        }
    }

    #Clean up
    if($listener){
        $listener.Stop()
    }

    $listener.Close()
}catch{
    Write-Host "Exception  $($_.Exception)"
}finally{
    if($listener){
        $listener.Abort()
        $listener.Close()
    }
}
Exit