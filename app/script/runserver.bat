@echo off
echo Running network configuration script...
powershell.exe -ExecutionPolicy Bypass -File ".\app\script\EnableNetworkDiscovery.ps1"
echo Network configuration script completed.

uvicorn app.main:app --reload