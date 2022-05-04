$PYTHON = "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe"
$REQ_PIP = "$PSScriptRoot\requirements.txt"

[System.Environment]::SetEnvironmentVariable('Path', $PSScriptRoot,[System.EnvironmentVariableTarget]::Process);	
[System.Environment]::SetEnvironmentVariable('Path', $PSScriptRoot,[System.EnvironmentVariableTarget]::User);	
if (Test-Path $REQ_PIP){
	Write-Host "Checking Python in Host PC...."
	if (!(Test-Path $PYTHON)){
		Write-Host "Python Tidak Tersedia pada Host pc.."
		Write-Host "jalankan script 'pre-install.ps1' untuk menginstall python.."
		Exit 1
	}
	
	Write-Host "Installing Module pada $REQ_PIP ..."
	& $PYTHON -m pip install -r $REQ_PIP

	Write-Host "Done Installing Module..."
	$env:Path += ";$PSScriptRoot"
	Write-Host "Enjoy.. And Run the script by running script program 'python gacha start'"
	Write-Host "	or run 'python ./gacha -h' for help command"
}
