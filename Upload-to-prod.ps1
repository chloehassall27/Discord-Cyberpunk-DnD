# Load WinSCP .NET assembly
Add-Type -Path "$PSScriptRoot/resources/WinSCPnet.dll"

try {
    Get-Content .env | foreach {
        $name, $value = $_.split('=')
        if ([string]::IsNullOrWhiteSpace($name) || $name.Contains('#')) {
          continue
        }
        Set-Content env:\$name $value
    }
}
catch {
    Write-Error "Failed to load .env file"
    exit 1
}

if ($env:SSH_PPK_PASSPHRASE -eq $Null ){
    Write-Error "Failed to find SSH_PPK_PASSPHRASE in .env file"
    exit 2
}

# Setup session options
$sessionOptions = New-Object WinSCP.SessionOptions -Property @{
    Protocol = [WinSCP.Protocol]::Sftp
    HostName = "20.246.94.220"
    UserName = "cyberpunk"
    SshPrivateKeyPath = "$PSScriptRoot\bot-vm.ppk"
    PrivateKeyPassphrase = $env:SSH_PPK_PASSPHRASE
    SshHostKeyFingerprint = "ssh-rsa 3072 ROV8vMDQCqFLu6DX8OjDK5vLCGJMK3przAL+T7KON9g"
}

$session = New-Object WinSCP.Session -Property @{
    ExecutablePath = "$PSScriptRoot/resources/WinSCP.exe"
}

# Create the filemask. Include all python files, all resources in ./resources, prefs.json, and requirements.txt
$transferOptions = New-Object WinSCP.TransferOptions
$transferOptions.FileMask = "*.py; $PSScriptRoot/resources/*; $PSScriptRoot/requirements.txt; $PSScriptRoot/prefs.json"
$transferOptions.AddRawSettings("ExcludeEmptyDirectories", "1")

try
{
    # Connect
    $session.Open($sessionOptions)

    # Upload files, collect results
    $transferResult = $session.PutFiles($PSScriptRoot, "/home/cyberpunk/server", $False, $transferOptions)

    if ($transferResult.Transfers.Count -eq 0){
        Write-Error "No transfers made"
        exit 3
    }

    # Iterate over every transfer
    foreach ($transfer in $transferResult.Transfers)
    {
        # Success or error?
        if ($transfer.Error -ne $Null)
        {
            Write-error "Upload of $($transfer.FileName) failed: $($transfer.Error.Message)"
            $error = $True
        }
    }

    if ($error -ne $True){
        Write-Host -ForegroundColor Green "All files uploaded successfully!"
    }
    
    Write-Host -ForegroundColor Cyan "$($transferResult.Transfers.Count) transfer(s) attempted :)"
}
finally
{
    # Disconnect, clean up
    $session.Dispose()
}

exit 0