rule all:
    input:
        "data/raw/atp_players.csv",
        "data/raw/atp_rankings_current.csv",
        "data/raw/RealGDP.csv",
        "results/tables/raw_dataset_shapes.csv",
        "results/tables/data_quality_summary.csv",
        "results/tables/missing_values_summary.csv",
        "data/processed/tennis_gdp_clean.csv",
        "results/tables/country_summary.csv",
        "results/tables/correlation_summary.csv",
        "results/tables/model_classification_report.csv",
        "results/tables/model_predictions.csv",
        "results/figures/points_distribution.png",
        "results/figures/gdp_distribution.png",
        "results/figures/gdp_vs_points.png",
        "results/figures/log_gdp_vs_points.png",
        "results/figures/player_points_by_gdp_group.png",
        "results/figures/country_gdp_vs_average_points.png"

rule acquire_data:
    output:
        players="data/raw/atp_players.csv",
        rankings="data/raw/atp_rankings_current.csv",
        gdp="data/raw/RealGDP.csv"
    shell:
        "python scripts/01_acquire_data.py"

rule profile_data:
    input:
        players="data/raw/atp_players.csv",
        rankings="data/raw/atp_rankings_current.csv",
        gdp="data/raw/RealGDP.csv"
    output:
        shapes="results/tables/raw_dataset_shapes.csv",
        quality="results/tables/data_quality_summary.csv",
        missing="results/tables/missing_values_summary.csv"
    shell:
        "python scripts/02_profile_data.py"

rule clean_integrate_data:
    input:
        players="data/raw/atp_players.csv",
        rankings="data/raw/atp_rankings_current.csv",
        gdp="data/raw/RealGDP.csv"
    output:
        "data/processed/tennis_gdp_clean.csv"
    shell:
        "python scripts/03_clean_integrate_data.py"

rule analyze_data:
    input:
        "data/processed/tennis_gdp_clean.csv"
    output:
        country_summary="results/tables/country_summary.csv",
        correlation_summary="results/tables/correlation_summary.csv",
        model_report="results/tables/model_classification_report.csv",
        predictions="results/tables/model_predictions.csv"
    shell:
        "python scripts/04_analyze_data.py"

rule make_visualizations:
    input:
        "data/processed/tennis_gdp_clean.csv"
    output:
        "results/figures/points_distribution.png",
        "results/figures/gdp_distribution.png",
        "results/figures/gdp_vs_points.png",
        "results/figures/log_gdp_vs_points.png",
        "results/figures/player_points_by_gdp_group.png",
        "results/figures/country_gdp_vs_average_points.png"
    shell:
        "python scripts/05_make_visualizations.py"