@echo off
chcp 65001 > nul
title Create Reel With My Real Voice
echo ======================================================
echo    🎙️ Personal Voice Facebook Reels Generator
echo ======================================================
echo.
cd /d "%~dp0"
python telegram_voice_bot.py
echo.
echo ======================================================
echo    🎉 সম্পন্ন হয়েছে! ফোনের Telegram চেক করুন।
echo ======================================================
pause

