@echo off
cd /d E:\Software\prometheus
prometheus.exe --config.file="E:\Software\python\datascienseproject\prometheus.yml" --web.listen-address=":9090"
pause