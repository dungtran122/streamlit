@echo off
cd /d "%~dp0"

echo ==================================================
echo        DANG KHOI DONG PHAN MEM...
echo ==================================================

:: Chạy Streamlit từ bộ Python Portable
.\python\python.exe -m streamlit run app.py --global.developmentMode=false

pause