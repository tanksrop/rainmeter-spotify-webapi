@echo off
set rootconfig = %1
CD %rootconfig%
start "" pythonw.exe .\main.py
exit