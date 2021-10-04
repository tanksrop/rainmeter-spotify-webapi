@echo off
set rootconfig = %1
CD %rootconfig%
start "" python\pythonw.exe .\main.py
exit