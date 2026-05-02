import pandas as pd
from pathlib import Path



def main():
    # Create raw data folder if it does not exist
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Data source URLs
    players_url = (
        "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/"
        "atp_players.csv"
    )

    rankings_url = (
        "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/"
        "atp_rankings_current.csv"
    )

    gdp_url = (
        "https://www.ers.usda.gov/media/6157/"
        "historical-and-projected-real-gross-domestic-product-gdp-and-growth-rates-"
        "of-gdp-for-baseline-countriesregions-in-billions-of-2017-dollars-1970-2035.csv?v=18519"
    )

    print("Downloading ATP players data...")
    players = pd.read_csv(players_url)

    print("Downloading ATP rankings data...")
    rankings = pd.read_csv(rankings_url)

    print("Downloading USDA real GDP data...")
    gdp = pd.read_csv(gdp_url)

    # Save raw files
    players.to_csv(raw_dir / "atp_players.csv", index=False)
    rankings.to_csv(raw_dir / "atp_rankings_current.csv", index=False)
    gdp.to_csv(raw_dir / "RealGDP.csv", index=False)

    print("Data acquisition complete.")
    print(f"Saved: {raw_dir / 'atp_players.csv'}")
    print(f"Saved: {raw_dir / 'atp_rankings_current.csv'}")
    print(f"Saved: {raw_dir / 'RealGDP.csv'}")


if __name__ == "__main__":
    main()

