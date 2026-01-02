@echo off
set SCRIPT_DIR=%~dp0
cd %SCRIPT_DIR%

CALL env.bat

REM Assign the value random password to the password variable
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION
set alfanum=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
set rustdesk_pw=
for /L %%b in (1, 1, 12) do (
    set /A rnd_num=!RANDOM! %% 62
    for %%c in (!rnd_num!) do (
        set rustdesk_pw=!rustdesk_pw!!alfanum:~%%c,1!
    )
)

rustdesk-1.4.4-x86_64.exe --silent-install
timeout /t 20

cd "C:\Program Files\RustDesk\"
rustdesk.exe --install-service
timeout /t 20

for /f "delims=" %%i in ('rustdesk.exe --get-id ^| more') do set rustdesk_id=%%i

rustdesk.exe --config "host=%HOST%,key=%KEY%"

rustdesk.exe --password %rustdesk_pw%

cd %SCRIPT_DIR%

echo ............................................... >> credentials.txt
REM Show the value of the ID Variable
echo RustDesk ID: %rustdesk_id% >> credentials.txt

REM Show the value of the Password Variable
echo Password: %rustdesk_pw% >> credentials.txt
echo ............................................... >> credentials.txt