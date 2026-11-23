$ErrorActionPreference = 'Stop'
$configPath = Join-Path $PSScriptRoot 'config.local.json'
if (-not (Test-Path $configPath)) { throw 'Copy config.example.json to config.local.json and edit it first.' }
$config = Get-Content $configPath -Raw | ConvertFrom-Json
$board = $config.board_ip
$python = $config.python_path
$receiver = $PSScriptRoot
$pc = $config.pc_ip
$env:MONITOR_HOST = $pc
$url = "http://${pc}:8000"
try {
    if (-not (Test-Path $python)) { throw "Python not found: $python" }
    if (-not (Test-Path "$receiver\server.py")) { throw 'Receiver is not installed.' }
    $online = $false
    try { $null = Invoke-RestMethod "$url/api/status" -TimeoutSec 2; $online = $true } catch {}
    if (-not $online) {
        $serverCommand = "Set-Location -LiteralPath '$receiver'; & '$python' -u server.py"
        Start-Process powershell.exe -ArgumentList @('-NoExit','-Command',$serverCommand)
        for ($i=0; $i -lt 20; $i++) {
            Start-Sleep -Milliseconds 500
            try { $null = Invoke-RestMethod "$url/api/status" -TimeoutSec 1; $online = $true; break } catch {}
        }
    }
    if (-not $online) { throw 'Receiver failed to start. Check the receiver window and PC IP address.' }
    Start-Process $url
    Write-Host 'Starting Orange Pi. Enter the SSH password if requested.'
    Write-Host 'Keep this window open. Ctrl+C stops detection. Stop the receiver in its own window.'
    ssh -t -o ConnectTimeout=8 "orangepi@$board" "cd /home/orangepi/orangepi_person_detection && ALARM_SERVER_URL=$url flock -n .detector.lock .venv/bin/python -u main.py"
    Write-Host "SSH exited with code $LASTEXITCODE. If already running, stop the old detection window first."
} catch {
    Write-Host $_ -ForegroundColor Red
}
Read-Host 'Press Enter to close'
