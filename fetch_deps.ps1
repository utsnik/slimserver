$ErrorActionPreference = "Stop"

Write-Host "Downloading OPKG..."
Invoke-WebRequest -Uri "https://downloads.yoctoproject.org/mirror/sources/trunk_opkg.googlecode.com_.svn_518_.tar.gz" -OutFile "opkg-svn518.tar.gz"

Write-Host "Repacking OPKG..."
if (Test-Path opkg_ext) { Remove-Item -Recurse -Force opkg_ext }
New-Item -ItemType Directory -Path opkg_ext | Out-Null
tar -xzf opkg-svn518.tar.gz -C opkg_ext
if (Test-Path "opkg_ext\trunk") {
    Rename-Item -Path "opkg_ext\trunk" -NewName "opkg"
}
tar -czf opkg-4545.tar.gz -C opkg_ext opkg

Write-Host "Downloading JiveTest from SqueezeOS repo..."
Invoke-WebRequest -Uri "https://github.com/ralph-irving/squeezeos/archive/refs/heads/master.zip" -OutFile "squeezeos-master.zip"

Write-Host "Extracting and packing JiveTest..."
if (Test-Path squeezeos_ext) { Remove-Item -Recurse -Force squeezeos_ext }
Expand-Archive -Path squeezeos-master.zip -DestinationPath squeezeos_ext -Force
tar -czf jivetest-1.0.tar.gz -C squeezeos_ext\squeezeos-master jivetest

Write-Host "Cleaning up temporary files..."
Remove-Item -Recurse -Force opkg_ext
Remove-Item -Recurse -Force squeezeos_ext
Remove-Item opkg-svn518.tar.gz
Remove-Item squeezeos-master.zip

Write-Host "SUCCESS: jivetest-1.0.tar.gz and opkg-4545.tar.gz are ready."
