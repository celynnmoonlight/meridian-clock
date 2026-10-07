param([switch]$Installer)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
Push-Location $projectRoot
try {
    uv sync --locked
    if ($LASTEXITCODE -ne 0) { throw 'Dependency sync failed.' }
    uv run python -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) { throw 'Tests failed.' }
    uv run pyinstaller --noconfirm packaging/meridian.spec
    if ($LASTEXITCODE -ne 0) { throw 'Application build failed.' }
    if ($Installer) {
        $compiler = Get-Command ISCC.exe -ErrorAction SilentlyContinue
        $compilerPath = if ($compiler) { $compiler.Source } else { Join-Path $env:LOCALAPPDATA 'MeridianClockBuildTools\InnoSetup\ISCC.exe' }
        if (-not (Test-Path -LiteralPath $compilerPath)) { throw 'Install Inno Setup 6 and add ISCC.exe to PATH to build the installer.' }
        & $compilerPath packaging/windows.iss
        if ($LASTEXITCODE -ne 0) { throw 'Installer build failed.' }
    }
} finally { Pop-Location }
