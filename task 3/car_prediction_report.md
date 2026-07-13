# Car Price Prediction with Machine Learning
*Author: Vivan Vasu*

## Executive Summary
Predicting the resale value of a vehicle is a common machine learning application. This project trains and compares two models—**Linear Regression** and **Random Forest Regressor**—to predict car prices based on features like showroom price, distance driven, age, transmission type, fuel type, and brand goodwill. The Random Forest model performed significantly better, reaching an $R^2$ score of **96.8%** and a Root Mean Squared Error (RMSE) of **0.855 Lakhs** on the test set.

---

## 1. Feature Engineering and Preprocessing
The following preprocessing steps were performed on the raw dataset:
1. **Vehicle Type Segmentation (`Vehicle_Type`):** Classified vehicles as either a 'Car' or 'Two-Wheeler' by parsing model names (e.g., matching Bajaj, TVS, and Activa as Two-Wheelers).
2. **Brand Name Extraction (`Brand`):** Extracted the brand name from the car name field to capture brand-specific depreciation.
3. **Resale Goodwill (`Brand_Goodwill`):** Set a brand retention score calculated as:
   $$\text{Retention Ratio} = \frac{\text{Selling Price}}{\text{Present Price}}$$
   To avoid data leakage, this was calculated only using training fold splits.
4. **Car Age (`Car_Age`):** Calculated vehicle age relative to the dataset's maximum year.
5. **Encoding and Scaling:** One-hot encoded categorical variables (`Fuel_Type`, `Selling_type`, `Transmission`, `Vehicle_Type`, `Brand`) and standardized all numerical fields (`Present_Price`, `Driven_kms`, `Owner`, `Car_Age`, `Brand_Goodwill`) using StandardScaler.

---

## 2. Model Performance
Both models were evaluated on the 20% test fold. The results are summarized below:

| Metric | Linear Regression | Random Forest Regressor |
| :--- | :--- | :--- |
| **$R^2$ Score** | 0.850 (85.0%) | **0.968 (96.8%)** |
| **MAE (Lakhs)** | 1.157 | **0.540 (~54,000 INR)** |
| **RMSE (Lakhs)** | 1.861 | **0.855 (~85,500 INR)** |

### Key Observations:
- **Linear Regression** performs okay with an $R^2$ of $85\%$, but it struggles to capture non-linear behaviors (e.g., how a car's price drops exponentially as it ages).
- **Random Forest** handled these interactions much better, reducing prediction error to a median of **0.54 Lakhs** (54,000 INR), which is highly accurate.

---

## 3. Visualization and Results

### Feature Correlations
- `Present_Price` has the strongest correlation (**0.88**) with `Selling_Price`, showing that showroom price dominates resale value.
- `Car_Age` has a negative correlation (**-0.24**), showing the expected deprecation over time.

![Correlation Heatmap](/home/vivan/internship%20/task%203/charts/correlation_heatmap.png)

### Predictions vs. Actual Pricing
The diagonal line indicates a perfect prediction. Random Forest values cluster much closer to the diagonal line compared to Linear Regression.

![Predicted vs. Actual pricing plot](/home/vivan/internship%20/task%203/charts/predicted_vs_actual.png)

### Feature Importances
According to the Random Forest model, the top features determining pricing are:
1. **`Present_Price`:** Represents ~88% of performance, anchoring the resale value heavily to the original cost.
2. **`Car_Age`:** Accounts for ~7% importance.
3. **`Driven_kms`:** Influences wear-and-tear depreciation.

![Feature Importances plot](/home/vivan/internship%20/task%203/charts/feature_importances.png)

---

## 4. Real-World Applications
Linear or Random Forest regressors are commonly used by online marketplaces (e.g., Cars24, CarDekho) or dealerships to:
- Instantly estimate trade-in valuations on websites.
- Help banks forecast lease residual values.
- Audit fleet inventories for buying opportunities.
