$ErrorActionPreference = 'Stop'

$launcher = Join-Path $PSScriptRoot 'start-windows.cmd'
if (-not (Test-Path -LiteralPath $launcher)) {
    throw "Launcher not found: $launcher"
}

$desktop = [Environment]::GetFolderPath([Environment+SpecialFolder]::DesktopDirectory)
# Unicode escapes keep this script compatible with Windows PowerShell 5.1.
$name = "$([char]0x56FE)$([char]0x7247)$([char]0x8F6C) PDF"
$shortcutPath = Join-Path $desktop "$name.lnk"
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $env:ComSpec
$shortcut.Arguments = '/d /c ""' + $launcher + '""'
$shortcut.WorkingDirectory = $PSScriptRoot
$shortcut.Description = 'Start Image to PDF in your browser'
$shortcut.IconLocation = "$env:SystemRoot\System32\shell32.dll,71"
$shortcut.WindowStyle = 7
$shortcut.Save()
Write-Output "Desktop shortcut created: $shortcutPath"
