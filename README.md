# מערכת ניהול עמותת עמרי

מערכת ניהול מקיפה לעמותת עמרי המאפשרת ניהול תורמים, אלמנות, הוצאות ותקציב.

## 🚀 Getting Started in 30 Seconds

```bash
# 1. Clone/download the project
# 2. Navigate to project folder
cd Omri-Association

# 3. Run the dashboard (choose one):
./run_dashboard.sh                    # macOS/Linux (recommended)
# OR
python3 -m streamlit run dashboard.py # Direct command

# 4. Open browser to: http://localhost:8501
```

**That's it!** The dashboard will start automatically. 🎉

## תכונות עיקריות

- 📊 **דשבורד אינטראקטיבי** עם סטטיסטיקות בזמן אמת
- 👥 **ניהול תורמים** - מעקב אחר תרומות והיסטוריית תרומות
- 👩 **ניהול אלמנות** - מעקב אחר פרטי אלמנות ותמיכה חודשית
- 💰 **ניהול תקציב** - מעקב אחר הוצאות ותחזיות תקציב
- 📈 **דוחות מתקדמים** - דוחות חודשיים, תורמים ואלמנות
- 🔗 **מפת קשרים** - ויזואליזציה של קשרי תורם-אלמנה
- ⚠️ **התראות חכמות** - התראות על בעיות תקציב ואיכות נתונים

## 🚀 Quick Start (הפעלה מהירה)

### Option 1: Using the Shell Script (Recommended)
```bash
# Make the script executable and run
chmod +x run_dashboard.sh
./run_dashboard.sh
```

### Option 2: Direct Python Command
```bash
python3 -m streamlit run dashboard.py
```

The dashboard will open automatically at **http://localhost:8501**

---

## 📋 Installation & Setup (התקנה והגדרה)

### System Requirements
- Python 3.8+
- Google Cloud Project with Google Sheets API enabled
- Service Account Key from Google Cloud Console

### Install Dependencies
```bash
pip install -r requirements.txt
```

1. **יצירת Google Cloud Project:**
   - עבור ל-[Google Cloud Console](https://console.cloud.google.com/)
   - צור פרויקט חדש או בחר קיים
   - הפעל את Google Sheets API

2. **יצירת Service Account:**
   - עבור ל-IAM & Admin > Service Accounts
   - צור Service Account חדש
   - הורד את קובץ ה-JSON key

3. **הגדרת Spreadsheet:**
   - צור Google Spreadsheet חדש
   - שתף אותו עם כתובת המייל של ה-Service Account (עם הרשאות עריכה)
   - העתק את ה-Spreadsheet ID מה-URL

4. **הגדרת הקבצים:**
   - שמור את קובץ ה-JSON key בשם `service_account.json` בתיקיית הפרויקט
   - עדכן את ה-Spreadsheet ID בקובץ `google_sheets_io.py`

5. **יצירת גיליונות:**
   צור את הגיליונות הבאים ב-Spreadsheet:
   - **Expenses** - הוצאות (עמודות: תאריך, שם, שקלים)
   - **Donations** - תרומות (עמודות: תאריך, שם, שקלים)
   - **Investors** - משקיעים (עמודות: תאריך, שם, שקלים)
   - **Widows** - אלמנות (עמודות: שם, מייל, טלפון, תעודת זהות, מספר ילדים, חודש התחלה, סכום חודשי, חללים, הערות, תורם, איש קשר לתרומה)

### Running the System

#### For macOS/Linux:
```bash
# Option 1: Run full setup + dashboard
./scripts/run_all.sh

# Option 2: Use the legacy shell script
chmod +x run_dashboard.sh
./run_dashboard.sh

# Option 3: Direct command
python3 -m streamlit run dashboard.py
```

#### For Windows:
```bash
# Option 1: Use the batch file
run_dashboard.bat

# Option 2: Direct command
python -m streamlit run dashboard.py
```

### Access the Dashboard
Once running, open your browser and go to: **http://localhost:8501**

### Stop the Dashboard
Press `Ctrl+C` in the terminal where it's running.

## מבנה הפרויקט

```
Omri-Association/
├── dashboard.py              # הקובץ הראשי של הדשבורד
├── google_sheets_io.py       # פונקציות לקריאה וכתיבה ל-Google Sheets
├── data_loading.py           # טעינת נתונים
├── data_processing.py        # עיבוד נתונים וסטטיסטיקות
├── data_visualization.py     # יצירת גרפים וויזואליזציות
├── reports.py                # יצירת דוחות PDF
├── alerts.py                 # מערכת התראות
├── requirements.txt          # תלויות Python
├── service_account.json      # מפתח Google Service Account (לא נכלל ב-Git)
└── README.md                 # קובץ זה
```

## שימוש במערכת

### דף הבית
- סקירה כללית של הסטטיסטיקות
- פעולות מהירות ליצירת דוחות
- התראות על בעיות

### ניהול תקציב
- עריכת הוצאות ותרומות
- תחזיות תקציב ל-36 חודשים
- התראות תקציב

### ניהול תורמים
- מעקב אחר תורמים ותרומות
- סטטיסטיקות תורמים
- היסטוריית תרומות

### ניהול אלמנות
- עריכת פרטי אלמנות
- מעקב אחר תמיכה חודשית
- קשרי תורם-אלמנה

### דוחות
- דוח חודשי מלא
- דוח תורמים
- דוח אלמנות
- דוח תקציב

### מפת קשרים
- ויזואליזציה של קשרי תורם-אלמנה
- עריכת קשרים
- ניתוח קשרים

## 🔧 Troubleshooting (פתרון בעיות)

### Common Issues

#### Port Already in Use
If you see "Port 8501 is already in use":
```bash
# Kill existing Streamlit processes
pkill -f "streamlit run dashboard.py"
# Then run again
./run_dashboard.sh
```

#### Python Version Issues
Make sure you have Python 3.8+:
```bash
python3 --version
# If not found, try:
python --version
```

#### Missing Dependencies
If you get import errors:
```bash
pip install -r requirements.txt
# Or for Python 3:
pip3 install -r requirements.txt
```

#### Permission Denied (macOS/Linux)
```bash
chmod +x run_dashboard.sh
```

### Dashboard Not Loading?
1. Check if Streamlit is running: `ps aux | grep streamlit`
2. Verify the port: `lsof -i :8501`
3. Check browser console for errors
4. Ensure Google Sheets connection is working

---

## 📞 Technical Support

לבעיות טכניות או שאלות, אנא פנה לצוות הפיתוח.

## 📄 License

פרויקט זה מיועד לשימוש פנימי של עמותת עמרי בלבד.
