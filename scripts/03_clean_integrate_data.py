"""
03_integrate_data.py

Cleans and integrates ATP player rankings data with USDA real GDP data.

Inputs:
- data/raw/atp_players.csv
- data/raw/atp_rankings_current.csv
- data/raw/RealGDP.csv

Outputs:
- data/processed/tennis_gdp_clean.csv
"""

from pathlib import Path
import numpy as np
import pandas as pd


IOC_TO_COUNTRY = {
    "USA": "United States",
    "ECU": "Ecuador",
    "AUS": "Australia",
    "ITA": "Italy",
    "RSA": "South Africa",
    "DEN": "Denmark",
    "HUN": "Hungary",
    "CHI": "Chile",
    "POL": "Poland",
    "PER": "Peru",
    "IND": "India",
    "SWE": "Sweden",
    "ESP": "Spain",
    "SUI": "Switzerland",
    "GER": "Germany",
    "ROU": "Romania",
    "CRO": "Croatia",
    "JPN": "Japan",
    "CZE": "Czech Republic",
    "RUS": "Russia",
    "GBR": "United Kingdom",
    "BRA": "Brazil",
    "FRA": "France",
    "SRB": "Serbia",
    "NED": "Netherlands",
    "CAN": "Canada",
    "GRE": "Greece",
    "MEX": "Mexico",
    "COL": "Colombia",
    "ARG": "Argentina",
    "BEL": "Belgium",
    "NZL": "New Zealand",
    "VEN": "Venezuela",
    "EGY": "Egypt",
    "BOL": "Bolivia",
    "AUT": "Austria",
    "PAK": "Pakistan",
    "IRL": "Ireland",
    "IRI": "Iran",
    "FIN": "Finland",
    "URU": "Uruguay",
    "ISR": "Israel",
    "KOR": "Korea",
    "CRC": "Costa Rica",
    "MAR": "Morocco",
    "SVK": "Slovakia",
    "UKR": "Ukraine",
    "PHI": "Philippines",
    "TUR": "Turkey",
    "HKG": "Hong Kong",
    "BUL": "Bulgaria",
    "NOR": "Norway",
    "POR": "Portugal",
    "GEO": "Georgia",
    "THA": "Thailand",
    "CHN": "China",
    "SLO": "Slovenia",
    "EST": "Estonia",
    "BLR": "Belarus",
    "UZB": "Uzbekistan",
    "ARM": "Armenia",
    "QAT": "Qatar",
    "BIH": "Bosnia and Herzegovina",
    "LTU": "Lithuania",
    "MDA": "Moldova",
    "KAZ": "Kazakhstan",
    "ISL": "Iceland",
    "UAE": "United Arab Emirates",
    "MNE": "Montenegro",
    "VIE": "Vietnam",
    "CYP": "Cyprus",
    "TJK": "Tajikistan",
    "NAM": "Namibia",
    "UGA": "Uganda",
    "KGZ": "Kyrgyzstan",
    "SGP": "Singapore",
    "PNG": "Papua New Guinea",
    "IRQ": "Iraq",
    "CMR": "Cameroon",
    "JOR": "Jordan",
    "PAN": "Panama",
    "NPL": "Nepal",
    "NIC": "Nicaragua",
    "AGO": "Angola",
    "BWA": "Botswana",
    "DEU": "Germany",
    "FRG": "Germany",
    "GDR": "Germany",
    "TWN": "Taiwan",
    "TPE": "Taiwan",
}


BAD_IOC_CODES = [
    "YUG", "URS", "SCG", "ANZ", "AHO", "ECA", "POC", "UNK", "?"
]


