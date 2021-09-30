@echo off
pip install requests PySide2
set rootconfig = %1
CD %rootconfig%
python .\setup.py