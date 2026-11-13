@echo off
setlocal EnableExtensions EnableDelayedExpansion
chcp 65001 > nul
title Отцы и дети - установка игры

rem ---------------------------------------------------------------------------
rem Установка на Windows 10 и 11. Нужен только интернет: игра скачивается с
rem GitHub, движок Ren'Py - с renpy.org. Ничего вручную ставить не надо.
rem ---------------------------------------------------------------------------

set "REPO=https://github.com/arekssbit4/otci-i-deti"
set "REPO_ZIP_URL=%REPO%/archive/refs/heads/main.zip"
set "RENPY_VER=8.5.2"
set "SDK_ZIP_URL=https://www.renpy.org/dl/%RENPY_VER%/renpy-%RENPY_VER%-sdk.zip"

set "ROOT=%LOCALAPPDATA%\OtciDeti"
set "SRC=%ROOT%\src"
set "PROJECT=%SRC%\otci-i-deti-main"
set "SDK=%ROOT%\renpy-%RENPY_VER%-sdk"
set "DIST=%ROOT%\dist"

echo ============================================================================
echo    ОТЦЫ И ДЕТИ - визуальная новелла по роману Тургенева
echo ============================================================================
echo    Этот файл сам скачает игру и сделает значок на Рабочем столе.
echo    Всего около 250 МБ, установка занимает 5-10 минут.
echo    Папка установки: %ROOT%
echo ============================================================================
echo.

if not exist "%ROOT%" mkdir "%ROOT%"

call :findexe
if defined EXE (
    echo Игра уже установлена - проверяю только значок.
    echo.
    goto shortcut
)

echo [1/4] Скачиваю игру с GitHub, около 85 МБ...
echo.
call :download "%REPO_ZIP_URL%" "%ROOT%\igra.zip"
if errorlevel 1 goto failed
echo.
echo       Распаковываю...
if exist "%PROJECT%" rmdir /s /q "%PROJECT%"
call :extract "%ROOT%\igra.zip" "%SRC%"
if errorlevel 1 goto failed
del "%ROOT%\igra.zip"
if not exist "%PROJECT%\game\script.rpy" (
    echo.
    echo   Не нашёл файлы игры после распаковки - попробуйте запустить файл ещё раз.
    goto failed
)
echo.

echo [2/4] Проверяю движок Ren'Py...
if exist "%SDK%\renpy.exe" (
    echo       Он уже есть, качать не нужно.
    echo.
    goto build
)
echo       Скачиваю Ren'Py %RENPY_VER%, около 160 МБ...
echo.
call :download "%SDK_ZIP_URL%" "%ROOT%\renpy.zip"
if errorlevel 1 goto failed
echo.
echo       Распаковываю...
call :extract "%ROOT%\renpy.zip" "%ROOT%"
if errorlevel 1 goto failed
del "%ROOT%\renpy.zip"
if not exist "%SDK%\renpy.exe" (
    echo.
    echo   Не нашёл renpy.exe после распаковки - попробуйте запустить файл ещё раз.
    goto failed
)
echo.

:build
echo [3/4] Собираю запуск игры, это 1-3 минуты...
echo.
"%SDK%\renpy.exe" "%SDK%\launcher" distribute "%PROJECT%" --package win --no-update --destination "%DIST%"
if errorlevel 1 echo       Ren'Py сообщил ошибку, но проверю результат.
set "GAME_ZIP="
for %%F in ("%DIST%\OtciDetiAlpha-*-win.zip") do set "GAME_ZIP=%%F"
if not defined GAME_ZIP (
    echo.
    echo   Сборка не получилась: Ren'Py не создал архив игры.
    echo   Скиньте текст выше разработчику и запустите файл ещё раз.
    goto failed
)
echo.
echo       Раскладываю собранную игру по папке...
call :extract "!GAME_ZIP!" "%DIST%"
if errorlevel 1 goto failed
del "!GAME_ZIP!"
call :findexe
if not defined EXE (
    echo.
    echo   Сборка не получилась: в архиве нет OtciDetiAlpha.exe.
    echo   Скиньте текст выше разработчику и запустите файл ещё раз.
    goto failed
)
echo.

:shortcut
echo [4/4] Ставлю значок на Рабочий стол...
set "DESKTOP=%USERPROFILE%\Desktop"
for /f "usebackq delims=" %%D in (`powershell -NoProfile -Command "[Environment]::GetFolderPath('Desktop')"`) do set "DESKTOP=%%D"
powershell -NoProfile -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut('!DESKTOP!\Отцы и дети.lnk'); $s.TargetPath='!EXE!'; $s.WorkingDirectory=(Split-Path '!EXE!'); $s.Description='Отцы и дети - визуальная новелла'; $s.Save()"
if not exist "!DESKTOP!\Отцы и дети.lnk" (
    echo.
    echo   Значок не получился, но игра установлена - файл вот здесь:
    echo   !EXE!
)
echo.

echo ============================================================================
echo   Готово. Экран игры "Отцы и дети" лежит на Рабочем столе - это обычный
echo   .exe, запускается двойным щелчком мыши.
echo ============================================================================
echo.

set "OTVET=n"
set /p OTVET=Запустить игру сейчас? (y/n):
if /i "!OTVET!"=="y" (
    start "" "!EXE!"
    echo.
    echo   Игра запущена. Хорошего чтения.
) else (
    echo.
    echo   Не запускаю. Игру всегда можно открыть с Рабочего стола -
    echo   значок "Отцы и дети".
)
timeout /t 6 /nobreak > nul
exit /b 0

rem ---------------------------------------------------------------------------
rem :findexe - находит собранный exe в папке dist (имя зависит от версии игры)
rem ---------------------------------------------------------------------------
:findexe
set "EXE="
for %%F in ("%DIST%\OtciDetiAlpha-*-win\OtciDetiAlpha.exe") do set "EXE=%%~fF"
exit /b 0

rem ---------------------------------------------------------------------------
rem :download <url> <файл> - качает с прогрессом в этом окне
rem Системный curl, если его нет (Windows старше 1806) - PowerShell.
rem ---------------------------------------------------------------------------
:download
if exist "%~2" del "%~2"
set "CURL=%SystemRoot%\System32\curl.exe"
if exist "!CURL!" (
    "!CURL!" --fail --location --retry 3 --progress-bar -o "%~2" "%~1"
    if errorlevel 1 exit /b 1
) else (
    powershell -NoProfile -Command "Invoke-WebRequest -Uri '%~1' -OutFile '%~2'"
    if errorlevel 1 exit /b 1
)
if not exist "%~2" exit /b 1
exit /b 0

rem ---------------------------------------------------------------------------
rem :extract <архив> <папка> - распаковывает zip
rem Берётся именно системный tar (быстрый), а не тот, что кладёт в PATH Git или
rem 7-Zip: у них другие правила для путей вида C:\.
rem ---------------------------------------------------------------------------
:extract
if not exist "%~2" mkdir "%~2"
set "TAR=%SystemRoot%\System32\tar.exe"
if exist "!TAR!" (
    "!TAR!" -xf "%~1" -C "%~2"
    if errorlevel 1 exit /b 1
) else (
    powershell -NoProfile -Command "Expand-Archive -LiteralPath '%~1' -DestinationPath '%~2' -Force"
    if errorlevel 1 exit /b 1
)
exit /b 0

:failed
echo.
echo   Установка не закончилась. Проверьте интернет и запустите файл ещё раз -
echo   он продолжит с того места, где остановился.
echo.
pause
exit /b 1
