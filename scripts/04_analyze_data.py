"""
04_analyze_data.py

Runs summary analysis and classification modeling.

Input:
- data/processed/tennis_gdp_clean.csv

Outputs:
- results/tables/country_summary.csv
- results/tables/correlation_summary.csv
- results/tables/model_classification_report.csv
- results/tables/model_predictions.csv
"""

from pathlib import Path
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def main():
    Path("results/tables").mkdir(parents=True, exist_ok=True)

    df = pd.read_csv("data/processed/tennis_gdp_clean.csv")

    # Country-level summary.
    country_summary = (
        df.groupby("country_name")
        .agg(
            average_points=("points", "mean"),
            median_points=("points", "median"),
            average_gdp=("Value", "mean"),
            player_count=("player_id", "nunique"),
            ranking_records=("rank", "count")
        )
        .reset_index()
        .sort_values("average_points", ascending=False)
    )

    country_summary.to_csv("results/tables/country_summary.csv", index=False)

    # Correlation summary.
    individual_corr = df[["Value", "log_gdp", "points", "rank"]].corr()

    country_corr = country_summary[
        ["average_gdp", "average_points", "player_count", "ranking_records"]
    ].corr()

    correlation_summary = pd.concat(
        {
            "individual_level": individual_corr,
            "country_level": country_corr
        }
    )

    correlation_summary.to_csv("results/tables/correlation_summary.csv")

    # Model features.
    features = [
        "age",
        "height",
        "handedness",
        "log_gdp",
        "gdp_group"
    ]

    model_df = df[features + ["rank_category"]].dropna().copy()

    X = model_df[features]

    # Only one-hot encode the categorical variable.
    X = pd.get_dummies(X, columns=["gdp_group"], drop_first=True)

    y = model_df["rank_category"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    # Logistic regression model.
    logistic_model = LogisticRegression(
        max_iter=5000,
        class_weight="balanced"
    )

    logistic_model.fit(X_train, y_train)

    logistic_pred = logistic_model.predict(X_test)

    logistic_report = classification_report(
        y_test,
        logistic_pred,
        output_dict=True,
        zero_division=0
    )

    logistic_report_df = pd.DataFrame(logistic_report).transpose()
    logistic_report_df.insert(0, "model", "logistic_regression")

    # Random forest model.
    random_forest_model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    )

    random_forest_model.fit(X_train, y_train)

    random_forest_pred = random_forest_model.predict(X_test)

    random_forest_report = classification_report(
        y_test,
        random_forest_pred,
        output_dict=True,
        zero_division=0
    )

    random_forest_report_df = pd.DataFrame(random_forest_report).transpose()
    random_forest_report_df.insert(0, "model", "random_forest")

    # Save combined model report.
    model_report = pd.concat(
        [logistic_report_df, random_forest_report_df],
        axis=0
    )

    model_report.to_csv("results/tables/model_classification_report.csv")

    # Save predictions for transparency.
    predictions = pd.DataFrame({
        "actual": y_test,
        "logistic_prediction": logistic_pred,
        "random_forest_prediction": random_forest_pred
    })

    predictions.to_csv("results/tables/model_predictions.csv", index=False)

    print("Analysis and modeling complete.")
    print("Saved: results/tables/country_summary.csv")
    print("Saved: results/tables/correlation_summary.csv")
    print("Saved: results/tables/model_classification_report.csv")
    print("Saved: results/tables/model_predictions.csv")


if __name__ == "__main__":
    main()