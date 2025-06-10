import pandas as pd
import streamlit as st
from io import BytesIO

# --- Configuration ---
st.set_page_config(page_title='דשבורד ועריכת Excel', layout='wide')
st.title("דשבורד עמותת עמותת עמרי למען משפחות השכול")

# --- File paths ---
main_file   = "omri.xlsx"
widows_file = "almanot.xlsx"

# --- Load initial data ---
exp   = pd.read_excel(main_file, sheet_name="Expenses",   usecols="A:C", names=["תאריך","שם","שקלים"], header=0)
don   = pd.read_excel(main_file, sheet_name="Donations",  usecols="A:C", names=["תאריך","שם","שקלים"], header=0)
inv   = pd.read_excel(main_file, sheet_name="Investors",  usecols="A:C", names=["תאריך","שם","שקלים"], header=0)
alman = pd.read_excel(widows_file)

# --- Clean & convert columns ---
for df in (exp, don, inv):
    df["תאריך"] = pd.to_datetime(df["תאריך"], dayfirst=True, errors="coerce").dt.normalize()
    df["שקלים"] = pd.to_numeric(df["שקלים"], errors="coerce").fillna(0)

if "סכום חודשי" in alman.columns:
    alman["סכום חודשי"] = (
        alman["סכום חודשי"].astype(str)
        .str.replace(",", "", regex=False)
        .str.extract(r"(\d+\.?\d*)")[0]
        .astype(float)
        .fillna(0)
    )

# --- Editable tables on the main page ---
st.markdown("## עריכת טבלאות מקוריות")
with st.expander("📋 עריכת הוצאות"):
    exp = st.data_editor(exp, num_rows="dynamic")
with st.expander("📋 עריכת תרומות עיקריות"):
    don = st.data_editor(don, num_rows="dynamic")
with st.expander("📋 עריכת תרומות משקיעים"):
    inv = st.data_editor(inv, num_rows="dynamic")
with st.expander("📋 עריכת מידע על אלמנות"):
    alman = st.data_editor(alman, num_rows="dynamic")

# --- Sidebar: Save edits back to original files ---
st.sidebar.header("שמירה ישירה של השינויים")
if st.sidebar.button("שמור שינויים לקבצים המקוריים"):
    with pd.ExcelWriter(main_file, engine="openpyxl", mode="w") as writer:
        exp.to_excel(writer, sheet_name="Expenses", index=False)
        don.to_excel(writer, sheet_name="Donations", index=False)
        inv.to_excel(writer, sheet_name="Investors", index=False)
    alman.to_excel(widows_file, index=False)
    st.sidebar.success("השינויים נשמרו ישירות לקבצים המקוריים!")

# --- Dashboard calculations with possibly edited data ---
sum_exp = exp["שקלים"].sum()
sum_don = don["שקלים"].sum()
sum_inv = inv["שקלים"].sum()
total_don = sum_don + sum_inv
available = total_don - sum_exp

# Monthly donations chart
don["month"] = don["תאריך"].dt.to_period("M").dt.to_timestamp()
monthly_don = don.groupby("month")["שקלים"].sum().reset_index()

# Widows summary
if "סכום חודשי" in alman.columns:
    total_widows = alman.shape[0]
    count_1000 = int((alman["סכום חודשי"] == 1000).sum())
    count_2000 = int((alman["סכום חודשי"] == 2000).sum())
    current_monthly_support = count_1000 * 1000 + count_2000 * 2000
    support_36_months = current_monthly_support * 36
else:
    total_widows = count_1000 = count_2000 = current_monthly_support = support_36_months = 0

# --- Display metrics ---
st.markdown("---")
st.subheader("סיכום אלמנות")
w1, w2, w3, w4 = st.columns(4)
w1.metric("סה״כ אלמנות נתמכות",    f"{total_widows}")
w2.metric("אלמנות ב-1,000 ₪",        f"{count_1000}")
w3.metric("אלמנות ב-2,000 ₪",        f"{count_2000}")
w4.metric("תמיכה חודשית נוכחית",     f"₪{current_monthly_support:,.0f}")

st.markdown("---")
st.subheader("עיקרי כספים")
c1, c2, c3 = st.columns(3)
c1.metric("סה״כ תרומות", f"₪{total_don:,.0f}")
c2.metric("סה״כ הוצאות", f"₪{sum_exp:,.0f}")
c3.metric("סכום זמין",   f"₪{available:,.0f}")

st.markdown("---")
st.subheader("גרף תרומות חודשיות (עיקריות)")
if not monthly_don.empty:
    st.line_chart(monthly_don.rename(columns={"month":"index","שקלים":"value"}).set_index("index"))
else:
    st.write("אין נתוני תאריך תקינים לתרומות עיקריות.")

# ==== פיצ'ר חישוב אלמנות נוספות (36 חודשים) ====
st.markdown("---")
st.subheader("חישוב הוספת אלמנות נוספות (36 חודשים)")
col1, col2 = st.columns(2)
with col1:
    n1 = st.slider(
        "מספר אלמנות ב-1,000 ₪/חודש",
        min_value=0,
        max_value=int((available + support_36_months) / (1000 * 36)) + 10,
        value=0, step=1
    )
    req1 = n1 * 1000 * 12 * 3
with col2:
    n2 = st.slider(
        "מספר אלמנות ב-2,000 ₪/חודש",
        min_value=0,
        max_value=int((available + support_36_months) / (2000 * 36)) + 10,
        value=0, step=1
    )
    req2 = n2 * 2000 * 12 * 3

# חישוב משותף
total_required = req1 + req2
diff = available - total_required - support_36_months

st.write(f"**דרוש לתקופה (36 חודשים):** ₪{total_required:,.0f}")
st.write(f"**הוצאה שוטפת נוכחית ל-36 חודשים:** ₪{support_36_months:,.0f}")
if diff >= 0:
    st.success(f"**תקציב חופשי שנותר:** ₪{diff:,.0f}")
else:
    st.error(f"**חסר לגייס:** ₪{abs(diff):,.0f}")