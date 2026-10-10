@echo off
title Jubayer AI Studio - Local Preview
echo ========================================================
echo   Launching Jubayer AI Studio Website (jubayer.dev)
echo ========================================================
echo Starting local web server on port 8080...
start http://localhost:8080/
python -m http.server 8080
pause
