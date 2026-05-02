# %%
import pandas as pd

# %%
player = pd.read_csv("atp_players.csv")
player

# %%
ranking = pd.read_csv("atp_rankings_current.csv")
ranking

# %%
player.columns

# %%
ranking.columns

# %%
gdp = pd.read_csv("RealGDP.csv")
gdp

# %%
gdp["Observation"].unique()

# %%
player["ioc"].unique()

# %%
player[player["ioc"] == "?"]

# %%
gdp.dropna()

# %%
import pandas as pd

# 1. Merge tennis tables
tennis = ranking.merge(
    player,
    left_on="player",
    right_on="player_id",
    how="left"
)

# 2. Extract year
tennis["ranking_date"] = pd.to_datetime(tennis["ranking_date"], format="%Y%m%d")
tennis["Year"] = tennis["ranking_date"].dt.year

# 3. Drop ambiguous historical codes
drop_codes = ["YUG", "URS", "SCG", "ANZ", "AHO", "ECA", "POC", "UNK", "?"]
tennis = tennis[~tennis["ioc"].isin(drop_codes)]

# 4. Map IOC code to USDA country name
ioc_to_country = {
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

tennis["country_name"] = tennis["ioc"].map(ioc_to_country)

# 5. Keep one USDA variable
usda_gdp = gdp[gdp["Unit"] == "Real GDP USD"].copy()

# 6. Remove aggregate regions
bad_obs = [
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
usda_gdp = usda_gdp[~usda_gdp["Observation"].isin(bad_obs)]

# 7. Merge
df = tennis.merge(
    usda_gdp,
    left_on=["country_name", "Year"],
    right_on=["Observation", "Year"],
    how="left"
)

# %%
df

# %%
df["Value"].unique()

# %%
df = df.dropna(subset=["Value"])

# %%
df = df.fillna("UNKNOWN")

# %%
df

# %%
df.describe(include="all")

# %%
import matplotlib.pyplot as plt

# Points distribution
plt.figure()
df["points"].dropna().hist(bins=50)
plt.title("Distribution of Player Points")
plt.xlabel("Points")
plt.ylabel("Frequency")
plt.show()

# GDP distribution
plt.figure()
df["Value"].dropna().hist(bins=50)
plt.title("Distribution of GDP")
plt.xlabel("GDP")
plt.ylabel("Frequency")
plt.show()

# %%
plt.figure()
plt.scatter(df["Value"], df["points"], alpha=0.5)
plt.xlabel("GDP")
plt.ylabel("Player Points")
plt.title("GDP vs Player Success")
plt.show()

# %%
import numpy as np

df["log_gdp"] = np.log(df["Value"])

plt.figure()
plt.scatter(df["log_gdp"], df["points"], alpha=0.5)
plt.xlabel("Log GDP")
plt.ylabel("Player Points")
plt.title("Log GDP vs Player Success")
plt.show()

# %%
# Create GDP bins
df["gdp_group"] = pd.qcut(df["Value"], q=4, labels=["Low", "Mid-Low", "Mid-High", "High"])

# Boxplot
groups = []
labels = []

for g in df["gdp_group"].dropna().unique():
    groups.append(df.loc[df["gdp_group"] == g, "points"].dropna())
    labels.append(g)

plt.figure()
plt.boxplot(groups, tick_labels=labels)
plt.title("Player Points by GDP Group")
plt.xlabel("GDP Group")
plt.ylabel("Points")
plt.show()

# %%
country_summary = df.groupby("country_name").agg({
    
    "points": "mean",
    "Value": "mean"
}).dropna()

print(country_summary.head())

# %%
plt.figure()
plt.scatter(country_summary["Value"], country_summary["points"])
plt.xlabel("Country GDP")
plt.ylabel("Average Player Points")
plt.title("Country Wealth vs Avg Player Success")
plt.show()

# %%
print("Correlation (GDP vs points):")
print(df[["Value", "points"]].corr())

print("Country-level correlation:")
print(country_summary[["Value", "points"]].corr())

# %%
import pandas as pd

# ranking_date to datetime
df["ranking_date"] = pd.to_datetime(df["ranking_date"], format="%Y%m%d", errors="coerce")

# clean dob
df["dob_clean"] = (
    df["dob"]
    .replace(["UNKNOWN", "unknown", ""], pd.NA)   # treat text placeholders as missing
    .astype("string")                             # convert everything to string safely
    .str.replace(".0", "", regex=False)           # remove trailing .0
    .str.strip()
)

# convert cleaned dob to datetime
df["dob_clean"] = pd.to_datetime(df["dob_clean"], format="%Y%m%d", errors="coerce")

# calculate age
df["age"] = ((df["ranking_date"] - df["dob_clean"]).dt.days / 365.25).round(0)

print(df[["dob", "dob_clean", "ranking_date", "age"]].head(10))

# %%
df["handedness"] = df["hand"].map({
    "R": 0,
    "L": 1
})

# Fill missing values
df["handedness"] = df["handedness"].fillna(-1)

# %%
df["handedness"]

# %%
def rank_category(rank):
    if rank <= 10:
        return "Top 10"
    elif rank <= 50:
        return "Top 50"
    elif rank <= 100:
        return "Top 100"
    else:
        return "100+"

# %%
df["rank_category"] = df["rank"].apply(rank_category)

# %%
df.columns

# %%
features = [
    "age",
    "height",
    "handedness",
    "log_gdp",       # better than raw GDP
    "gdp_group"
]

# %% [markdown]
# rank ❌ (that’s literally what you're predicting)
# points ❌ (strong proxy for rank)
# ranking_date ❌ unless you engineer time features
# player_id, name ❌ useless identifiers

# %%
import pandas as pd

X = df[features]

# one-hot encode categorical variables
X = pd.get_dummies(X, columns= features)

y = df["rank_category"]

# %%
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000, multi_class="multinomial")

# %%
from sklearn.ensemble import RandomForestClassifier

model2 = RandomForestClassifier(
    
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

# %%
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(classification_report(y_test, y_pred))

# %%



