@echo off
echo ================================
echo בדיקת התקנת Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python לא מותקן במחשב זה.
    echo נא להוריד ולהתקין Python מהאתר: https://www.python.org/downloads/
    pause
    exit
)

echo ================================
echo בדיקת התקנת pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo pip לא מותקן. מנסה להתקין pip...
    python -m ensurepip
)

echo ================================
echo התקנת כל התלויות...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo ================================
echo הפעלת הדשבורד...
start http://localhost:8501
streamlit run dashboard.py

pause 