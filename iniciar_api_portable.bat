
@echo off
echo Activando el entorno virtual y ejecutando la API...
cd %~dp0
call entorno_estimador_nuevo\Scriptsctivate
pip install -r requirements.txt
python app.py
