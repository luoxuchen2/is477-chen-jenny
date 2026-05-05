# Data Dictionary

## Project Dataset

**File:** `data/processed/tennis_gdp_clean.csv`

This cleaned dataset integrates ATP tennis player ranking records with country-level real GDP data from the USDA ERS International Macroeconomic Data Set. Each row represents an ATP ranking record for a player in a specific year, enriched with player characteristics and country GDP information.

## Source Datasets

### ATP Players

**File:** `data/raw/atp_players.csv`  
**Source:** Jeff Sackmann `tennis_atp` GitHub repository  
**Description:** Contains demographic and identifying information about ATP players.

### ATP Rankings Current

**File:** `data/raw/atp_rankings_current.csv`  
**Source:** Jeff Sackmann `tennis_atp` GitHub repository  
**Description:** Contains ATP ranking records, including ranking date, player ID, rank, and ranking points.

### USDA Real GDP

**File:** `data/raw/RealGDP.csv`  
**Source:** USDA ERS International Macroeconomic Data Set  
**Description:** Contains historical and projected real GDP values for countries and regions.

## Cleaned Dataset Columns

| Column | Description |
|---|---|
| ranking_date | Date of the ATP ranking record. Converted from YYYYMMDD format into a date. |
| rank | ATP ranking position for the player on the ranking date. Lower values indicate better rankings. |
| player | Player identifier from the ATP rankings dataset. |
| points | ATP ranking points for the player. Higher values generally indicate stronger player performance. |
| player_id | Player identifier from the ATP players dataset. Used to merge rankings with player information. |
| name_first | Player first name. |
| name_last | Player last name. |
| hand | Player handedness. R = right-handed, L = left-handed, U or missing = unknown. |
| dob | Player date of birth in YYYYMMDD format in the raw ATP data. |
| ioc | Player country code from the ATP dataset. |
| height | Player height in centimeters, when available. |
| Year | Year extracted from `ranking_date`. Used to merge ATP data with GDP data. |
| country_name | Country name created by mapping ATP IOC country codes to USDA country names. |
| Observation | Country or region name from the USDA GDP dataset. |
| Unit | Measurement type from the USDA dataset. This project keeps records where `Unit` is `Real GDP USD`. |
| Value | Real GDP value from USDA, measured in billions of 2017 U.S. dollars. |
| log_gdp | Natural logarithm of `Value`. Created to reduce skewness in GDP values. |
| gdp_group | GDP quartile group based on `Value`: Low, Mid-Low, Mid-High, or High. |
| dob_clean | Cleaned version of the player date of birth converted to a date. |
| age | Player age at the time of the ranking record. Calculated using `ranking_date` and `dob_clean`. |
| handedness | Numeric version of handedness. Right-handed = 0, left-handed = 1, missing/unknown = -1. |
| rank_category | Ranking category created from `rank`: Top 10, Top 50, Top 100, or 100+. |

## Integration Strategy

The ATP rankings dataset was first merged with the ATP players dataset using the player identifier:

- `ranking.player`
- `player.player_id`

The integrated ATP dataset was then joined with the USDA GDP dataset using:

- `country_name`
- `Year`

Because the ATP data uses IOC-style country codes and the USDA data uses country names, an IOC-to-country-name mapping was created manually in `scripts/03_clean_integrate_data.py`.

## Cleaning Decisions

The following cleaning decisions were applied:

1. Removed ambiguous or historical ATP country codes such as `YUG`, `URS`, `SCG`, `ANZ`, `UNK`, and `?`.
2. Mapped ATP IOC country codes to USDA country names.
3. Kept only USDA records where `Unit` equals `Real GDP USD`.
4. Removed aggregate regions from the USDA data, such as `World`, `Europe`, `Asia`, and `High Income Countries`, because the analysis focuses on individual countries.
5. Dropped records where GDP values were missing after integration.
6. Converted ranking dates and dates of birth into date format.
7. Created player age at the time of ranking.
8. Created `log_gdp` to reduce skew in GDP values.
9. Created GDP quartile groups.
10. Created ranking categories for classification modeling.

## Data Quality Notes

Some ATP player fields, such as height, date of birth, and handedness, contain missing or inconsistent values. The project handles these by cleaning date fields, encoding missing handedness as `-1`, and dropping rows missing key modeling variables. The USDA GDP dataset contains both countries and aggregate regions, so aggregate regions were removed before integration.

## Output Files

| File | Description |
|---|---|
| `data/processed/tennis_gdp_clean.csv` | Cleaned and integrated dataset used for analysis and modeling. |
| `results/tables/raw_dataset_shapes.csv` | Row and column counts for raw datasets. |
| `results/tables/data_quality_summary.csv` | Column-level data quality summary. |
| `results/tables/missing_values_summary.csv` | Missing values summary by dataset and column. |
| `results/tables/country_summary.csv` | Country-level summary of player points and GDP. |
| `results/tables/correlation_summary.csv` | Correlation results for GDP, ranking, and points. |
| `results/tables/model_classification_report.csv` | Classification model performance results. |
| `results/tables/model_predictions.csv` | Actual and predicted rank categories. |
| `results/figures/points_distribution.png` | Distribution of ATP ranking points. |
| `results/figures/gdp_distribution.png` | Distribution of real GDP values. |
| `results/figures/gdp_vs_points.png` | Scatterplot of GDP and player points. |
| `results/figures/log_gdp_vs_points.png` | Scatterplot of log GDP and player points. |
| `results/figures/player_points_by_gdp_group.png` | Boxplot of player points by GDP group. |
| `results/figures/country_gdp_vs_average_points.png` | Country-level GDP versus average player points. |
