REM Copy and paste script to the route path (RelaxApp). Otherwise it won't work.

@echo off
chcp 65001 >nul

setlocal enabledelayedexpansion

echo. 
echo ======================
echo   Starting Packaging
echo ======================
echo.
echo Current directory: %cd%
echo Cleaning old packaging...
echo.

call :remove_folder "build"
call :remove_folder "dist"

echo. 
echo ============================
echo   Packaging in progress...
echo ============================
echo.

python -m PyInstaller RelaxApp.spec

set STATUS=%ERRORLEVEL%
set "package=False"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ==================================
    echo   Packaging has been successful!
    echo ==================================
    echo.
    call :remove_folder "build"
    set "package=True"
) else (
    echo.
    echo =========================
    echo   Packaging has failed!
    echo =========================
    echo.
)

set "folder_number=1"

if "!package!"=="True" (
    :verificar
    if exist "E:\Programación\Portfolio\AppEmpaquetada\Versión !folder_number!" (
        set /a folder_number+=1
        goto verificar
        
    ) else (
    echo Creating folder "Versión !folder_number!"...
    mkdir "E:\Programación\Portfolio\AppEmpaquetada\Versión !folder_number!"
    echo Moving folder "RelaxApp" to "E:\Programación\Portfolio\AppEmpaquetada\Versión !folder_number!"
    move "dist\RelaxApp" "E:\Programación\Portfolio\AppEmpaquetada\Versión !folder_number!"
    call :remove_folder "dist"
    )
)

echo.
echo ========================
echo   Packaging has ended!
echo ========================
echo.

pause

goto :EOF

REM ======== Functions =========
:remove_folder
set "folder=%~1"
if exist "!folder!" (
    echo Removing folder "!folder!"...
    rmdir /s /q "!folder!"
    echo Folder "!folder!" has been removed.
) else (
    echo Folder "!folder!" does not exist.
)
goto :EOF
