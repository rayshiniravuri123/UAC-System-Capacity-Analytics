
from pathlib import Path
import pandas as pd
import streamlit as st

# ==========================================
# 1. PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="UAC Care Load Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("System Capacity & Care Load Analytics")
st.subheader("Unaccompanied Children (UAC) Program")

st.write(
    "Interactive dashboard to analyse CBP custody, "
    "HHS care, total system load and daily intake."
)

# ==========================================
# 2. FIND THE DATASET AUTOMATICALLY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DATA_FILENAME = "UAC_Feature_Engineered_Dataset.csv"

possible_locations = [
    BASE_DIR / "UAC_Project_Output" / DATA_FILENAME,
    BASE_DIR / DATA_FILENAME,
]

DATA_FILE = None

for path in possible_locations:
    if path.exists():
        DATA_FILE = path
        break

# Search inside project folders if not found above
if DATA_FILE is None:
    matches = list(BASE_DIR.rglob(DATA_FILENAME))

    if matches:
        DATA_FILE = matches[0]

if DATA_FILE is None:
    st.error("Dataset not found!")

    st.write("Dashboard folder:", str(BASE_DIR))

    st.write(
        "Please run uac_analysis.py first. "
        "It creates UAC_Project_Output and the required CSV."
    )

    st.stop()

# ==========================================
# 3. LOAD DATASET
# ==========================================

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)

    data["Date"] = pd.to_datetime(
        data["Date"],
        errors="coerce"
    )

    return data

try:
    df = load_data(str(DATA_FILE))

except Exception as error:
    st.error(f"Unable to load dataset: {error}")
    st.stop()

st.success("Dataset loaded successfully!")

# ==========================================
# 4. SIDEBAR DATE FILTER
# ==========================================

st.sidebar.title("Dashboard Filters")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:

    start_date, end_date = date_range

    filtered = df[
        (df["Date"].dt.date >= start_date)
        & (df["Date"].dt.date <= end_date)
    ].copy()

else:
    filtered = df.copy()

if filtered.empty:
    st.warning("No records found for the selected dates.")
    st.stop()

# ==========================================
# 5. KPI CARDS
# ==========================================

st.header("Key Performance Indicators")

latest_load = filtered["Total System Load"].dropna()

average_load = filtered["Total System Load"].mean()

maximum_load = filtered["Total System Load"].max()

average_intake = filtered["Net Daily Intake"].mean()

positive_days = (
    filtered["Net Daily Intake"] > 0
).sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Latest System Load",
    f"{latest_load.iloc[-1]:,.0f}"
    if not latest_load.empty else "N/A"
)

col2.metric(
    "Average System Load",
    f"{average_load:,.0f}"
)

col3.metric(
    "Maximum System Load",
    f"{maximum_load:,.0f}"
)

col4.metric(
    "Positive Intake Days",
    f"{positive_days}"
)

st.divider()

# ==========================================
# 6. TOTAL SYSTEM LOAD
# ==========================================

st.header("1. Total System Load Trend")

st.line_chart(
    filtered.set_index("Date")["Total System Load"]
)

# ==========================================
# 7. CBP VS HHS COMPARISON
# ==========================================

st.header("2. CBP Custody vs HHS Care")

comparison = filtered.set_index("Date")[
    [
        "Children in CBP custody",
        "Children in HHS Care"
    ]
]

st.line_chart(comparison)

# ==========================================
# 8. NET DAILY INTAKE
# ==========================================

st.header("3. Net Daily Intake Trend")

st.line_chart(
    filtered.set_index("Date")["Net Daily Intake"]
)

st.metric(
    "Average Net Daily Intake",
    f"{average_intake:,.2f}"
)

# ==========================================
# 9. BACKLOG PRESSURE
# ==========================================

st.header("4. Daily Backlog Pressure")

st.metric(
    "Days with Positive Net Intake",
    f"{positive_days}"
)

st.write(
    "Positive net intake means transfers into HHS "
    "exceeded HHS discharges on that reporting day."
)

st.caption(
    "This is a daily pressure indicator, not a confirmed "
    "cumulative backlog."
)
# ==========================================
# 10. GROWTH RATE
# ==========================================

st.header("5. Care Load Growth Rate")

if "Care Load Growth Rate" in filtered.columns:

    st.line_chart(
        filtered.set_index("Date")["Care Load Growth Rate"]
    )

else:
    st.warning("Care Load Growth Rate column is not available.")
# ==========================================
# KEY INSIGHTS
# ==========================================

st.header("8. Key Insights")

if not filtered.empty:

    highest_load = filtered.loc[
        filtered["Total System Load"].idxmax()
    ]

    lowest_load = filtered.loc[
        filtered["Total System Load"].idxmin()
    ]

    latest_data = filtered.sort_values("Date").iloc[-1]

    st.write(
        f"Highest system load: {highest_load['Total System Load']:,.0f}"
    )

    st.write(
        f"Date of highest load: {highest_load['Date'].strftime('%d-%m-%Y')}"
    )

    st.write(
        f"Lowest system load: {lowest_load['Total System Load']:,.0f}"
    )

    st.write(
        f"Latest recorded system load: {latest_data['Total System Load']:,.0f}"
    )

else:
    st.warning("No data available for the selected date range.")





# ==========================================
# 11. DETAILED DATA
# ==========================================

st.header("6. Detailed UAC Dataset")

st.dataframe(
    filtered,
    use_container_width=True
)

# ==========================================
# 12. DOWNLOAD FILTERED DATA
# ==========================================

csv_data = filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Filtered Dataset",
    data=csv_data,
    file_name="UAC_Filtered_Analysis.csv",
    mime="text/csv"
)

# ==========================================
# 13. FOOTER
# ==========================================

st.divider()

st.success("UAC Analytics Dashboard Loaded Successfully!")

st.caption(
    "Project: System Capacity & Care Load Analytics "
    "| Unaccompanied Children Program"
)

# ==========================================
# MONTHLY SYSTEM LOAD ANALYSIS
# ==========================================

st.header("6. Monthly System Load Analysis")

monthly_data = (
    filtered.set_index("Date")["Total System Load"]
    .resample("MS")
    .mean()
)

st.line_chart(monthly_data)

st.caption(
    "This chart displays the average system load for each month."
)

# ==========================================
# YEARLY SYSTEM LOAD ANALYSIS
# ==========================================

st.header("7. Yearly System Load Analysis")

yearly_data = (
    filtered.groupby(
        filtered["Date"].dt.year
    )["Total System Load"]
    .mean()
)

st.bar_chart(yearly_data)

st.caption(
    "This chart compares the average system load across years."
)
