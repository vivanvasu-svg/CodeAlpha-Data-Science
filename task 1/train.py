import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def main():
    # Load iris dataset
    csv_path = 'Iris.csv'
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    data = pd.read_csv(csv_path)
    print(f"Data successfully loaded. Shape: {data.shape}")
    print(data.head())

    # ID col isn't a biological feature, so let's drop it
    if 'Id' in data.columns:
        data = data.drop(columns=['Id'])

    # Split features and target
    X = data.drop(columns=['Species'])
    y = data['Species']

    # Split: 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Simple Random Forest classifier
    print("\nTraining Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict and evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:\n", report)

    # Plot Confusion Matrix
    plt.figure(figsize=(6, 4))
    labels = np.unique(y)
    sns.heatmap(
        cm, 
        annot=True, 
        fmt="d", 
        cmap="Blues", 
        xticklabels=labels, 
        yticklabels=labels,
        cbar=False
    )
    plt.title("Confusion Matrix", fontsize=12, fontweight='bold', pad=10)
    plt.xlabel("Predicted Species")
    plt.ylabel("Actual Species")
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=300)
    plt.close()
    print("Saved confusion matrix plot as confusion_matrix.png")

    # Plot Feature Importance
    plt.figure(figsize=(6, 4))
    importances = model.feature_importances_
    features = X.columns
    sorted_idx = np.argsort(importances)[::-1]

    sns.barplot(x=importances[sorted_idx], y=features[sorted_idx], palette="viridis", hue=features[sorted_idx], legend=False)
    plt.title("Feature Importance", fontsize=12, fontweight='bold', pad=10)
    plt.xlabel("Importance Score")
    plt.ylabel("Features")
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300)
    plt.close()
    print("Saved feature importance plot as feature_importance.png")

if __name__ == '__main__':
    main()
