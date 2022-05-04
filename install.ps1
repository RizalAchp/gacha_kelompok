$PYTHON = "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe"
<<<<<<< HEAD
$REQ_PIP = "$PSScriptRoot\requirements.txt"	

if (Get-ExecutionPolicy -eq 'RemoteSigned') {
	Write-Host "Checking Python in Host PC...."
	if (!(Test-Path $PYTHON)){
		Write-Host "Python Tidak Tersedia pada Host pc.."
		Write-Host "Menjalankan script 'pre-install.ps1' untuk menginstall python.."
		& "$PSScriptRoot\pre-install.ps1"
	}
	Write-Host "Creating Virtual Environment.."
	& $PYTHON -m venv venv
	Write-Host "Done Creating Virtual Environtment.."
	Write-Host " "
	Write-Host "Activating Virtual Environment.."
        & "$PSScriptRoot\venv\Scripts\Activate.ps1"
	Write-Host " "
	Write-Host "Installing Module pada $REQ_PIP .."
	$PYTHON_ENV = "$env:VIRTUAL_ENV\Scripts\python.exe"
	& $PYTHON_ENV -m pip install -r $REQ_PIP
	Write-Host "Done Installing Module..."

	$prm = Read-Host -Prompt 'Would you like to build the program? y/n'
	if ($prm -eq 'y') {
		& "$env:VIRTUAL_ENV\Scripts\pyinstaller.exe" "$PSScriptRoot\gacha.spec" 
    	}
	$PROG = "$PSScriptRoot\dist"
	if ($Test-Path $PROG){
		[System.Environment]::SetEnvironmentVariable('Path',$PROG,[System.EnvironmentVariableTarget]::Process);	
		[System.Environment]::SetEnvironmentVariable('Path',$PROG,[System.EnvironmentVariableTarget]::User);	
	}
	$ex = Read-Host -Prompt 'exit ? [any]'
	if (!($ex -eq "_")){
		Exit 0
	}
} else {
	Write-host "Execution Policy does not allow this script to run properly"
	Write-host "If you have the proper permissions,"
	Write-Host "Please close powershell,"
	Write-host "then right click the powershell icon and run as administrator"
	Write-host "Once in the powershell environment, execute the following:"
	Write-host "Set-ExecutionPolicy RemoteSigned -Force"

	$ex = Read-Host -Prompt 'exit ? y/n'
	if (!($ex -eq "_")){
		Exit 0
	}
}


=======
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
>>>>>>> c6794b6c012b47ed6d2a673461b40d4529163701
