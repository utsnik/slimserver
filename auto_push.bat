@echo off
setlocal EnableDelayedExpansion
set LOG_FILE=/tmp/squeezeos_build_fab4.log
set SSH_CMD=ssh -o StrictHostKeyChecking=no -i C:\Users\Igland\.ssh\oracle_key utking@10.1.4.12

echo Waiting for the build to finish...
:loop
%SSH_CMD% "grep 'Tasks Summary: Attempted' %LOG_FILE%" >nul 2>&1
if !errorlevel! equ 0 (
    echo Build finished! Pushing the firmware to the radio...
    call push_fw_to_radio.bat
    goto :done
)

%SSH_CMD% "grep 'Failed tasks' %LOG_FILE%" >nul 2>&1
if !errorlevel! equ 0 (
    echo Build failed. Check the logs.
    goto :done
)

timeout /t 60 >nul
goto :loop

:done
echo Done.
