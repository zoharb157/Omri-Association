import altair as alt
import pandas as pd
import streamlit as st
from io import BytesIO

# --- Configuration & Styling ---
st.set_page_config(page_title="דשבורד ועריכת Excel", page_icon="📊", layout="wide")

CUSTOM_STYLE = """
<style>
:root {
    --primary-color: #1E88E5;
    --success-color: #2E7D32;
    --danger-color: #C62828;
    --warning-color: #F9A825;
    --surface-color: #ffffff;
}
.stApp {
    background: linear-gradient(180deg, rgba(241,245,249,0.95) 0%, #ffffff 100%);
}
.block-container {
    padding-top: 2.5rem;
}
.metric-card {
    border-radius: 22px;
    padding: 1.4rem 1.6rem;
    color: #ffffff;
    display: flex;
    gap: 1.1rem;
    align-items: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 18px 35px rgba(15, 23, 42, 0.12);
    min-height: 128px;
}
.metric-card .metric-icon {
    font-size: 2.6rem;
    line-height: 1;
}
.metric-card .metric-content {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
}
.metric-card .metric-title {
    font-size: 0.95rem;
    font-weight: 500;
    opacity: 0.85;
}
.metric-card .metric-value {
    font-size: 1.85rem;
    font-weight: 700;
}
.metric-card .metric-subtitle {
    font-size: 0.85rem;
    opacity: 0.8;
}
.metric-card.light {
    color: #1f2937;
    background: linear-gradient(135deg, #fff7e6 0%, #ffe0b2 100%);
    box-shadow: 0 15px 28px rgba(250, 179, 0, 0.25);
}
.metric-card.success {
    background: linear-gradient(135deg, #43a047 0%, #2e7d32 100%);
}
.metric-card.warning {
    background: linear-gradient(135deg, #fdd835 0%, #f9a825 100%);
    color: #1f2937;
}
.metric-card.danger {
    background: linear-gradient(135deg, #ef5350 0%, #c62828 100%);
}
.metric-card.primary {
    background: linear-gradient(135deg, #1e88e5 0%, #42a5f5 100%);
}
.stTabs [data-baseweb="tab-list"] {
    gap: 0.6rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 999px;
    padding: 0.6rem 1.4rem;
    font-weight: 600;
    background-color: rgba(30,136,229,0.08);
    color: #1f2937;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: #ffffff;
    background: linear-gradient(135deg, #1e88e5 0%, #42a5f5 100%);
    box-shadow: 0 14px 30px rgba(30, 136, 229, 0.25);
}
</style>
"""
st.markdown(CUSTOM_STYLE, unsafe_allow_html=True)

st.title("דשבורד עמותת עמרי למען משפחות השכול")
st.caption("התעדכנות מהירה, עריכת נתונים וחישובי תמיכה ארוכי טווח במקום אחד.")

# --- File paths ---
main_file = "omri.xlsx"
widows_file = "almanot.xlsx"


