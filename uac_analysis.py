from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# UAC SYSTEM CAPACITY & CARE LOAD ANALYTICS
# Keep this Python file and the CSV in the SAME folder.
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "HHS_Unaccompanied_Alien_Children_Program.csv"
OUTPUT_DIR = BASE_DIR / "UAC_Project_Output"
OUTPUT_DIR.mkdir(exist_ok=True)

if not CSV_FILE.exists():
    raise FileNotFoundError(
        f"CSV file not found:\n{CSV_FILE}\n\n"
        "Place HHS_Unaccompanied_Alien_Children_Program.csv "
        "in the same folder as this Python file."
    )

print("Loading UAC dataset...")
df = pd.read_csv(CSV_FILE)

# Exact column names verified from the supplied CSV
DATE = "Date"
APPREHENDED = "Children apprehended and placed in CBP custody*"
CBP_CUSTODY = "Children in CBP custody"
CBP_TRANSFERS = "Children transferred out of CBP custody"
HHS_CARE = "Children in HHS Care"
HHS_DISCHARGES = "Children discharged from HHS Care"

required_columns = [
    DATE, APPREHENDED, CBP_CUSTODY, CBP_TRANSFERS,
    HHS_CARE, HHS_DISCHARGES
]
missing_columns = [c for c in required_columns if c not in df.columns]
if missing_columns:
    raise ValueError(f"These required columns are missing: {missing_columns}")

# STEP 1 — Clean rows and convert data types
df = df[required_columns].copy()
df = df.dropna(how="all")
df[DATE] = pd.to_datetime(df[DATE], errors="coerce")
df = df.dropna(subset=[DATE])

numeric_columns = [
    APPREHENDED, CBP_CUSTODY, CBP_TRANSFERS, HHS_CARE, HHS_DISCHARGES
]
for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column].astype(str).str.replace(",", "", regex=False).str.strip(),
        errors="coerce"
    )

df = df.sort_values(DATE)
duplicate_count = int(df.duplicated(subset=[DATE]).sum())
df = df.drop_duplicates(subset=[DATE], keep="last").reset_index(drop=True)

print(f"STEP 1 complete: {len(df)} dated records; {duplicate_count} duplicate dates removed.")

# STEP 2 — Missing reporting dates (do NOT replace missing observations with zero)
all_dates = pd.date_range(df[DATE].min(), df[DATE].max(), freq="D")
reported_dates = pd.DatetimeIndex(df[DATE].drop_duplicates())
missing_dates = all_dates.difference(reported_dates)

pd.DataFrame({"Missing_Date": missing_dates}).to_csv(
    OUTPUT_DIR / "UAC_Missing_Dates_Report.csv", index=False
)
coverage_pct = len(reported_dates) / len(all_dates) * 100
print(f"STEP 2 complete: {len(missing_dates)} missing calendar dates; coverage {coverage_pct:.2f}%.")

# STEP 3 — Complete calendar dataset; absent dates remain blank/NaN
daily = df.set_index(DATE).reindex(all_dates)
daily.index.name = DATE
daily = daily.reset_index()
daily["Reporting Status"] = daily[numeric_columns].notna().any(axis=1).map(
    {True: "Reported", False: "Missing"}
)
daily.to_csv(OUTPUT_DIR / "UAC_Complete_Daily_Dataset.csv", index=False)
print("STEP 3 complete: complete daily calendar saved.")

# STEP 4 — Basic data validation
validation = df[[DATE] + numeric_columns].copy()
validation["Has Negative Value"] = df[numeric_columns].lt(0).any(axis=1)
validation["Has Missing Numeric Value"] = df[numeric_columns].isna().any(axis=1)
validation.to_csv(OUTPUT_DIR / "UAC_Data_Validation_Report.csv", index=False)
print("STEP 4 complete: validation report saved.")
print("Rows with negative values:", int(validation["Has Negative Value"].sum()))
print("Rows with missing numeric values:", int(validation["Has Missing Numeric Value"].sum()))

# STEP 5 — Feature engineering
df["Total System Load"] = df[CBP_CUSTODY] + df[HHS_CARE]
df["Net Daily Intake"] = df[CBP_TRANSFERS] - df[HHS_DISCHARGES]

previous_load = df["Total System Load"].shift(1)