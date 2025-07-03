@echo off
cd
SET local=%~dp0

%local%\nssm.exe remove VIVO_SRV_MONITOR

echo Desinstalacao finalizada!
pause