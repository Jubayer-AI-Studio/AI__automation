@echo off
chcp 65001 > nul
title Facebook Reels & AI Kit Generator
echo ======================================================
echo    ?? Facebook AI Reels & Content Kit Generator
echo ======================================================
echo.
cd /d "%~dp0"
python main.py
echo.
echo ======================================================
echo    ?? ??????? ?????! ????? Telegram ??? ?????
echo ======================================================
pause