BAD_GDP_OBSERVATIONS = [
    "Africa", "Asia", "Asia Less Japan", "Asia and Oceania",
    "BRIICs", "East Asia", "East Asia Less Japan",
    "Euro Zone", "Europe", "Europe and Central Asia",
    "European Union 15", "European Union 27",
    "Former Centrally Planned Economies", "Former Soviet Union",
    "High Income Countries", "High Income Countries less USA",
    "Latin America", "Low Income Countries",
    "Lower-Middle Income Countries", "Middle East",
    "Middle East and North Africa", "North Africa",
    "North America", "Oceania", "South America", "South Asia",
    "Southeast Asia", "Sub-Saharan Africa", "USMCA",
    "Upper-Middle Income Countries", "World", "World Less USA",
    "Other Former Soviet Union", "Other Europe", "Other Asia Oceania"
]


def rank_category(rank):
    if rank <= 10:
        return "Top 10"
    elif rank <= 50:
        return "Top 50"
    elif rank <= 100:
        return "Top 100"
    else:
        return "100+"


def main():
    Path("data/processed").mkdir(parents=True, exist_ok=True)

    players = pd.read_csv("data/raw/atp_players.csv")
    rankings = pd.read_csv("data/raw/atp_rankings_current.csv")
    gdp = pd.read_csv("data/raw/RealGDP.csv")

    # Merge ATP rankings with player demographic information.
    tennis = rankings.merge(
        players,
        left_on="player",
        right_on="player_id",
        how="left"
    )

    # Convert ranking date and extract year.
    tennis["ranking_date"] = pd.to_datetime(
        tennis["ranking_date"],
        format="%Y%m%d",
        errors="coerce"
    )
    tennis["Year"] = tennis["ranking_date"].dt.year

    # Remove ambiguous or historical country codes.
    tennis = tennis[~tennis["ioc"].isin(BAD_IOC_CODES)].copy()

    # Map IOC country codes to USDA country names.
    tennis["country_name"] = tennis["ioc"].map(IOC_TO_COUNTRY)

    # Keep only real GDP data.
    usda_gdp = gdp[gdp["Unit"] == "Real GDP USD"].copy()

    # Remove aggregate regions that are not individual countries.
    usda_gdp = usda_gdp[~usda_gdp["Observation"].isin(BAD_GDP_OBSERVATIONS)].copy()

    # Merge tennis data with GDP data.
    df = tennis.merge(
        usda_gdp,
        left_on=["country_name", "Year"],
        right_on=["Observation", "Year"],
        how="left"
    )

    # Keep rows with matched GDP value.
    df = df.dropna(subset=["Value"]).copy()

    # Make sure important numeric variables are numeric.
    numeric_cols = ["rank", "points", "height", "Value", "dob"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Create log GDP.
    df = df[df["Value"] > 0].copy()
    df["log_gdp"] = np.log(df["Value"])

    # Create GDP quartile groups.
    df["gdp_group"] = pd.qcut(
        df["Value"],
        q=4,
        labels=["Low", "Mid-Low", "Mid-High", "High"],
        duplicates="drop"
    )

    # Clean date of birth.
    df["dob_clean"] = (
        df["dob"]
        .astype("string")
        .str.replace(".0", "", regex=False)
        .str.strip()
    )

    df["dob_clean"] = pd.to_datetime(
        df["dob_clean"],
        format="%Y%m%d",
        errors="coerce"
    )

    # Calculate age.
    df["age"] = ((df["ranking_date"] - df["dob_clean"]).dt.days / 365.25).round(0)

    # Encode handedness.
    df["handedness"] = df["hand"].map({
        "R": 0,
        "L": 1
    })

    df["handedness"] = df["handedness"].fillna(-1)

    # Create ranking category outcome variable.
    df["rank_category"] = df["rank"].apply(rank_category)

    # Remove rows missing model features.
    model_cols = ["age", "height", "handedness", "log_gdp", "gdp_group", "rank_category"]
    df = df.dropna(subset=model_cols).copy()

    # Save cleaned and integrated data.
    df.to_csv("data/processed/tennis_gdp_clean.csv", index=False)

    print("Cleaning and integration complete.")
    print("Saved: data/processed/tennis_gdp_clean.csv")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")


if __name__ == "__main__":
    main()