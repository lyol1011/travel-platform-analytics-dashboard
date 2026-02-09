# Travel Platform Analytics: EDA + Stakeholder Questions + Power BI Dashboard

Group project from **DSCB310 – Data Analysis & Business Intelligence 1 (WS 2025/26)**.  
We act as a data science consulting team advising a US-based online travel booking platform.

The project covers:
- data preprocessing (users + clickstreams),
- exploratory analysis for a marketing stakeholder,
- statistical analysis answering concrete stakeholder questions,
- a prototype **Power BI business dashboard**.

> Educational project only.

---

## Business Case & Dataset

The platform dataset consists of multiple tables:
- `user.csv` (one row per user)
- `clickstreams.csv` (session logs)
- `geo_info.csv` (country attributes)
- `statistics.csv` (population statistics per country)

Target variable in the business context:
- `destination_country` of the first booking  
  - `NDF` = *no booking*
  - `other` = booking happened, but destination not in the predefined list

---

## Notebooks

1) **User data cleaning** — `I-filter_user_data.ipynb`  
   - duplicates checks, date parsing, missingness overview  
   - data quality rules (e.g., unrealistic ages removed)  
   - exports: `data/user_filtered.parquet`

2) **Clickstream cleaning** — `II-filter_clickstreams_data.ipynb`  
   - duplicates removal, handling “-unknown-” values, missingness  
   - session logic (e.g., new session if inactivity > 30 minutes)  
   - exports: `data/clickstreams_filtered.parquet`

3) **EDA for Marketing** — `III-user_EDA.ipynb`  
   - booking trends over time, conversion patterns, correlations  
   - insights oriented towards marketing decisions

4) **Stakeholder Questions** — `IV-stakeholders-questions.ipynb`  
   - statistical tests + visualizations (e.g., Chi² tests, effect sizes)  
   - explores relationships between user attributes, behavior and destinations

---

## Power BI Dashboard

Folder: `powerbi/`

- `Business Dashboard.pbix` — editable Power BI project
- `Business Dashboard.pdf` — exported dashboard (viewable on GitHub)
- `Business Dashboard - Annahmen.pdf` — stakeholder choice, KPI definitions and assumptions

Dashboard stakeholder: **Marketing department**  
Dashboard goal: fast decision support to prioritize channels/devices and identify conversion & NDF issues.

Key KPIs (example from dashboard export):
- Users, Bookers, Booking Rate, NDF Rate, Avg Sessions/User
- Conversion funnel and segment breakdowns (channel, device, destination, age, gender)
- Top countries and trends over time




