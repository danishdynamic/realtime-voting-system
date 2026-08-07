# start.ps1
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot
$env:PYTHONPATH = "$projectRoot"

Write-Host "Starting Flask API..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot'; `$env:PYTHONPATH='$projectRoot'; py -m backend.run"

Write-Host "Starting WebSocket Server..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot'; `$env:PYTHONPATH='$projectRoot'; py -m backend.websocket_server"

Write-Host "Starting Kafka Consumer..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot'; `$env:PYTHONPATH='$projectRoot'; py -m backend.app.consumers.vote_consumer"

Write-Host "Starting Frontend (React)..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot\frontend'; npm run dev"

Write-Host ""
Write-Host "All services started! Access your app at:"
Write-Host "  Frontend:  http://localhost:3000"
Write-Host "  API:       http://localhost:5000/api/health"
Write-Host "  WebSocket: ws://localhost:8000"
Write-Host ""
Write-Host "Press Ctrl+C in each window to stop."