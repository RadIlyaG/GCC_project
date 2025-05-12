@echo off
setlocal

REM Папка проекта — скрипт предполагает, что он запускается из корня (где лежит qsfc, utils и requirements.txt)
set PROJECT_DIR=%~dp0
set VENV_DIR=%PROJECT_DIR%.venv
set PYTHON=%VENV_DIR%\Scripts\python.exe

echo [1/4] Создание виртуального окружения...
python -m venv "%VENV_DIR%"

echo [2/4] Установка зависимостей...
"%PYTHON%" -m pip install --upgrade pip
"%PYTHON%" -m pip install -r "%PROJECT_DIR%requirements.txt"

echo [3/4] Создание ярлыка на рабочем столе...
REM PowerShell создаёт ярлык
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
 "$s = New-Object -ComObject WScript.Shell; ^
  $shortcut = $s.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\Run_Graphs.lnk'); ^
  $shortcut.TargetPath = '%PYTHON%'; ^
  $shortcut.Arguments = '\"%PROJECT_DIR%qsfc\PrepareOpenGraphs.py\"'; ^
  $shortcut.WorkingDirectory = '%PROJECT_DIR%qsfc'; ^
  $shortcut.WindowStyle = 1; ^
  $shortcut.IconLocation = '%SystemRoot%\System32\shell32.dll, 1'; ^
  $shortcut.Save()"

echo [4/4] Установка завершена.
pause
