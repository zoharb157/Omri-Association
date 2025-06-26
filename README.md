# מערכת ניהול עמותת עמרי

מערכת ניהול מקיפה לעמותת עמרי המאפשרת ניהול תורמים, אלמנות, הוצאות ותקציב.

## תכונות עיקריות

- 📊 **דשבורד אינטראקטיבי** עם סטטיסטיקות בזמן אמת
- 👥 **ניהול תורמים** - מעקב אחר תרומות והיסטוריית תרומות
- 👩 **ניהול אלמנות** - מעקב אחר פרטי אלמנות ותמיכה חודשית
- 💰 **ניהול תקציב** - מעקב אחר הוצאות ותחזיות תקציב
- 📈 **דוחות מתקדמים** - דוחות חודשיים, תורמים ואלמנות
- 🔗 **מפת קשרים** - ויזואליזציה של קשרי תורם-אלמנה
- ⚠️ **התראות חכמות** - התראות על בעיות תקציב ואיכות נתונים

## התקנה והפעלה

### דרישות מערכת
- Python 3.8+
- Google Cloud Project עם Google Sheets API מופעל
- Service Account Key מ-Google Cloud Console

### התקנת תלויות
```bash
pip install -r requirements.txt
```

### הגדרת Google Sheets

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

### הפעלת המערכת
```bash
streamlit run dashboard.py
```

או הפעל את הקובץ `run_dashboard.bat` (Windows).

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

## תמיכה טכנית

לבעיות טכניות או שאלות, אנא פנה לצוות הפיתוח.

## רישיון

פרויקט זה מיועד לשימוש פנימי של עמותת עמרי בלבד.
