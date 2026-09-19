@echo off
chcp 65001 > nul
title Jubayer Facebook AI Comment Automator
echo =====================================================================
echo    💬 JUBAYER.DEV FACEBOOK AI COMMENT AUTOMATOR (DESKTOP ENGINE)
echo =====================================================================
echo.
echo আপনার ফেসবুক ভিডিও ও পোস্টের নতুন কমেন্ট মনিটর করা হচ্ছে...
echo প্রতিটি কমেন্টে মানুষের মতো স্বাভাবিক গতি ও সেফটি ডিলে সহকারে
echo জেমিনি এআই বুদ্ধিদীপ্ত উত্তর টাইপ করবে এবং টেলিগ্রামে নোটিফিকেশন পাঠাবে।
echo.
echo [1] লাইভ মোডে চালু করতে এন্টার চাপুন
echo [2] পরীক্ষামূলক (Dry-Run) টেস্ট করতে 'test' লিখে এন্টার দিন
set /p MODE="আপনার পছন্দ (Default 1): "

if "%MODE%"=="test" (
    echo.
    echo 🧪 পরীক্ষামূলক টেস্ট মোড চালু হচ্ছে... (কোনো কমেন্ট পোস্ট হবে না)
    python comment_bot/comment_automator.py --dry-run
) else (
    echo.
    echo 🚀 লাইভ অটো-কমেন্ট রিপ্লাই চালু হচ্ছে...
    python comment_bot/comment_automator.py
)

pause
