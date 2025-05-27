import pandas as pd
import streamlit as st

# --- Configuration ---
st.set_page_config(
    page_title='דשבורד עמותת עמותת עמרי למען משפחות השכול',
    layout='wide'
)

# --- File paths ---
main_file   = "omri.xlsx"
widows_file = "almanot.xlsx"

# --- Load widows data ---
almanot = pd.read_excel(widows_file)

# --- Summaries for widows support ---
almanot["סכום חודשי"] = (
    almanot.iloc[:, 6]                   # עמודת סכום חודשי
    .astype(str)
    .str.replace(",", "", regex=False)    # הסרת פסיקים
    .str.extract(r"(\d+\.?\d*)")[0]        # תפיסת המספר
    .astype(float)
    .fillna(0)
)

total_widows = almanot.shape[0]
count_1000   = int((almanot["סכום חודשי"] == 1000).sum())
count_2000   = int((almanot["סכום חודשי"] == 2000).sum())
# --- Compute current support sums ---
current_monthly_support = count_1000 * 1000 + count_2000 * 2000
support_36_months       = current_monthly_support * 36  # 3 שנים

# --- Load financial sheets (עמודות A–C: תאריך, שם, שקלים) ---
exp = pd.read_excel(
    main_file,
    sheet_name="Expenses",
    usecols="A:C",
    names=["תאריך", "שם", "שקלים"],
    header=0
)
don = pd.read_excel(
    main_file,
    sheet_name="Donations",
    usecols="A:C",
    names=["תאריך", "שם", "שקלים"],
    header=0
)
inv = pd.read_excel(
    main_file,
    sheet_name="Investors",
    usecols="A:C",
    names=["תאריך", "שם", "שקלים"],
    header=0
)

# --- Clean & convert ---
for df_sub in (exp, don, inv):
    # המרת למ datetime ואיפוס השעה
    df_sub["תאריך"] = pd.to_datetime(df_sub["תאריך"], dayfirst=True, errors="coerce").dt.normalize()
    # המרת 'שקלים' למספר
    df_sub["שקלים"] = pd.to_numeric(df_sub["שקלים"], errors="coerce").fillna(0)

# --- Compute sums ---
sum_exp   = exp["שקלים"].sum()
sum_don   = don["שקלים"].sum()
sum_inv   = inv["שקלים"].sum()
total_don = sum_don + sum_inv
available = total_don - sum_exp

# --- Prepare monthly donations chart ---
don["month"] = don["תאריך"].dt.to_period("M").dt.to_timestamp()
monthly_don = don.groupby("month")["שקלים"].sum().reset_index()

# --- Streamlit layout ---
st.title("דשבורד עמותת עמותת עמרי למען משפחות השכול")

# Metrics עיקריים
c1, c2, c3 = st.columns(3)
c1.metric("סה״כ תרומות", f"₪{total_don:,.0f}")
c2.metric("סה״כ הוצאות", f"₪{sum_exp:,.0f}")
c3.metric("סכום זמין",   f"₪{available:,.0f}")

st.markdown("---")

# 0) סיכום אלמנות
st.subheader("סיכום אלמנות")
w1, w2, w3, w4 = st.columns(4)
w1.metric("סה״כ אלמנות נתמכות", f"{total_widows}")
w2.metric("אלמנות ב-1,000 ₪", f"{count_1000}")
w3.metric("אלמנות ב-2,000 ₪", f"{count_2000}")
w4.metric("תמיכה חודשית נוכחית (₪)",    f"₪{current_monthly_support:,.0f}")

# טבלת האלמנות
with st.expander("📋 מידע על האלמנות"):
    st.dataframe(almanot)

st.markdown("---")

# טבלאות פירוט (עם תצוגת תאריך ללא שעה)
with st.expander("📋 טבלת הוצאות"):
    exp_disp = exp.copy()
    exp_disp["תאריך"] = exp_disp["תאריך"].dt.strftime("%Y-%m-%d")
    st.dataframe(exp_disp)

with st.expander("📋 טבלת תרומות עיקריות"):
    don_disp = don.copy()
    don_disp["תאריך"] = don_disp["תאריך"].dt.strftime("%Y-%m-%d")
    st.dataframe(don_disp)

with st.expander("📋 טבלת תרומות משקיעים"):
    inv_disp = inv.copy()
    inv_disp["תאריך"] = inv_disp["תאריך"].dt.strftime("%Y-%m-%d")
    st.dataframe(inv_disp)

st.markdown("---")

# גרף תרומות חודשיות
st.subheader("גרף תרומות חודשיות (עיקריות)")
if not monthly_don.empty:
    st.line_chart(
        data=monthly_don.rename(columns={"month": "index", "שקלים": "value"})
                         .set_index("index"),
        height=300
    )
else:
    st.write("אין נתוני תאריך תקינים לתרומות עיקריות.")

# ==== פיצ'ר חישוב אלמנות נוספות (משותף) ====
st.subheader("חישוב הוספת אלמנות נוספות")

col1, col2 = st.columns(2)

with col1:
    n1 = st.slider(
        "מספר אלמנות בקצב תשלום של 1,000 ₪ לחודש",
        min_value=0,
        max_value=int(available / (1000 * 36)) + 10,
        value=0,
        step=1
    )
    req1 = n1 * 1000 * 12 * 3  # שנתיים

with col2:
    n2 = st.slider(
        "מספר אלמנות בקצב תשלום של 2,000 ₪ לחודש",
        min_value=0,
        max_value=int(available / (2000 * 36)) + 10,
        value=0,
        step=1
    )
    req2 = n2 * 2000 * 12 * 3  # שנתיים

# חישוב משותף
total_required = req1 + req2
diff = available - total_required - support_36_months

st.write(f"**דרוש לתקופה (36 חודשים):** ₪{total_required:,.0f}")
st.write(f"**הוצאה שוטפת נוכחית ל-36 חודשים:** ₪{support_36_months:,.0f}")
if diff >= 0:
    st.success(f"**תקציב חופשי שנותר:** ₪{diff:,.0f}")
else:
    st.error(f"**חסר לגייס:** ₪{abs(diff):,.0f}")

st.markdown("""
---
להרצה:
```bash
pip install pandas streamlit  
streamlit run dashboard.py

""")
# --- End of file ---
