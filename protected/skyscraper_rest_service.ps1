




function Process-RequestsAsync{
     Param( 
        [System.Net.HttpListenerContext]
        $Context
     )
    $innerContext = $Context
    $response = $context.Response

    #Construct a response.
    If($innerContext.Request.HasEntityBody){
        [System.IO.Stream]$postBodyStream = $innerContext.Request.InputStream
        $encoding = $innerContext.Request.ContentEncoding
        [System.IO.StreamReader]$reader = New-Object System.IO.StreamReader($postBodyStream,$encoding)
        $uri = $reader.ReadToEnd()
        $responseString =  & .\skyscraper_ie.ps1 -Uri $uri
        $buffer = [System.Text.Encoding]::UTF8.GetBytes($responseString)
        #Get a response stream and write the response to it.
        $response.ContentLength64 = $buffer.Length
        [System.IO.Stream]$output = $response.OutputStream
        $output.Write($buffer,0,$buffer.Length)
        #You must close the output stream.
        $output.Close()
    } Else{
        $response.StatusCode = 400
        $response.OutputStream.Close()
    }
}


function Process-Requests{
    Write-Host "Process-Request method called"

    $context = $listener.GetContext()
    Process-RequestsAsync -Context $context #TODO  Make it async in PS (does not work with powershell object and start-job)
}




#MAIN
try{
    if($Host.UI.RawUI.KeyAvailable -and (3 -eq  
        [int]$Host.UI.RawUI.ReadKey("AllowCtrlC,IncludeKeyUp,NoEcho").Character)){
         Write-Host "CTRL+C read"
    }

    $url = 'http://localhost:8089/'
    $listener = New-Object System.Net.HttpListener
    $listener.Prefixes.Add($url)
    $listener.Stop()
    $listener.Start()

    Write-Host "Started listening at $url"

    While($listener.IsListening){
       <#[System.Management.Automation.PowerShell]$psInstance = [System.Management.Automation.PowerShell]::Create()
       [void]$psInstance.AddCommand("Process-Requests", $true)
       $psInstance.Invoke()#>
       Process-Requests
    }

    #Clean up
    if($listener){
        $listener.Stop()
    }

    $listener.Close()
}finally{
    if($listener){
        $listener.Abort()
        $listener.Close()
    }
}
Exit