# --- Helper functions ---
def clean_finance_df(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    if "תאריך" in cleaned.columns:
        cleaned["תאריך"] = pd.to_datetime(cleaned["תאריך"], dayfirst=True, errors="coerce").dt.normalize()
    if "שקלים" in cleaned.columns:
        cleaned["שקלים"] = pd.to_numeric(cleaned["שקלים"], errors="coerce").fillna(0)
    return cleaned


def clean_widows_df(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    if "סכום חודשי" in cleaned.columns:
        cleaned["סכום חודשי"] = (
            cleaned["סכום חודשי"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.extract(r"(\d+\.?\d*)")[0]
            .astype(float)
            .fillna(0)
        )
    return cleaned


def format_currency(value: float, decimals: int = 0) -> str:
    return f"₪{value:,.{decimals}f}"


def metric_card(title: str, value: str, subtitle: str = "", icon: str = "ℹ️", variant: str = "primary") -> None:
    st.markdown(
        f"""
        <div class="metric-card {variant}">
            <div class="metric-icon">{icon}</div>
            <div class="metric-content">
                <span class="metric-title">{title}</span>
                <span class="metric-value">{value}</span>
                <span class="metric-subtitle">{subtitle}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_export_workbook(
    exp_df: pd.DataFrame, don_df: pd.DataFrame, inv_df: pd.DataFrame, alman_df: pd.DataFrame
) -> BytesIO:
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        exp_df.to_excel(writer, sheet_name="Expenses", index=False)
        don_df.to_excel(writer, sheet_name="Donations", index=False)
        inv_df.to_excel(writer, sheet_name="Investors", index=False)
        alman_df.to_excel(writer, sheet_name="Widows", index=False)
    buffer.seek(0)
    return buffer


# --- Load and prepare data ---
exp = pd.read_excel(
    main_file,
    sheet_name="Expenses",
    usecols="A:C",
    names=["תאריך", "שם", "שקלים"],
    header=0,
)
don = pd.read_excel(
    main_file,
    sheet_name="Donations",
    usecols="A:C",
    names=["תאריך", "שם", "שקלים"],
    header=0,
)
inv = pd.read_excel(
    main_file,
    sheet_name="Investors",
    usecols="A:C",
    names=["תאריך", "שם", "שקלים"],
    header=0,
)
alman = pd.read_excel(widows_file)

exp = clean_finance_df(exp)
don = clean_finance_df(don)
inv = clean_finance_df(inv)
alman = clean_widows_df(alman)

overview_tab, analytics_tab, editing_tab, planning_tab = st.tabs(
    [
        "🔎 מבט על הארגון",
        "📈 ניתוח נתונים ותרשימים",
        "✏️ עריכת נתונים",
        "🧮 תכנון תמיכה עתידי",
    ]
)

with editing_tab:
    st.markdown("### עריכת טבלאות המקור")
    st.write("כל שינוי נשמר בזיכרון המערכת עד ללחיצה על כפתור השמירה בצד שמאל או הורדת קובץ חדש.")
    editor_tabs = st.tabs(
        [
            "הוצאות",
            "תרומות עיקריות",
            "תרומות משקיעים",
            "מידע על אלמנות",
        ]
    )
    finance_column_config = {
        "תאריך": st.column_config.DateColumn("תאריך"),
        "שקלים": st.column_config.NumberColumn("שקלים", format="₪%0.0f", step=100),
    }
    with editor_tabs[0]:
        exp = st.data_editor(
            exp,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            column_config=finance_column_config,
            key="expenses_editor",
        )
    with editor_tabs[1]:
        don = st.data_editor(
            don,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            column_config=finance_column_config,
            key="donations_editor",
        )
    with editor_tabs[2]:
        inv = st.data_editor(
            inv,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            column_config=finance_column_config,
            key="investors_editor",
        )
    with editor_tabs[3]:
        widows_config = {}
        if "סכום חודשי" in alman.columns:
            widows_config["סכום חודשי"] = st.column_config.NumberColumn(
                "סכום חודשי", format="₪%0.0f", step=100
            )
        alman = st.data_editor(
            alman,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            column_config=widows_config,
            key="widows_editor",
        )
    st.info("לא לשכוח לשמור או להוריד קובץ חדש לאחר סיום העריכה.")

exp = clean_finance_df(exp)
don = clean_finance_df(don)
inv = clean_finance_df(inv)
alman = clean_widows_df(alman)

# --- Calculations ---
sum_exp = float(exp["שקלים"].sum())
sum_don = float(don["שקלים"].sum())
sum_inv = float(inv["שקלים"].sum())
total_don = sum_don + sum_inv
available = total_don - sum_exp

# Prepare monthly analytics
don_analytics = don.dropna(subset=["תאריך"]).copy()
inv_analytics = inv.dropna(subset=["תאריך"]).copy()
exp_analytics = exp.dropna(subset=["תאריך"]).copy()

for frame in (don_analytics, inv_analytics, exp_analytics):
    frame["month"] = frame["תאריך"].dt.to_period("M").dt.to_timestamp()

monthly_don = don_analytics.groupby("month")["שקלים"].sum().reset_index()
monthly_inv = inv_analytics.groupby("month")["שקלים"].sum().reset_index()
monthly_exp = exp_analytics.groupby("month")["שקלים"].sum().reset_index()

monthly_summary = (
    monthly_don.rename(columns={"שקלים": "תרומות עיקריות"})
    .merge(monthly_inv.rename(columns={"שקלים": "תרומות משקיעים"}), on="month", how="outer")
    .merge(monthly_exp.rename(columns={"שקלים": "הוצאות"}), on="month", how="outer")
    .fillna(0)
    .sort_values("month")
)
if not monthly_summary.empty:
    monthly_summary["סה\"כ הכנסות"] = (
        monthly_summary["תרומות עיקריות"] + monthly_summary["תרומות משקיעים"]
    )
    monthly_summary["יתרה"] = monthly_summary["סה\"כ הכנסות"] - monthly_summary["הוצאות"]

# Widows summary
if "סכום חודשי" in alman.columns:
    total_widows = int(alman.shape[0])
    widows_distribution = (
        alman.groupby("סכום חודשי")
        .size()
        .reset_index(name="מספר אלמנות")
        .sort_values("סכום חודשי")
    )
    count_1000 = int((alman["סכום חודשי"] == 1000).sum())
    count_2000 = int((alman["סכום חודשי"] == 2000).sum())
    current_monthly_support = float(alman["סכום חודשי"].sum())
    support_36_months = current_monthly_support * 36
else:
    total_widows = 0
    widows_distribution = pd.DataFrame(columns=["סכום חודשי", "מספר אלמנות"])
    count_1000 = count_2000 = 0
    current_monthly_support = support_36_months = 0.0

# --- Sidebar actions ---
st.sidebar.header("פעולות מהירות")
st.sidebar.caption("השינויים נשמרים לקבצים או ניתנים להורדה כאקסל חדש.")
if st.sidebar.button("שמור שינויים לקבצים המקוריים", use_container_width=True):
    with pd.ExcelWriter(main_file, engine="openpyxl", mode="w") as writer:
        exp.to_excel(writer, sheet_name="Expenses", index=False)
        don.to_excel(writer, sheet_name="Donations", index=False)
        inv.to_excel(writer, sheet_name="Investors", index=False)
    alman.to_excel(widows_file, index=False)
    st.sidebar.success("השינויים נשמרו בהצלחה לקבצים המקוריים!")

export_buffer = build_export_workbook(exp, don, inv, alman)
st.sidebar.download_button(
    "הורד קובץ אקסל מעודכן",
    data=export_buffer,
    file_name="omri_dashboard_export.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True,
)
st.sidebar.markdown("---")
st.sidebar.metric("סכום זמין", format_currency(available))
st.sidebar.metric("סה\"כ תרומות", format_currency(total_don))
st.sidebar.metric("סה\"כ הוצאות", format_currency(sum_exp))
st.sidebar.metric("תמיכה חודשית קיימת", format_currency(current_monthly_support))


with overview_tab:
    st.subheader("תמונת מצב פיננסית")
    col1, col2, col3, col4 = st.columns(4, gap="large")
    with col1:
        metric_card("סה\"כ תרומות", format_currency(total_don), "כולל תרומות משקיעים", "💙", "primary")
    with col2:
        metric_card("סה\"כ הוצאות", format_currency(sum_exp), "על סמך הנתונים המעודכנים", "🧾", "danger")
    with col3:
        metric_card("יתרה זמינה", format_currency(available), "לאחר קיזוז הוצאות", "🏦", "success")
    coverage_ratio = total_don / sum_exp if sum_exp else None
    coverage_value = f"{coverage_ratio:.1f}x" if coverage_ratio else "—"
    with col4:
        metric_card("יחס כיסוי תרומות", coverage_value, "הכנסות חלקי הוצאות", "⚖️", "warning")

    st.subheader("תמיכה באלמנות")
    colw1, colw2, colw3, colw4 = st.columns(4, gap="large")
    with colw1:
        metric_card("סה\"כ אלמנות נתמכות", f"{total_widows}", "סכום כולל של כל הרמות", "👩‍👧", "light")
    with colw2:
        metric_card("אלמנות ב-1,000 ₪", f"{count_1000}", "עלות חודשית ₪1,000 לאלמנה", "1️⃣", "light")
    with colw3:
        metric_card("אלמנות ב-2,000 ₪", f"{count_2000}", "עלות חודשית ₪2,000 לאלמנה", "2️⃣", "light")
    with colw4:
        metric_card(
            "תמיכה חודשית נוכחית",
            format_currency(current_monthly_support),
            "כלל ההתחייבויות הקיימות",
            "💛",
            "light",
        )

    st.markdown("#### חלוקת התמיכה החודשית")
    if not widows_distribution.empty:
        distribution_display = widows_distribution.copy()
        distribution_display["חלק יחסי"] = (
            distribution_display["מספר אלמנות"] / distribution_display["מספר אלמנות"].sum()
        )
        distribution_display["סכום חודשי"] = distribution_display["סכום חודשי"].apply(format_currency)
        distribution_display["חלק יחסי"] = distribution_display["חלק יחסי"].map(lambda v: f"{v:.0%}")
        st.dataframe(
            distribution_display.rename(
                columns={"סכום חודשי": "רמת תמיכה", "מספר אלמנות": "מספר", "חלק יחסי": "אחוז"}
            ),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("אין נתונים להצגת חלוקת תמיכה.")

    st.markdown("#### התחייבויות קיימות ל-36 חודשים")
    if support_36_months > 0 or available > 0:
        total_capacity = support_36_months + max(available, 0)
        progress_value = min(max(support_36_months / total_capacity if total_capacity else 0, 0), 1)
        st.progress(progress_value)
        st.caption(
            f"התחייבות נוכחית: {format_currency(support_36_months)} ל-36 חודשים | יתרה זמינה: {format_currency(available)}"
        )
    else:
        st.info("לא הוזנו נתונים לחישוב התחייבויות.")


with analytics_tab:
    st.subheader("מגמות הכנסה והוצאה חודשיות")
    if not monthly_summary.empty:
        chart_source = monthly_summary.melt(
            id_vars="month",
            value_vars=["תרומות עיקריות", "תרומות משקיעים", "הוצאות"],
            var_name="סוג",
            value_name="שקלים",
        )
        chart = (
            alt.Chart(chart_source)
            .mark_line(point=True)
            .encode(
                x=alt.X("month:T", title="חודש", axis=alt.Axis(format="%Y-%m")),
                y=alt.Y("שקלים:Q", title="סכום (₪)"),
                color=alt.Color("סוג:N", title=""),
                tooltip=[
                    alt.Tooltip("month:T", title="חודש", format="%Y-%m"),
                    alt.Tooltip("סוג:N", title="קטגוריה"),
                    alt.Tooltip("שקלים:Q", title="סכום", format=",.0f"),
                ],
            )
            .properties(height=360)
        )
        st.altair_chart(chart, use_container_width=True)

        summary_display = monthly_summary.copy()
        summary_display["חודש"] = summary_display["month"].dt.strftime("%Y-%m")
        summary_display = summary_display.drop(columns="month").set_index("חודש")
        st.dataframe(
            summary_display.style.format(format_currency),
            use_container_width=True,
        )
    else:
        st.info("אין נתוני תאריך מספקים להציג מגמות חודשיות.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("##### תומכים מובילים")
        supporters = pd.concat(
            [
                don.assign(מקור="תרומה עיקרית"),
                inv.assign(מקור="תרומת משקיע"),
            ],
            ignore_index=True,
        )
        if not supporters.empty:
            top_supporters = (
                supporters.groupby("שם", dropna=False)["שקלים"].sum().reset_index()
                .assign(שם=lambda df: df["שם"].fillna("ללא שם"))
                .sort_values("שקלים", ascending=False)
                .head(8)
            )
            top_supporters["שקלים"] = top_supporters["שקלים"].apply(format_currency)
            st.dataframe(
                top_supporters.rename(columns={"שם": "תורם", "שקלים": "סה\"כ תרומות"}),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("אין נתוני תרומות להצגה.")
    with col_b:
        st.markdown("##### הוצאות בולטות")
        top_expenses = (
            exp.groupby("שם", dropna=False)["שקלים"].sum().reset_index()
            .assign(שם=lambda df: df["שם"].fillna("ללא שם"))
            .sort_values("שקלים", ascending=False)
            .head(8)
        )
        if not top_expenses.empty:
            top_expenses["שקלים"] = top_expenses["שקלים"].apply(format_currency)
            st.dataframe(
                top_expenses.rename(columns={"שם": "ספק / יעד", "שקלים": "סה\"כ הוצאה"}),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("אין נתוני הוצאות להצגה.")


with planning_tab:
    st.subheader("חישוב הוספת אלמנות נוספות (36 חודשים)")
    st.write("בדקו כיצד הוספת אלמנות תשפיע על התקציב הקיים ל-36 חודשים קדימה.")

    def slider_limit(monthly_amount: float) -> int:
        total_pool = max(available + support_36_months, 0)
        base_limit = int(total_pool / (monthly_amount * 36)) + 10 if monthly_amount > 0 else 10
        return max(base_limit, 10)

    col1, col2 = st.columns(2)
    with col1:
        max_1000 = slider_limit(1000)
        n1 = st.slider(
            "מספר אלמנות ב-1,000 ₪/חודש",
            min_value=0,
            max_value=max_1000,
            value=0,
            step=1,
            key="widows_slider_1000",
        )
        req1 = n1 * 1000 * 36
    with col2:
        max_2000 = slider_limit(2000)
        n2 = st.slider(
            "מספר אלמנות ב-2,000 ₪/חודש",
            min_value=0,
            max_value=max_2000,
            value=0,
            step=1,
            key="widows_slider_2000",
        )
        req2 = n2 * 2000 * 36

    total_required = req1 + req2
    existing_commitment = support_36_months
    required_total = existing_commitment + total_required
    diff = available - required_total

    st.markdown("#### סיכום התחייבויות")
    sum_col1, sum_col2, sum_col3 = st.columns(3, gap="large")
    with sum_col1:
        metric_card(
            "עלות אלמנות חדשות ל-36 חודשים",
            format_currency(total_required),
            f"{n1} אלמנות ב-₪1,000 | {n2} אלמנות ב-₪2,000",
            "➕",
            "primary",
        )
    with sum_col2:
        metric_card(
            "התחייבויות קיימות",
            format_currency(existing_commitment),
            "סך הכל עבור התמיכה הקיימת",
            "📦",
            "warning",
        )
    status_variant = "success" if diff >= 0 else "danger"
    status_icon = "✅" if diff >= 0 else "⚠️"
    status_subtitle = "תקציב חופשי לאחר כל ההתחייבויות" if diff >= 0 else "נדרש לגייס סכום זה"
    with sum_col3:
        metric_card(
            "יתרה לאחר התחייבויות",
            format_currency(diff),
            status_subtitle,
            status_icon,
            status_variant,
        )

    if required_total > 0:
        coverage = min(max(available / required_total, 0), 1)
        st.progress(coverage)
        st.caption(
            f"סה\"כ נדרש: {format_currency(required_total)} | יתרה זמינה: {format_currency(available)}"
        )
    else:
        st.info("אין התחייבויות חדשות לחישוב כעת.")

    if diff >= 0:
        st.success(f"לאחר הכללת כל ההתחייבויות יוותר תקציב של {format_currency(diff)}.")
    else:
        st.error(f"חסר לגייס {format_currency(abs(diff))} כדי לעמוד בכל ההתחייבויות ל-36 חודשים.")

