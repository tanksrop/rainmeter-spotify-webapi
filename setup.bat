@echo off
set rootconfig = %1
CD %rootconfig%
if exist importantinfo.json goto exit
start "" python\python.exe .\setup.py
exit