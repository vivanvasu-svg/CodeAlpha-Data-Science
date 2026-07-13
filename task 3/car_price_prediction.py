import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

sns.set_theme(style="whitegrid")

def get_brand_and_type(row):
    name = str(row['Car_Name']).lower().strip()
    
    # Identify key two-wheeler brands & models
    bike_brands = ['royal enfield', 'ktm', 'bajaj', 'tvs', 'hero', 'yamaha', 'um', 'hyosung', 'mahindra']
    bike_models = ['activa', 'cb ', 'unicorn', 'shine', 'dream', 'cbr', 'twister', 'trigger', 'karizma', 'jupiter', 'wego', 'access']
    
    first_word = name.split()[0]
    brand = first_word
    
    # Map model keywords back to their manufacturers
    if first_word == 'royal':
        brand = 'royal enfield'
    elif first_word in ['etios', 'corolla', 'fortuner', 'innova', 'camry', 'land']:
        brand = 'toyota'
    elif first_word in ['i20', 'i10', 'grand', 'eon', 'xcent', 'elantra', 'creta', 'verna']:
        brand = 'hyundai'
    elif first_word in ['city', 'brio', 'amaze', 'jazz']:
        brand = 'honda'
    elif first_word in ['ritz', 'sx4', 'ciaz', 'wagon', 'swift', 'vitara', 's', 'alto', 'ertiga', 'dzire', 'baleno', 'omni', '800']:
        brand = 'maruti suzuki'
    
    if brand == 'activa':
        brand = 'honda'
        
    is_bike = any(b in name for b in bike_brands) or any(m in name for m in bike_models)
    vehicle_type = 'Two-Wheeler' if is_bike else 'Car'
    
    return pd.Series([brand, vehicle_type])

def main():
    print("Running Car Price Prediction Pipeline...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "car data.csv")
    charts_dir = os.path.join(base_dir, "charts")
    os.makedirs(charts_dir, exist_ok=True)
    
    # Load dataset
    df = pd.read_csv(data_path)
    print(f"Loaded shape: {df.shape}")
    
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
        
    df = df.dropna()
    
    # Feature Engineering
    df[['Brand', 'Vehicle_Type']] = df.apply(get_brand_and_type, axis=1)
    
    # Car age is relative to maximum year in dataset (2018) plus 1 to prevent zero/negative values
    ref_year = df['Year'].max() + 1
    df['Car_Age'] = ref_year - df['Year']
    
    df_vis = df.copy()
    
    # Target Resale Goodwill retention ratio computation on training fold to check leakage
    df['Price_Retention'] = df['Selling_Price'] / df['Present_Price']
    X = df.drop(columns=['Selling_Price', 'Car_Name', 'Year', 'Price_Retention'])
    y = df['Selling_Price']
    
    # Train-test split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Split: {X_train.shape[0]} train rows, {X_test.shape[0]} test rows")
    
    # Target encoding for resale brand retention
    train_df = X_train.copy()
    train_df['Selling_Price'] = y_train
    train_df['Price_Retention'] = train_df['Selling_Price'] / train_df['Present_Price']
    
    brand_goodwill = train_df.groupby('Brand')['Price_Retention'].median().to_dict()
    global_median = train_df['Price_Retention'].median()
    
    X_train['Brand_Goodwill'] = X_train['Brand'].map(brand_goodwill).fillna(global_median)
    X_test['Brand_Goodwill'] = X_test['Brand'].map(brand_goodwill).fillna(global_median)
    
    # One-hot encode categoricals
    cat_cols = ['Fuel_Type', 'Selling_type', 'Transmission', 'Vehicle_Type', 'Brand']
    X_comb = pd.concat([X_train, X_test], axis=0)
    X_comb_encoded = pd.get_dummies(X_comb, columns=cat_cols, drop_first=True)
    
    X_train_encoded = X_comb_encoded.iloc[:X_train.shape[0]].copy()
    X_test_encoded = X_comb_encoded.iloc[X_train.shape[0]:].copy()
    
    # Standard scale numeric columns
    num_cols = ['Present_Price', 'Driven_kms', 'Owner', 'Car_Age', 'Brand_Goodwill']
    scaler = StandardScaler()
    
    X_train_scaled = X_train_encoded.copy()
    X_test_scaled = X_test_encoded.copy()
    
    X_train_scaled[num_cols] = scaler.fit_transform(X_train_encoded[num_cols])
    X_test_scaled[num_cols] = scaler.transform(X_test_encoded[num_cols])
    
    # Model A: Linear Regression
    lr = LinearRegression()
    lr.fit(X_train_scaled, y_train)
    y_pred_lr = lr.predict(X_test_scaled)
    
    # Model B: Random Forest Regressor
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train_scaled, y_train)
    y_pred_rf = rf.predict(X_test_scaled)
    
    # Evaluate
    models = [("Linear Regression", y_pred_lr), ("Random Forest", y_pred_rf)]
    metrics = {}
    for name, pred in models:
        r2 = r2_score(y_test, pred)
        mae = mean_absolute_error(y_test, pred)
        rmse = np.sqrt(mean_squared_error(y_test, pred))
        metrics[name] = {"R2": r2, "MAE": mae, "RMSE": rmse}
        
    print("\n--- Model Performance Metrics ---")
    print(pd.DataFrame(metrics).T)
    
    # Visualizations
    print("\nGenerating charts...")
    
    # Chart 1: Heatmap
    plt.figure(figsize=(9, 7))
    df_num = df_vis[['Selling_Price', 'Present_Price', 'Driven_kms', 'Owner', 'Car_Age']]
    df_num = df_num.copy()
    df_num['Brand_Goodwill'] = df_vis['Brand'].map(brand_goodwill).fillna(global_median)
    
    sns.heatmap(df_num.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Correlation Matrix Heatmap")
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, "correlation_heatmap.png"))
    plt.close()
    
    # Chart 2: Predictions Scatter Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    
    # LR
    sns.scatterplot(ax=axes[0], x=y_test, y=y_pred_lr, color='#3498db', alpha=0.7)
    axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--k', lw=2)
    axes[0].set_title(f"Linear Regression (R² = {metrics['Linear Regression']['R2']:.3f})")
    axes[0].set_xlabel("Actual Price (Lakhs)")
    axes[0].set_ylabel("Predicted Price (Lakhs)")
    
    # RF
    sns.scatterplot(ax=axes[1], x=y_test, y=y_pred_rf, color='#2ecc71', alpha=0.7)
    axes[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--k', lw=2)
    axes[1].set_title(f"Random Forest (R² = {metrics['Random Forest']['R2']:.3f})")
    axes[1].set_xlabel("Actual Price (Lakhs)")
    
    plt.suptitle("Model Evaluation: Predicted vs. Actual Pricing")
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, "predicted_vs_actual.png"))
    plt.close()
    
    # Chart 3: Random Forest Feature Importances
    plt.figure(figsize=(10, 5))
    importances = rf.feature_importances_
    features = X_train_scaled.columns
    sorted_idx = np.argsort(importances)[::-1]
    
    top_n = min(10, len(features))
    sns.barplot(x=importances[sorted_idx[:top_n]], y=features[sorted_idx[:top_n]], palette="viridis", hue=features[sorted_idx[:top_n]], legend=False)
    plt.title(f"Top {top_n} Feature Importances (Random Forest)")
    plt.xlabel("Importance Score")
    plt.ylabel("Features")
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, "feature_importances.png"))
    plt.close()
    
    print("\nModel pipeline run completed.")

if __name__ == '__main__':
    main()
