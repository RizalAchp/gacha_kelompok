$URL_DWNLD = "https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe"
$OUT_DWNLD = "c:/tmp/python-3.10.4-amd64.exe"

if (Test-Path $OUT_DWNLD){
	Write-Host "Script sudah ada.. Skipping Installasi"
	return;
}
<<<<<<< HEAD
else {
	[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 
	New-Item -ItemType Directory -Force -Path "C:/tmp"
	Invoke-WebRequest -Uri "$URL_DWNLD" -OutFile "$OUT_DWNLD"
	& $OUT_DWNLD /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
	Write-Host "Pre-Installasi Selesai.. Jalankan script 'install.ps1' for installasi program"
}
=======
New-Item -ItemType Directory -Force -Path "C:/tmp"

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 
Invoke-WebRequest -Uri "$URL_DWNLD" -OutFile "$OUT_DWNLD"

& $OUT_DWNLD /quiet InstallAllUsers=1 PrependPath=1 Include_test=0


Write-Host "Pre-Installasi Selesai.. Jalankan script 'install.ps1' for installasi program"
>>>>>>> c6794b6c012b47ed6d2a673461b40d4529163701
