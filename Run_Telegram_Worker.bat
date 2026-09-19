@echo off
chcp 65001 > nul
title Jubayer Personal AI Telegram Worker
echo =====================================================================
echo    🤖 JUBAYER.DEV PERSONAL AI TELEGRAM WORKER (DESKTOP ENGINE)
echo =====================================================================
echo.
echo টেলিগ্রাম থেকে ভিডিও বা পোস্ট তৈরির রিকোয়েস্ট মনিটর করা হচ্ছে...
echo পিসি চালু থাকা অবস্থায় যেকোনো সময় টেলিগ্রামে 'ভিডিও দাও' লিখলে
echo এখানে স্বয়ংক্রিয়ভাবে ভিডিও তৈরি হয়ে সরাসরি ফোনে চলে যাবে।
echo.
python telegram_assistant_worker.py
pause
