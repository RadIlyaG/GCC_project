param(
    [string]$TargetPath,
    [string]$Arguments,
    [string]$WorkingDirectory
)

$s = New-Object -ComObject WScript.Shell
$shortcut = $s.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\Run_Graphs.lnk')
$shortcut.TargetPath = $TargetPath
$shortcut.Arguments = "`"$Arguments`""
$shortcut.WorkingDirectory = $WorkingDirectory
$shortcut.WindowStyle = 1
$shortcut.IconLocation = "$env:SystemRoot\System32\shell32.dll, 1"
$shortcut.Save()
