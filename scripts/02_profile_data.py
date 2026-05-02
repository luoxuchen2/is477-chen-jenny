"""
02_profile_data.py

Profiles the raw ATP and USDA GDP datasets before cleaning/integration.

Inputs:
- data/raw/atp_players.csv
- data/raw/atp_rankings_current.csv
- data/raw/RealGDP.csv

Outputs:
- results/tables/data_quality_summary.csv
- results/tables/missing_values_summary.csv
- results/tables/raw_dataset_shapes.csv
"""

from pathlib import Path
import pandas as pd


def profile_dataset(df, dataset_name):
    """
    Create basic data quality profile for one dataset.
    """
    rows = []

    for col in df.columns:
        rows.append({
            "dataset": dataset_name,
            "column": col,
            "dtype": str(df[col].dtype),
            "num_rows": len(df),
            "missing_count": df[col].isna().sum(),
            "missing_percent": round(df[col].isna().mean() * 100, 2),
            "unique_count": df[col].nunique(dropna=True),
            "duplicate_rows_total": df.duplicated().sum()
        })

    return pd.DataFrame(rows)


def main():
    # Create output folder
    output_dir = Path("results/tables")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Read raw data
    players = pd.read_csv("data/raw/atp_players.csv")
    rankings = pd.read_csv("data/raw/atp_rankings_current.csv")
    gdp = pd.read_csv("data/raw/RealGDP.csv")

    # Dataset shape summary
    shapes = pd.DataFrame([
        {
            "dataset": "ATP players",
            "rows": players.shape[0],
            "columns": players.shape[1]
        },
        {
            "dataset": "ATP rankings current",
            "rows": rankings.shape[0],
            "columns": rankings.shape[1]
        },
        {
            "dataset": "USDA Real GDP",
            "rows": gdp.shape[0],
            "columns": gdp.shape[1]
        }
    ])

    shapes.to_csv(output_dir / "raw_dataset_shapes.csv", index=False)

    # Column-level profile
    players_profile = profile_dataset(players, "ATP players")
    rankings_profile = profile_dataset(rankings, "ATP rankings current")
    gdp_profile = profile_dataset(gdp, "USDA Real GDP")

    data_quality_summary = pd.concat(
        [players_profile, rankings_profile, gdp_profile],
        ignore_index=True
    )

    data_quality_summary.to_csv(
        output_dir / "data_quality_summary.csv",
        index=False
    )

    # Smaller missingness-only table for README/report
    missing_values_summary = data_quality_summary[
        [
            "dataset",
            "column",
            "missing_count",
            "missing_percent",
            "unique_count",
            "dtype"
        ]
    ].sort_values(
        by=["dataset", "missing_percent"],
        ascending=[True, False]
    )

    missing_values_summary.to_csv(
        output_dir / "missing_values_summary.csv",
        index=False
    )

    print("Data profiling complete.")
    print(f"Saved: {output_dir / 'raw_dataset_shapes.csv'}")
    print(f"Saved: {output_dir / 'data_quality_summary.csv'}")
    print(f"Saved: {output_dir / 'missing_values_summary.csv'}")


if __name__ == "__main__":
    main()