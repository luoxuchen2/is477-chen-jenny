"""
01_acquire_data.py

Downloads the raw datasets used in the project and verifies file integrity
using SHA-256 checksums.

Outputs:
- data/raw/atp_players.csv
- data/raw/atp_rankings_current.csv
- data/raw/RealGDP.csv
- data/raw/actual_checksums_sha256.csv
- data/raw/checksum_verification.csv
"""

from pathlib import Path
import hashlib
import pandas as pd


def sha256_file(path):
    """Return SHA-256 hash for a file."""
    h = hashlib.sha256()

    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            h.update(chunk)

    return h.hexdigest()


def main():
    raw_dir = Path("data/raw")
    metadata_dir = Path("metadata")

    raw_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)

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
    players = pd.read_csv(players_url, low_memory=False)

    print("Downloading ATP rankings data...")
    rankings = pd.read_csv(rankings_url, low_memory=False)

    print("Downloading USDA real GDP data...")
    gdp = pd.read_csv(gdp_url, low_memory=False)

    # Save raw files
    players_path = raw_dir / "atp_players.csv"
    rankings_path = raw_dir / "atp_rankings_current.csv"
    gdp_path = raw_dir / "RealGDP.csv"

    players.to_csv(players_path, index=False)
    rankings.to_csv(rankings_path, index=False)
    gdp.to_csv(gdp_path, index=False)

    print("Data acquisition complete.")
    print(f"Saved: {players_path}")
    print(f"Saved: {rankings_path}")
    print(f"Saved: {gdp_path}")

    # Compute actual checksums from downloaded files
    actual_checksums = pd.DataFrame(
        [
            {
                "file": "atp_players.csv",
                "actual_sha256": sha256_file(players_path)
            },
            {
                "file": "atp_rankings_current.csv",
                "actual_sha256": sha256_file(rankings_path)
            },
            {
                "file": "RealGDP.csv",
                "actual_sha256": sha256_file(gdp_path)
            }
        ]
    )

    actual_checksums_path = raw_dir / "actual_checksums_sha256.csv"
    actual_checksums.to_csv(actual_checksums_path, index=False)

    print(f"Saved: {actual_checksums_path}")

    # Compare actual checksums against expected checksums
    expected_checksums_path = metadata_dir / "expected_checksums.csv"

    if not expected_checksums_path.exists():
        starter_expected = actual_checksums.rename(
            columns={"actual_sha256": "expected_sha256"}
        )

        starter_expected.to_csv(expected_checksums_path, index=False)

        print("No expected checksum file was found.")
        print(f"Created starter file: {expected_checksums_path}")
        print("Review the downloaded files. If correct, keep this file for future verification.")

    expected_checksums = pd.read_csv(expected_checksums_path)

    verification = expected_checksums.merge(
        actual_checksums,
        on="file",
        how="left"
    )

    verification["matches_expected"] = (
        verification["expected_sha256"] == verification["actual_sha256"]
    )

    verification_path = raw_dir / "checksum_verification.csv"
    verification.to_csv(verification_path, index=False)

    print(f"Saved: {verification_path}")

    if not verification["matches_expected"].all():
        print(verification)
        raise ValueError(
            "At least one downloaded file failed SHA-256 verification."
        )

    print("All files passed SHA-256 checksum verification.")


if __name__ == "__main__":
    main()