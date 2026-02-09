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

## Repository Structure

├─ notebooks/ # Jupyter analysis pipeline
├─ src/ # helper functions used by notebooks
└─ powerbi/ # PBIX + PDF export + assumptions

