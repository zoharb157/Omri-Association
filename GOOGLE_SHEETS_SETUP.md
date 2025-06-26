# מדריך השלמת המעבר ל-Google Sheets

## סטטוס נוכחי

✅ **הושלם:**
- עדכון Spreadsheet ID: `1zo3Rnmmykvd55owzQyGPSjx6cYfy4SB3SZc-Ku7UcOo`
- החלפת קריאות Excel בפונקציות Google Sheets ב-`data_loading.py`
- החלפת קריאות Excel בפונקציות Google Sheets ב-`dashboard.py`
- הוספת תלויות Google Sheets ל-`requirements.txt`
- עדכון ה-README עם הוראות

⏳ **נדרש להשלמה:**

## שלב 1: יצירת Google Cloud Project

1. עבור ל-[Google Cloud Console](https://console.cloud.google.com/)
2. צור פרויקט חדש או בחר פרויקט קיים
3. הפעל את Google Sheets API:
   - עבור ל-APIs & Services > Library
   - חפש "Google Sheets API"
   - לחץ על "Enable"

## שלב 2: יצירת Service Account

1. עבור ל-IAM & Admin > Service Accounts
2. לחץ על "Create Service Account"
3. תן שם: `omri-association-sheets`
4. לחץ על "Create and Continue"
5. תן הרשאות: `Editor`
6. לחץ על "Done"
7. לחץ על Service Account שיצרת
8. עבור לטאב "Keys"
9. לחץ על "Add Key" > "Create new key"
10. בחר JSON
11. הורד את הקובץ

## שלב 3: הגדרת Spreadsheet

1. צור Google Spreadsheet חדש
2. שתף אותו עם כתובת המייל של ה-Service Account (מהקובץ JSON)
3. תן הרשאות עריכה
4. העתק את ה-Spreadsheet ID מה-URL (כבר קיים: `1zo3Rnmmykvd55owzQyGPSjx6cYfy4SB3SZc-Ku7UcOo`)

## שלב 4: יצירת גיליונות

צור את הגיליונות הבאים ב-Spreadsheet:

### גיליון Expenses
עמודות:
- תאריך
- שם  
- שקלים

### גיליון Donations
עמודות:
- תאריך
- שם
- שקלים

### גיליון Investors
עמודות:
- תאריך
- שם
- שקלים

### גיליון Widows
עמודות:
- שם
- מייל
- טלפון
- תעודת זהות
- מספר ילדים
- חודש התחלה
- סכום חודשי
- חללים
- הערות
- תורם
- איש קשר לתרומה

## שלב 5: הגדרת הקבצים

1. שמור את קובץ ה-JSON key בשם `service_account.json` בתיקיית הפרויקט
2. וודא שה-Spreadsheet ID מעודכן ב-`google_sheets_io.py` (כבר מעודכן)

## שלב 6: התקנת תלויות

```bash
pip install gspread google-auth
```

או:

```bash
pip install -r requirements.txt
```

## שלב 7: העברת נתונים

אם יש לך נתונים קיימים ב-Excel, העבר אותם ל-Google Sheets:

1. פתח את הקבצים `omri.xlsx` ו-`almanot.xlsx`
2. העתק את הנתונים לגיליונות המתאימים ב-Google Sheets
3. וודא שעמודות התואמות לעמודות שהוגדרו למעלה

## שלב 8: בדיקה

1. הפעל את המערכת:
```bash
streamlit run dashboard.py
```

2. בדוק שהנתונים נטענים מ-Google Sheets
3. בדוק שניתן לערוך ולשמור נתונים
4. בדוק שכל הפונקציות עובדות כראוי

## פתרון בעיות

### שגיאה: "Service account file not found"
- וודא שקובץ `service_account.json` נמצא בתיקיית הפרויקט

### שגיאה: "Spreadsheet not found"
- וודא שה-Spreadsheet ID נכון
- וודא שה-Service Account יש לו הרשאות עריכה

### שגיאה: "Sheet not found"
- וודא ששמות הגיליונות תואמים: Expenses, Donations, Investors, Widows

### שגיאה: "Permission denied"
- וודא שה-Service Account יש לו הרשאות עריכה ב-Spreadsheet

## הערות חשובות

1. **גיבוי:** מומלץ ליצור גיבוי של הנתונים לפני המעבר
2. **בדיקה:** בדוק את המערכת בסביבת פיתוח לפני הפעלה בסביבת ייצור
3. **הרשאות:** וודא שה-Service Account יש לו רק את ההרשאות הנדרשות
4. **ביטחון:** אל תעלה את קובץ `service_account.json` ל-Git

## תמיכה

לבעיות טכניות, אנא פנה לצוות הפיתוח עם:
- הודעת השגיאה המלאה
- לוגים מהמערכת
- תיאור הבעיה 