# Status Report 


### Update on Each Task

We first read the rankings dataset: tennis_atp/atp_rankings_current.csv at master, the ATP players dataset: tennis_atp/atp_players.csv at master, and the GDP dataset: International Macroeconomic Data Set | Economic Research Service.

Next, we looked at the country's unique values for GDP as well as players’ IOC (country they represent).

Then, for the GDP dataset, we dropped all NA values.

We merged the rankings dataset and players dataset to create the tennis dataset. We then extracted years (meaning, put it in DateTime format). Afterwards, we dropped ambiguous historical countries such as Yugoslavia (YUG) and URS (Soviet Union).

Additionally, we mapped the IOC country code of each player to the USDA (the GDP dataset) country name.

Then, we removed the aggregated region from the GDP dataset, such as “Asia Less Japan” and “Asia and Oceania”.

Following this step, we merged the tennis dataset with the GDP dataset using a left merge. 

We then imputed any remaining NaN value with the value “UNKNOWN”.

We created a distribution graph with player points and a distribution of the GDP. 

We also created a scatter plot between GDP (x-axis) vs. Player Points (y-axis).

Following this step, we noticed how skewed the scatter plot looked, so we decided to create a log scatter plot as well.

We created a box plot where we categorized GDP into four levels: low, mid-low, mid-high, and high. We placed these groups on the x-axis and player points on the y-axis. 

We made a scatter plot of county GDP (x-axis) vs. average player points for each country (y-axis).

Then, we found the correlation between GDP and average player points.


### Update on Timeline:

**Step 1: Data Acquisition and Organization** – *Target Completion: March 13, 2026* Completed by Maya Jenny and Luoxu Chen

**Step 2: Data Integration** – *Target Completion: March 13, 2026* - Completed by Luoxu Chen

**Step 3: Data Quality Assessment and Cleaning** – *Target Completion: March 27, 2026* - Completed by Luoxu Chen 

**Step 4: Exploratory Data Analysis** – *Target Completion: March 27, 2026* - Completed by Maya Jenny

**Step 5: Feature Engineering** – *Target Completion: April 3, 2026*  - Completed by Luoxu Chen

**Step 6: Model Preparation** – *Target Completion: April 17, 2026* - Maya Jenny

**Step 7: Model Training and Prediction** – *Target Completion: April 24, 2026* - Luoxu Chen

**Step 8: Model Evaluation** – *Target Completion: May 1, 2026* - Maya Jenny

**Step 9: Workflow Automation, Documentation, and Reproducibility** – *Target Completion: May 1, 2026* - Luoxu Chen 



### Changes to Project Plan

Our Milestone 2 feedback suggested that we enhance the depth of our data integration and analysis. To implement this recommendation, we incorporated a third dataset containing country-level GDP information. This addition allowed us to perform more meaningful operations by linking tennis players to economic indicators based on their country of origin.
As a result, our research question was refined to examine whether there is a relationship between a player’s country’s wealth and their success in professional tennis, as measured by match outcomes and overall rankings.
Beyond the inclusion of this dataset, no major changes to the workflow were deemed necessary. The integration process was straightforward, as the datasets shared a common country-level attribute, allowing for efficient merging and data cleaning.



### Challenges 

The integration between the GDP dataset and the player dataset presented several challenges due to inconsistencies in country formatting. The GDP dataset represented countries using full names, while the player dataset used three-letter country abbreviations. To address this, we created a mapping between country names and their corresponding abbreviations to ensure consistency across datasets.
Additionally, the GDP dataset included aggregated regional entries (e.g., “Asia”), which do not correspond to individual player nationalities. These entries were removed to maintain a consistent level of granularity. We also identified countries in the player dataset that no longer exist (e.g., Yugoslavia). Since these entities are not relevant to modern rankings (e.g., 2024), they were excluded from our analysis.
After standardizing country representations, we successfully merged the datasets based on country-level identifiers.
We also encountered issues with the dob (date of birth) column, which was stored in a non-standard float format (e.g., 19131122.0). To correct this, we converted the values to integers, then to strings, and finally parsed them into proper datetime objects. This allowed us to engineer a new feature representing player age at the ranking date in 2024. Age was then rounded to the nearest whole number to facilitate clearer aggregation and analysis.


### Individual Contributions 

##### Luoxu Chen: 
I was responsible for the core technical components of the project, including data integration, data cleaning, feature engineering, and workflow automation. I merged the rankings and player datasets to construct a unified tennis dataset, standardized date formats, and resolved inconsistencies in country representations by mapping IOC codes to GDP country names. I also handled data quality issues, such as removing obsolete country entries and converting improperly formatted date-of-birth values into usable datetime formats to engineer player age features.

Additionally, I implemented the integration of the GDP dataset, ensured proper handling of missing values, and prepared the dataset for modeling. I was also responsible for model training and prediction, as well as final workflow automation, documentation, and reproducibility of the project.

##### Maya Jenny:
