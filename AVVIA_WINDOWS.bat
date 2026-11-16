@echo off
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel%==0 (set "PY=py") else (set "PY=python")
%PY% -m pip install -r requirements.txt
if errorlevel 1 (echo Installazione non riuscita. Installa Python 3.10+ e riprova. & pause & exit /b 1)
%PY% -m streamlit run app.py
pause
