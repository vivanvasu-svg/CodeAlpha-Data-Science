# CodeAlpha Data Science Internship

This repository contains tasks completed during my Data Science Internship at CodeAlpha. Each task is self-contained with its code, raw datasets, generated visual diagrams, and written reports.

---

## Repository Structure

```directory
├── README.md
├── task 1/
│   ├── .gitignore
│   ├── Iris.csv
│   ├── train.py
│   ├── confusion_matrix.png
│   └── feature_importance.png
├── task 2/
│   ├── .gitignore
│   ├── archive(1)/
│   │   ├── Unemployment in India.csv
│   │   └── Unemployment_Rate_upto_11_2020.csv
│   ├── analysis.py
│   ├── unemployment_report.md
│   └── charts/
└── task 3/
    ├── .gitignore
    ├── car data.csv
    ├── car_price_prediction.py
    ├── car_prediction_report.md
    └── charts/
```

---

## Tasks Overview

### Task 1: Iris Flower Classification
- **Description:** A classification model built using a Random Forest Classifier to distinguish between Iris flower species (Setosa, Versicolor, and Virginica) based on biological features.
- **Frameworks:** `pandas`, `scikit-learn`, `seaborn`, `matplotlib`.
- **Accuracy Achieved:** $90.00\%$
- **Location:** `task 1/`

### Task 2: Unemployment Analysis in India
- **Description:** Exploratory Data Analysis (EDA) on datasets tracking monthly unemployment metrics across major Indian states from May 2019 to November 2020. Analyzed rural-to-urban divergence, COVID-19 lock-down spikes (which saw average rates climb to $18.75\%$), and the correlation with Labor Participation Rates ($r = -0.31$).
- **Frameworks:** `pandas`, `seaborn`, `matplotlib`.
- **Location:** `task 2/`

### Task 3: Car Resale Price Prediction
- **Description:** A regression system that compares Linear Regression and a Random Forest Regressor to predict the resale price of cars and motorcycles using ex-showroom values, age, mileage, fuel type, and brand trust factor indices.
- **Frameworks:** `pandas`, `scikit-learn`, `seaborn`, `matplotlib`.
- **Performance:** Random Forest Regressor outperformed Linear Regression with an $R^2$ of **$96.8\%$** and a Root Mean Squared Error (RMSE) of **0.855 Lakhs**.
- **Location:** `task 3/`

---

## Installation & Running the Code

To run these scripts locally on your machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/CodeAlpha-Data-Science.git
   cd CodeAlpha-Data-Science
   ```

2. **Install required dependencies:**
   ```bash
   pip install pandas numpy scikit-learn matplotlib seaborn
   ```

3. **Run individual modules:**
   - **Task 1 Classifier:**
     ```bash
     cd "task 1"
     python train.py
     ```
   - **Task 2 Analysis:**
     ```bash
     cd "task 2"
     python analysis.py
     ```
   - **Task 3 Predictor:**
     ```bash
     cd "task 3"
     python car_price_prediction.py
     ```
