# Unemployment Analysis in India (2019-2020)
*Author: Vivan Vasu*

## Executive Summary
This report analyzes unemployment trends in India before and during the COVID-19 pandemic using data from May 2019 to November 2020. The goal is to study how rural and urban markets behaved, measure the impact of the national lockdown, and see the correlation between unemployment rates and labor force participation.

---

## 1. Data and Cleaning Process
Two main datasets containing monthly employment numbers and unemployment rates across different states were preprocessed:
- **Dataset 1 (Rural & Urban):** Helped compare rural and urban areas.
- **Dataset 2 (State Level):** Contained geocoded coordinates and region zones up to November 2020.

### Preprocessing:
1. Stripped whitespaces from column headers and string values.
2. Handled missing rows and dropped completely empty values.
3. Converted dates to standard datetime format for consistency.
4. Extracted year and month columns to make trend analysis easier.

---

## 2. Overall Trends and Lockdown Impact
Before March 2020, national unemployment was relatively stable, staying between **8.8%** and **9.9%**. The nationwide lockdown in late March 2020 caused a major spike.

![National Unemployment Trend](/home/vivan/internship%20/task%202/charts/overall_unemployment_trend.png)

- **Pre-lockdown average (Jan-Mar 2020):** **9.76%**
- **Lockdown peak (Apr-Jun 2020):** **18.75%** (Nearly double)
- **Recovery average (Jul-Oct 2020):** **9.22%**

The peak in April and May was caused by the sudden halt of business operations. As restrictions started easing in June 2020, unemployment numbers returned to pre-pandemic levels fairly quickly.

---

## 3. Comparison: Urban vs. Rural Areas
Urban areas were hit harder during the lockdown compared to rural sectors:

![Urban vs Rural Comparison](/home/vivan/internship%20/task%202/charts/urban_vs_rural_comparison.png)

- **Pre-lockdown averages:** Urban was structurally higher at **10.91%** compared to rural at **8.23%**.
- **Lockdown peak averages:** Urban unemployment jumped to **22.08%**, while rural rose to **18.26%**.
- **Discussion:** Rural areas were slightly cushioned because agricultural activities were allowed to continue early on and programs like MGNREGA helped support returning laborers. Urban areas, which rely heavily on services and retail, had fewer safety nets.

---

## 4. State-wide and Regional Impact
The intensity of the lockdown varied heavily across states:

![State-wise Peak Lockdown Unemployment](/home/vivan/internship%20/task%202/charts/statewise_unemployment_covid.png)

- **Most Affected States (Apr-Jun 2020):** Puducherry and Jharkhand saw averages go past **50%** due to service shutdowns. Tamil Nadu, Bihar, and Haryana stayed between **30% and 40%**.
- **Least Affected States:** Gujarat and Telangana maintained lower averages, partly due to industries resuming operations sooner.

### Zone Trends:
![Zone-wise Trends](/home/vivan/internship%20/task%202/charts/zone_unemployment_trend.png)

The South zone experienced an explosive spike in April 2020, driven by strict lockdowns in metropolitan cities, but recovered in a V-shape by July.

---

## 5. Labour Participation and Unemployment Correlation
Analyzing the relationship between the Unemployment Rate and the Labour Participation Rate (LPR) shows a negative correlation:

![Unemployment vs Participation](/home/vivan/internship%20/task%202/charts/unemployment_vs_participation.png)

- **Correlation Coefficient ($r$):** **-0.31**
- **Insight:** During the peak lockdown months, the LPR dropped as unemployment rose. This indicates that many people stopped actively looking for jobs because they knew none were available, effectively exiting the active workforce temporarily.

---

## 6. Baseline Seasonality Check (2019)
To make sure the 2020 spikes were pandemic-driven rather than normal seasonal changes, we checked the month-on-month trend for 2019:

| Month (2019) | Avg Unemployment Rate (%) |
| :--- | :--- |
| May | 8.87% |
| June | 9.30% |
| July | 9.03% |
| August | 9.64% |
| September | 9.05% |
| October | 9.90% |
| November | 9.87% |
| December | 9.50% |

The dataset shows no dramatic shifts in 2019 (variance was only around **1%**). This confirms that the severe spike in 2020 was indeed a unique economic shock from COVID-19.

---

## 7. Policy Recommendations
Based on the data, here are some practical policy ideas for future economic shocks:
1. **Urban jobs program:** Implementing an urban counterpart to MGNREGA to support service and informals sector workers during crises.
2. **Social security for gig workers:** Protecting freelancers and contract laborers who lack corporate safety nets.
3. **Regional manufacturing support:** Encouraging industrial diversification in vulnerable regions to avoid dependency on service sectors.
