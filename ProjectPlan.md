# Project Plan for Luoxu Chen and Maya Jenny 

## Overview: 
The goal of this project is to analyze how player characteristics relate to ATP rankings and to explore whether these characteristics can help predict a player’s ranking performance. By integrating two complementary datasets: one containing ATP player information (such as height, handedness, country, and date of birth) and another containing historical ATP ranking data. The project aims to examine patterns between player attributes and ranking outcomes. Understanding these relationships can provide insight into how physical and demographic characteristics may influence success in professional tennis.

To achieve this goal, the project will first clean and preprocess both datasets, ensuring that variables such as player identifiers, dates, and missing values are handled appropriately. The datasets will then be merged using common identifiers linking player information with ranking history. After integration, exploratory data analysis will be conducted to investigate trends between player characteristics and rankings. Additional features such as player age at the time of ranking will be calculated to enhance the analysis.

Finally, a predictive modeling approach will be implemented to examine whether player characteristics can be used to estimate ranking outcomes. Statistical and machine learning techniques, such as linear regression, will be used to model the relationship between player attributes and ranking performance. The results will provide insights into the factors that may influence ATP rankings and highlight how data analysis can be used to study performance patterns in professional tennis.


## Team: 

Maya Jenny will be responsible for cleaning the data in the dataset, early data visualization insight, and evaluating the model Luoxu creates. Luoxu Chen will be responsible for data engineering, modeling the data with a train-test split, and result prediction and visualization.

## Research / Business Question:
Can we create a predictive model on a player’s ranking in 2024 based on characteristics of the player, such as height, age, and country?


## Datasets

**Datasets:** https://github.com/JeffSackmann/tennis_atp 

**First Dataset:** 
ATP Players
https://github.com/JeffSackmann/tennis_atp/blob/master/atp_players.csv 

This dataset contains demographic and physical information about professional ATP tennis players. The variables include player identifiers, first and last names, handedness, date of birth, nationality (IOC country code), and height. These attributes provide information about player characteristics that may influence performance in professional tennis. In this project, the dataset will be used to analyze how player characteristics such as age, height, and handedness relate to ATP ranking outcomes. The dataset will also be used to calculate additional variables, such as player age at the time of each ranking observation.

**Second Dataset** 
ATP Rankings 
https://github.com/JeffSackmann/tennis_atp/blob/master/atp_rankings_current.csv 

This dataset contains ATP player rankings recorded throughout the year 2024. Each record includes the ranking date, player identifier, ranking position, and ranking points. Although the dataset only covers the 2024 season, rankings are recorded on multiple dates throughout the year, allowing us to observe changes in ranking positions over time. In this project, the ranking dataset will serve as the primary measure of player performance. It will be integrated with the player information dataset using player identifiers so that player characteristics can be analyzed alongside ranking outcomes.

These two datasets both share the common attribute of player ID, where each player gets a unique numerical id. We are able to merge on this attribute. 


## Timeline
This project will follow a structured data lifecycle consisting of data acquisition, integration, cleaning, analysis, modeling, and documentation. GitHub will be used for version control and collaboration, and all work will be documented in Markdown to ensure transparency and reproducibility. Each team member will contribute commits to the repository to demonstrate individual contributions.

**Step 1: Data Acquisition and Organization** – Target Completion: March 13, 2026
Both team members will collect the two datasets (ATP player dataset and ATP ranking dataset) from the Jeff Sackmann tennis repository. Files will be stored as CSV files in the project repository and organized into folders for raw data, processed data, and analysis scripts.

**Step 2: Data Integration – Target Completion**: March 13, 2026 
The datasets will be merged using Python and Pandas by linking player identifiers. This step will ensure that player attributes and ranking history are combined into a unified dataset.

**Step 3: Data Quality Assessment and Cleaning** – Target Completion: March 27, 2026
The team will assess missing values, duplicates, and formatting issues. Cleaning methods will include handling missing values, correcting inconsistent data types, and verifying valid ranges for variables such as ranking and height.

**Step 4: Exploratory Data Analysis** – Target Completion: March 27, 2026
Descriptive statistics and visualizations such as histograms, box plots, and summary statistics (mean, median, and distribution patterns) will be generated to understand the structure of the data.

**Step 5: Feature Engineering** – Target Completion: April 3, 2026
New variables will be created, including calculating player age based on ranking date and date of birth. Categorical variables such as handedness will be converted into numerical formats for modeling.

**Step 6: Model Preparation** – Target Completion: April 17, 2026
The dataset will be split into training and testing sets to prepare for predictive modeling.

**Step 7: Model Training and Prediction** – Target Completion: April 24, 2026
A predictive model (such as linear regression) will be trained to estimate ranking outcomes using player characteristics. Predictions will be generated using the testing dataset.

**Step 8: Model Evaluation** – Target Completion: May 1, 2026
Model performance will be evaluated using metrics such as R² and RMSE to determine how well player characteristics explain ranking outcomes.

**Step 9: Workflow Automation, Documentation, and Reproducibility** – Target Completion: May 1, 2026
The project workflow will be automated through structured scripts to ensure reproducibility. Metadata and documentation will be provided to describe datasets, variables, and analysis steps so that others can replicate the project.

Throughout the project, ethical considerations, licensing requirements, and proper attribution for the datasets will be documented to ensure responsible data usage.


## Constraint: 

One limitation of this project is that the datasets are compiled from publicly available tennis records and may contain incomplete or missing information for some players or time periods. For example, certain player attributes such as height, handedness, or birth dates may not be available for all athletes, which could reduce the number of observations usable for analysis. Additionally, rankings data is recorded periodically rather than continuously, meaning that a player’s ranking may not perfectly reflect their exact competitive level at every point in time.

Another constraint is related to data provenance. The dataset used in this project was compiled by Jeff Sackmann from multiple tennis statistics sources and historical records. While it is widely used for academic and sports analytics research, it is not an official ATP dataset and may contain minor inconsistencies or errors due to aggregation from different sources.

There are also licensing considerations. The dataset is distributed under a Creative Commons Attribution-NonCommercial-ShareAlike license, meaning it can be used for research and educational purposes but cannot be used for commercial applications without permission. 

Finally, the project focuses only on the variables available in the dataset, such as player height, age, and handedness. Other factors that may influence rankings, such as injuries, coaching changes, training conditions, or psychological factors, are not captured in the data, which may limit the predictive power of the analysis.



## Gaps: 

Future topics such as workflow automation, reproducibility, and metadata documentation will help ensure that the data processing pipeline is organized, transparent, and reproducible. As these topics are introduced, the project workflow may be refined to improve data management and documentation.
