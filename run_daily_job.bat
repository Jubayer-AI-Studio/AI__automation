@echo off
chcp 65001 >nul
cd /d "C:\Users\ASSDI\Desktop\facebook"
python youtube_production\automated_daily_publisher.py >> data\daily_scheduler.log 2>&1
