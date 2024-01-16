# Get drive with System32 folder
$systemDrive = (Get-WmiObject Win32_OperatingSystem).SystemDrive
# Wait for 1 second until easy closed
Start-Sleep -Seconds 1
# Download easy file
Invoke-WebRequest -Uri "https://github.com/easy-pkg/easy/raw/main/dist/easy.exe" -OutFile "$systemDrive\Windows\System32\easy.exe"
# Wait for another 1 second
Start-Sleep -Seconds 1
# Download default easy config
Invoke-WebRequest -Uri "https://github.com/easy-pkg/easy/raw/main/dist/easy.config.json" -OutFile "$systemDrive\Windows\System32\easy.config.json"
# Output the message
Write-Output "$(Write-Host -ForegroundColor Green '✔') $(Write-Host -ForegroundColor Magenta 'easy') $(Write-Host -ForegroundColor White 'will be updated after this message.')"
