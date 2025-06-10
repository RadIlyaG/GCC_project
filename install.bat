@echo off
setlocal

REM Папка проекта — скрипт предполагает, что он запускается из корня (где лежит qsfc, utils и requirements.txt)

set "PROJECT_DIR=%~dp0"
set "VENV_DIR=%PROJECT_DIR%.venv"
set "PYTHON=%VENV_DIR%\Scripts\python.exe"

echo [1/4] Создание виртуального окружения...
.venv\Scripts\python.exe -m venv "%VENV_DIR%"

echo [2/4] Установка зависимостей...
"%PYTHON%" -m pip install --upgrade pip
"%PYTHON%" -m pip install -r "%PROJECT_DIR%requirements.txt"

echo [3/4] Создание ярлыка на рабочем столе...

powershell -NoProfile -ExecutionPolicy Bypass -File "%PROJECT_DIR%create_shortcut.ps1" ^
 -TargetPath "%PYTHON%" ^
 -Arguments "%PROJECT_DIR%qsfc\PrepareOpenGraphs.py" ^
 -WorkingDirectory "%PROJECT_DIR%qsfc"
echo [4/4] Установка завершена.
pause

