import pandas as pd
import streamlit as st

st.set_page_config(page_title="דשבורד ועריכת Excel", layout="wide")

st.markdown(
    """
    <style>
    div[data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top left, rgba(78, 84, 200, 0.18), transparent 40%),
                    radial-gradient(circle at bottom right, rgba(13, 202, 240, 0.18), transparent 45%),
                    #f4f6fb;
    }
    div[data-testid="stHeader"] {
        background: transparent;
    }
    .hero {
        background: linear-gradient(135deg, #4e54c8, #0dcaf0);
        padding: 2.75rem 3rem;
        border-radius: 28px;
        color: #ffffff;
        box-shadow: 0 18px 45px rgba(15, 64, 119, 0.3);
        margin-bottom: 2rem;
    }
    .hero h1 {
        font-size: 2.4rem;
        margin-bottom: 0.35rem;
    }
    .hero p {
        font-size: 1.1rem;
        opacity: 0.95;
        margin-bottom: 0.25rem;
    }
    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.88);
        padding: 1.25rem 1.35rem;
        border-radius: 22px;
        box-shadow: 0 12px 38px rgba(15, 64, 119, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.45);
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1f2a44;
    }
    div[data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #41506b;
    }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(78, 84, 200, 0.92), rgba(13, 202, 240, 0.85));
        color: #ffffff;
    }
    div[data-testid="stSidebar"] span,
    div[data-testid="stSidebar"] p,
    div[data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    div[data-testid="stSidebar"] .stButton>button,
    div[data-testid="stSidebar"] .stDownloadButton>button {
        background-color: rgba(255, 255, 255, 0.16);
        color: #ffffff;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.35);
        transition: all 0.2s ease;
    }
    div[data-testid="stSidebar"] .stButton>button:hover,
    div[data-testid="stSidebar"] .stDownloadButton>button:hover {
        background-color: rgba(255, 255, 255, 0.26);
    }
    .editor-wrapper {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 22px;
        padding: 1.2rem;
        box-shadow: 0 12px 40px rgba(15, 64, 119, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.45);
    }
    div[data-testid="stDataFrame"] {
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.45);
        box-shadow: 0 8px 30px rgba(15, 64, 119, 0.08);
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class=\"hero\">
        <h1>דשבורד עמותת עמרי למען משפחות השכול</h1>
        <p>מעקב מרוכז אחר תרומות, הוצאות והתחייבויות לתמיכת אלמנות.</p>
        <p>ערכו את הנתונים, שמרו וחקרו תרחישים בקלות באמצעות הכלים מטה.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

main_file = "omri.xlsx"
widows_file = "almanot.xlsx"


def clean_financial_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "תאריך" in df.columns:
        df["תאריך"] = pd.to_datetime(df["תאריך"], dayfirst=True, errors="coerce").dt.normalize()
    if "שקלים" in df.columns:
        df["שקלים"] = pd.to_numeric(df["שקלים"], errors="coerce").fillna(0.0)
    return df


def clean_widows_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "סכום חודשי" in df.columns:
        cleaned = df["סכום חודשי"].astype(str).str.replace(",", "", regex=False)
        df["סכום חודשי"] = (
            pd.to_numeric(cleaned.str.extract(r"(\d+\.?\d*)")[0], errors="coerce")
            .fillna(0.0)
        )
    return df


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")


def format_currency(value: float) -> str:
    return f"₪{value:,.0f}"


exp = clean_financial_df(
    pd.read_excel(
        main_file,
        sheet_name="Expenses",
        usecols="A:C",
        names=["תאריך", "שם", "שקלים"],
        header=0,
    )
)

don = clean_financial_df(
    pd.read_excel(
        main_file,
        sheet_name="Donations",
        usecols="A:C",
        names=["תאריך", "שם", "שקלים"],
        header=0,
    )
)

inv = clean_financial_df(
    pd.read_excel(
        main_file,
        sheet_name="Investors",
        usecols="A:C",
        names=["תאריך", "שם", "שקלים"],
        header=0,
    )
)

alman = clean_widows_df(pd.read_excel(widows_file))

overview_tab, data_tab, planning_tab = st.tabs([
    "סקירה כללית",
    "עריכת נתונים",
    "תכנון תמיכות",
])

with data_tab:
    st.markdown("### עריכת נתוני המקור")
    st.caption("ערכו את הטבלאות הניהוליות – כל שינוי ישתקף מיד בכל הדשבורד.")

    edit_tabs = st.tabs([
        "הוצאות",
        "תרומות עיקריות",
        "תרומות משקיעים",
        "נתוני אלמנות",
    ])

    with edit_tabs[0]:
        st.markdown("#### הוצאות העמותה")
        exp = st.data_editor(
            exp,
            num_rows="dynamic",
            use_container_width=True,
            key="expenses_editor",
            hide_index=True,
            column_config={
                "תאריך": st.column_config.DateColumn("תאריך", format="DD/MM/YYYY"),
                "שם": st.column_config.TextColumn("שם"),
                "שקלים": st.column_config.NumberColumn("שקלים", format="₪%,d"),
            },
        )
        st.caption("הוסיפו או עדכנו הוצאות. ניתן לייצא את הטבלה מהסרגל הימני.")

    with edit_tabs[1]:
        st.markdown("#### תרומות עיקריות")
        don = st.data_editor(
            don,
            num_rows="dynamic",
            use_container_width=True,
            key="donations_editor",
            hide_index=True,
            column_config={
                "תאריך": st.column_config.DateColumn("תאריך", format="DD/MM/YYYY"),
                "שם": st.column_config.TextColumn("שם"),
                "שקלים": st.column_config.NumberColumn("שקלים", format="₪%,d"),
            },
        )
        st.caption("תרומות מקרן עיקרית או תורמים פרטיים – לעדכון מיידי של הנתונים.")

    with edit_tabs[2]:
        st.markdown("#### תרומות משקיעים")
        inv = st.data_editor(
            inv,
            num_rows="dynamic",
            use_container_width=True,
            key="investors_editor",
            hide_index=True,
            column_config={
                "תאריך": st.column_config.DateColumn("תאריך", format="DD/MM/YYYY"),
                "שם": st.column_config.TextColumn("שם"),
                "שקלים": st.column_config.NumberColumn("שקלים", format="₪%,d"),
            },
        )
        st.caption("תרומות ייעודיות מצד משקיעים ושיתופי פעולה.")

    with edit_tabs[3]:
        st.markdown("#### ניהול אלמנות נתמכות")
        alman = st.data_editor(
            alman,
            num_rows="dynamic",
            use_container_width=True,
            key="widows_editor",
            hide_index=True,
            column_config={
                "סכום חודשי": st.column_config.NumberColumn("סכום חודשי", format="₪%,d"),
            },
        )
        st.caption("נהלו את רשימת המשפחות הנתמכות וערכי התמיכה החודשיים.")

exp = clean_financial_df(exp)
don = clean_financial_df(don)
inv = clean_financial_df(inv)
alman = clean_widows_df(alman)

sum_exp = exp["שקלים"].sum()
sum_don = don["שקלים"].sum()
sum_inv = inv["שקלים"].sum()
total_don = sum_don + sum_inv
available = total_don - sum_exp

if "סכום חודשי" in alman.columns and not alman.empty:
    total_widows = int(alman.shape[0])
    count_1000 = int((alman["סכום חודשי"] == 1000).sum())
    count_2000 = int((alman["סכום חודשי"] == 2000).sum())
    current_monthly_support = float(alman["סכום חודשי"].sum())
    support_36_months = current_monthly_support * 36
else:
    total_widows = count_1000 = count_2000 = 0
    current_monthly_support = support_36_months = 0.0


summary_don = don.dropna(subset=["תאריך"]).copy()
summary_don["month"] = summary_don["תאריך"].dt.to_period("M").dt.to_timestamp()
monthly_don = (
    summary_don.groupby("month")["שקלים"].sum().reset_index(name="תרומות")
    if not summary_don.empty
    else pd.DataFrame(columns=["month", "תרומות"])
)

summary_exp = exp.dropna(subset=["תאריך"]).copy()
summary_exp["month"] = summary_exp["תאריך"].dt.to_period("M").dt.to_timestamp()
monthly_exp = (
    summary_exp.groupby("month")["שקלים"].sum().reset_index(name="הוצאות")
    if not summary_exp.empty
    else pd.DataFrame(columns=["month", "הוצאות"])
)

finance_timeline = pd.merge(monthly_don, monthly_exp, on="month", how="outer").fillna(0.0)
finance_timeline = finance_timeline.sort_values("month")

donors_labeled = don.copy()
donors_labeled["שם"] = donors_labeled["שם"].fillna("לא צויין")
top_donors = (
    donors_labeled.groupby("שם")["שקלים"].sum().reset_index()
    if not donors_labeled.empty
    else pd.DataFrame(columns=["שם", "שקלים"])
)
top_donors = top_donors.sort_values("שקלים", ascending=False).head(10)

recent_expenses = (
    exp.dropna(subset=["תאריך"]).sort_values("תאריך", ascending=False).head(6)
    if not exp.empty
    else pd.DataFrame(columns=exp.columns)
)

recent_donations = (
    don.dropna(subset=["תאריך"]).sort_values("תאריך", ascending=False).head(6)
    if not don.empty
    else pd.DataFrame(columns=don.columns)
)

with st.sidebar:
    st.markdown("### פעולות מהירות")
    st.caption("שמרו את כל השינויים חזרה לקבצי ה-Excel המקומיים.")
    if st.button("💾 שמירת שינויים לקבצים המקוריים", key="save_button"):
        with pd.ExcelWriter(main_file, engine="openpyxl", mode="w") as writer:
            exp.to_excel(writer, sheet_name="Expenses", index=False)
            don.to_excel(writer, sheet_name="Donations", index=False)
            inv.to_excel(writer, sheet_name="Investors", index=False)
        alman.to_excel(widows_file, index=False)
        st.success("השינויים נשמרו בהצלחה.")

    st.markdown("---")
    st.markdown("### מדדי מצב זריזים")
    st.metric("סה״כ תרומות", format_currency(total_don))
    st.metric("סה״כ הוצאות", format_currency(sum_exp))
    st.metric("סכום זמין", format_currency(available))

    st.markdown("---")
    st.markdown("### הורדות CSV מעודכנות")
    st.download_button(
        "📥 הורדת הוצאות",
        data=to_csv_bytes(exp),
        file_name="expenses.csv",
        mime="text/csv",
        key="download_expenses",
    )
    st.download_button(
        "📥 הורדת תרומות עיקריות",
        data=to_csv_bytes(don),
        file_name="donations.csv",
        mime="text/csv",
        key="download_donations",
    )
    st.download_button(
        "📥 הורדת תרומות משקיעים",
        data=to_csv_bytes(inv),
        file_name="investors.csv",
        mime="text/csv",
        key="download_investors",
    )
    st.download_button(
        "📥 הורדת רשימת אלמנות",
        data=to_csv_bytes(alman),
        file_name="widows.csv",
        mime="text/csv",
        key="download_widows",
    )
    st.caption("כל ההורדות כוללות את הנתונים לאחר עדכונים.")

with overview_tab:
    st.markdown("### תמונת מצב נוכחית")
    widows_cols = st.columns(4)
    widows_cols[0].metric("סה״כ אלמנות נתמכות", f"{total_widows}")
    widows_cols[1].metric("אלמנות ב-1,000 ₪", f"{count_1000}")
    widows_cols[2].metric("אלמנות ב-2,000 ₪", f"{count_2000}")
    widows_cols[3].metric("תמיכה חודשית נוכחית", format_currency(current_monthly_support))

    st.markdown("### מדדי כספים")
    finance_cols = st.columns(3)
    finance_cols[0].metric("סה״כ תרומות", format_currency(total_don))
    finance_cols[1].metric("סה״כ הוצאות", format_currency(sum_exp))
    finance_cols[2].metric("יתרת תקציב", format_currency(available))

    st.markdown("### מגמות חודשיות")
    if not finance_timeline.empty:
        chart_df = finance_timeline.set_index("month")[["תרומות", "הוצאות"]]
        chart_df.index.name = "חודש"
        st.line_chart(chart_df)
    else:
        st.info("אין נתונים חודשייים להצגה כרגע.")

    st.markdown("### תורמים מובילים ופעילות עדכנית")
    donors_col, activity_col = st.columns(2)

    with donors_col:
        st.markdown("#### עשרת התורמים המובילים")
        if not top_donors.empty:
            donors_display = top_donors.copy()
            donors_display["שקלים"] = donors_display["שקלים"].map(format_currency)
            donors_display.rename(columns={"שם": "שם התורם", "שקלים": "סכום"}, inplace=True)
            st.dataframe(donors_display, hide_index=True, use_container_width=True)
        else:
            st.caption("אין עדיין נתוני תרומות להצגה.")

    with activity_col:
        st.markdown("#### פעילות כספית אחרונה")
        activity_tabs = st.tabs(["תרומות", "הוצאות"])
        with activity_tabs[0]:
            if not recent_donations.empty:
                donations_display = recent_donations[["תאריך", "שם", "שקלים"]].copy()
                donations_display["תאריך"] = donations_display["תאריך"].dt.strftime("%d/%m/%Y")
                donations_display["שקלים"] = donations_display["שקלים"].map(format_currency)
                donations_display.rename(columns={"שם": "שם התורם"}, inplace=True)
                st.dataframe(donations_display, hide_index=True, use_container_width=True)
            else:
                st.caption("אין תרומות אחרונות להצגה.")
        with activity_tabs[1]:
            if not recent_expenses.empty:
                expenses_display = recent_expenses[["תאריך", "שם", "שקלים"]].copy()
                expenses_display["תאריך"] = expenses_display["תאריך"].dt.strftime("%d/%m/%Y")
                expenses_display["שקלים"] = expenses_display["שקלים"].map(format_currency)
                expenses_display.rename(columns={"שם": "ספק / שימוש"}, inplace=True)
                st.dataframe(expenses_display, hide_index=True, use_container_width=True)
            else:
                st.caption("אין הוצאות אחרונות להצגה.")

with planning_tab:
    st.markdown("### סימולציית תמיכה ל-36 חודשים")
    st.caption("התאימו את מספר המשפחות והבינו כיצד התקציב מושפע בטווח הארוך.")

    base_budget = max(available + support_36_months, 0)
    cost_1000 = 1000 * 36
    cost_2000 = 2000 * 36
    max_1000 = int(base_budget / cost_1000) + 10
    max_2000 = int(base_budget / cost_2000) + 10

    slider_cols = st.columns(2)
    with slider_cols[0]:
        n1 = st.slider(
            "מספר אלמנות ב-1,000 ₪/חודש",
            min_value=0,
            max_value=max_1000,
            value=0,
            step=1,
        )
        req1 = n1 * cost_1000
    with slider_cols[1]:
        n2 = st.slider(
            "מספר אלמנות ב-2,000 ₪/חודש",
            min_value=0,
            max_value=max_2000,
            value=0,
            step=1,
        )
        req2 = n2 * cost_2000

    total_required = req1 + req2
    commitment_total = support_36_months + total_required
    remaining_budget = available - commitment_total

    results_cols = st.columns(3)
    results_cols[0].metric("עלות אלמנות חדשות (36 חוד׳)", format_currency(total_required))
    results_cols[1].metric("התחייבות נוכחית ל-36 חוד׳", format_currency(support_36_months))
    results_cols[2].metric("יתרה לאחר התחייבויות", format_currency(remaining_budget))

    if commitment_total > 0:
        coverage_ratio = max(0.0, min(available / commitment_total, 1.0))
    else:
        coverage_ratio = 1.0
    st.progress(coverage_ratio)
    st.caption(f"כיסוי תקציבי כולל: {coverage_ratio * 100:,.0f}%")

    if remaining_budget >= 0:
        st.success(f"יש תקציב עודף של {format_currency(remaining_budget)} לאחר התחייבויות ל-36 חודשים.")
    else:
        st.error(f"חסר לגייס {format_currency(abs(remaining_budget))} כדי לכסות 36 חודשים של תמיכה.")

    st.caption("החישובים מבוססים על הסכומים שהוזנו ומתעדכנים עם כל שינוי בטבלאות.")
