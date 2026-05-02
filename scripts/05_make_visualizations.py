"""
05_make_visualizations.py

Creates visualizations from the cleaned ATP-GDP dataset.

Input:
- data/processed/tennis_gdp_clean.csv

Outputs:
- results/figures/points_distribution.png
- results/figures/gdp_distribution.png
- results/figures/gdp_vs_points.png
- results/figures/log_gdp_vs_points.png
- results/figures/player_points_by_gdp_group.png
- results/figures/country_gdp_vs_average_points.png
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def main():
    Path("results/figures").mkdir(parents=True, exist_ok=True)

    df = pd.read_csv("data/processed/tennis_gdp_clean.csv")

    # Points distribution.
    plt.figure()
    df["points"].dropna().hist(bins=50)
    plt.title("Distribution of Player Points")
    plt.xlabel("Points")
    plt.ylabel("Frequency")
    plt.savefig("results/figures/points_distribution.png", bbox_inches="tight")
    plt.close()

    # GDP distribution.
    plt.figure()
    df["Value"].dropna().hist(bins=50)
    plt.title("Distribution of GDP")
    plt.xlabel("Real GDP")
    plt.ylabel("Frequency")
    plt.savefig("results/figures/gdp_distribution.png", bbox_inches="tight")
    plt.close()

    # GDP vs player points.
    plt.figure()
    plt.scatter(df["Value"], df["points"], alpha=0.5)
    plt.xlabel("Real GDP")
    plt.ylabel("Player Points")
    plt.title("GDP vs Player Success")
    plt.savefig("results/figures/gdp_vs_points.png", bbox_inches="tight")
    plt.close()

    # Log GDP vs player points.
    plt.figure()
    plt.scatter(df["log_gdp"], df["points"], alpha=0.5)
    plt.xlabel("Log GDP")
    plt.ylabel("Player Points")
    plt.title("Log GDP vs Player Success")
    plt.savefig("results/figures/log_gdp_vs_points.png", bbox_inches="tight")
    plt.close()

    # Boxplot of points by GDP group.
    group_order = ["Low", "Mid-Low", "Mid-High", "High"]

    groups = [
        df.loc[df["gdp_group"] == group, "points"].dropna()
        for group in group_order
        if group in df["gdp_group"].dropna().unique()
    ]

    labels = [
        group
        for group in group_order
        if group in df["gdp_group"].dropna().unique()
    ]

    plt.figure()
    plt.boxplot(groups, tick_labels=labels)
    plt.title("Player Points by GDP Group")
    plt.xlabel("GDP Group")
    plt.ylabel("Points")
    plt.savefig(
        "results/figures/player_points_by_gdp_group.png",
        bbox_inches="tight"
    )
    plt.close()

    # Country-level scatterplot.
    country_summary = (
        df.groupby("country_name")
        .agg(
            average_points=("points", "mean"),
            average_gdp=("Value", "mean")
        )
        .dropna()
        .reset_index()
    )

    plt.figure()
    plt.scatter(country_summary["average_gdp"], country_summary["average_points"])
    plt.xlabel("Country Real GDP")
    plt.ylabel("Average Player Points")
    plt.title("Country Wealth vs Average Player Success")
    plt.savefig(
        "results/figures/country_gdp_vs_average_points.png",
        bbox_inches="tight"
    )
    plt.close()

    print("Visualizations complete.")
    print("Saved figures in results/figures/")


if __name__ == "__main__":
    main()