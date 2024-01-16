# Download easy file
Invoke-WebRequest -Uri "https://github.com/easy-pkg/easy/raw/main/dist/easy.exe" -OutFile "C:\Windows\System32\easy.exe"
# Download default easy config
Invoke-WebRequest -Uri "https://github.com/easy-pkg/easy/raw/main/dist/easy.config.json" -OutFile "C:\Windows\System32\easy.config.json"
