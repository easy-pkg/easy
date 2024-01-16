# Get drive with System32 folder
$systemDrive = (Get-WmiObject Win32_OperatingSystem).SystemDrive
# Download easy file
Invoke-WebRequest -Uri "https://github.com/easy-pkg/easy/raw/main/dist/easy.exe" -OutFile "$systemDrive\Windows\System32\easy.exe"
# Download default easy config
Invoke-WebRequest -Uri "https://github.com/easy-pkg/easy/raw/main/dist/easy.config.json" -OutFile "$systemDrive\Windows\System32\easy.config.json"
# Run easy
Start-Process -FilePath "cmd.exe /c $systemDrive\Windows\System32\easy.exe"
