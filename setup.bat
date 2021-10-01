@echo off
set rootconfig = %1
CD %rootconfig%
if exist importantinfo.json goto exit
pip install requests PySide2
python .\setup.py
exit