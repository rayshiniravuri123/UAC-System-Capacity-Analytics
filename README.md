
# System Capacity & Care Load Analytics for Unaccompanied Children

## Project Overview
This project analyzes the Unaccompanied Alien Children (UAC) Program data to understand system capacity, child care load, daily intake, transfers, and discharges.

The objective is to identify trends and understand how the number of children in the system changes over time.

## Business Problem
The UAC program needs to monitor the number of children entering, remaining in, and leaving the care system.

This analysis helps understand:
- Changes in daily system load
- CBP custody and HHS care trends
- Net daily intake
- Backlog pressure
- Monthly and yearly system load patterns

## Tools & Technologies
- Python
- Pandas
- Matplotlib
- Streamlit
- CSV Dataset
- Visual Analytics

## Project Workflow
1. Data loading
2. Data cleaning and validation
3. Missing date analysis
4. Feature engineering
5. KPI calculation
6. Trend analysis
7. Data visualization
8. Interactive dashboard development

## Key Dashboard Features
- Total System Load Trend
- CBP Custody vs HHS Care
- Net Daily Intake Trend
- Daily Backlog Pressure
- Care Load Growth Rate
- Monthly System Load Analysis
- Yearly System Load Analysis
- Key Insights
- Date range filtering
- Filtered dataset download

## Project Structure
- uac_analysis.py – Data analysis script
- app.py – Streamlit dashboard
- UAC_Project_Output/ – Generated reports and charts
- README.md – Project documentation

## How to Run
Install the required libraries:

```bash
pip install pandas matplotlib streamlit
```

Run the analysis:

```bash
python uac_analysis.py
```

Run the dashboard:

```bash

## Data Visualizations

### 1. Daily System Load
![Daily System Load](UAC_Project_Output/Chart_1_Daily_System_Load.png)

### 2. Weekly System Load
![Weekly System Load](UAC_Project_Output/Chart_2_Weekly_System_Load.png)

### 3. CBP Custody vs HHS Care
![CBP vs HHS](UAC_Project_Output/Chart_3_CBP_vs_HHS.png)

### 4. Net Daily Intake
![Net Daily Intake](UAC_Project_Output/Chart_4_Net_Daily_Intake.png)

python -m streamlit run app.py
```

## Expected Outcome
An interactive analytics dashboard that helps explore UAC program trends and understand changes in system capacity and care load over time.

