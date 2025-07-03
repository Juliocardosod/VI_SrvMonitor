@echo off
cd
SET local=%~dp0

%local%\nssm.exe install VIVO_SRV_MONITOR SrvMonitor.exe

%local%\nssm set VIVO_SRV_MONITOR Application %local%\SrvMonitor.exe
%local%\nssm set VIVO_SRV_MONITOR AppDirectory %local%
%local%\nssm set VIVO_SRV_MONITOR DisplayName VIVO_SRV_MONITOR

%local%\nssm set VIVO_SRV_MONITOR AppExit Default Exit

%local%\nssm start VIVO_SRV_MONITOR 
echo Instalacao finalizada!
pause