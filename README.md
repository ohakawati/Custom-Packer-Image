# NBA Data Scrape & Analytics using BigQuery and Looker

Using a localalized python script we can scrape data directly from NBA.com and load that data into Bigquery. From Bigquery we can perform customized sql queries in order to gain visualized insights in the BI tool Looker.
![NBA DataScrape](https://github.com/ohakawati/NBA-Analytics/assets/89810188/2701cb97-ade5-46a8-b58f-c2df308a06cf)


# 1. We will need a Bigquery service account with the Big Query admin role in order to read and write data to our big query tables
<img width="1148" alt="Screenshot 2024-03-27 at 11 41 52 PM" src="https://github.com/ohakawati/NBA-Analytics/assets/89810188/631b71da-e511-47ed-b76d-059575e0cc8f">
Ensure you download the credentials and store those credentials securely, for the sake of this demo we have the credentials in the same directory so its easy for the python script to reference.


# 2. Download numpy and pandas in your python virtual env
<img width="703" alt="Screenshot 2024-03-27 at 11 45 21 PM" src="https://github.com/ohakawati/NBA-Analytics/assets/89810188/4aca0b37-9f62-4e59-8d59-3d970212495c">

# 3. Run the nbascrape.py and nbateamsscrape.py, output should give you two csv files popluated with data
For these scripts we utilize numpy in order to handle any denied requests made to nba.com, we utilize pandas in order to view the data as a dataframe. From there the data is populated into a csv the will be utilized in our next step when running our Big Query python scripts. In the nbateamsscrape.py you will notice that we had to map team names to their apprpriate abbreviation. This is done so that the data is consistent in Big query with the team abbriviations collected in the nbascrape.py. The teams data is not directly utilized in this project however team performance can be utilized later on when determining relationships between player performance on that team.
<img width="187" alt="Screenshot 2024-03-27 at 11 53 49 PM" src="https://github.com/ohakawati/NBA-Analytics/assets/89810188/27bc1c30-eda7-4245-a154-5afdfe1806b4">
<img width="1134" alt="Screenshot 2024-03-27 at 11 54 28 PM" src="https://github.com/ohakawati/NBA-Analytics/assets/89810188/e276c3db-b9bd-4249-98c2-a53b2cc1b58d">
<img width="1116" alt="Screenshot 2024-03-27 at 11 54 40 PM" src="https://github.com/ohakawati/NBA-Analytics/assets/89810188/c60f63ed-6df6-4ca4-a5d1-0c1046ae0155">

# 4. With our csv stored locally, we run the bigquery.py and bigqueryteams.py script
<img width="1357" alt="Screenshot 2024-03-28 at 12 00 13 AM" src="https://github.com/ohakawati/NBA-Analytics/assets/89810188/c93a64b6-7920-42ad-8572-33dd655c7274">
Before running this script you need to import gcp bigquery in your python venv. In this script we generate the bq schema from the csv headers, create the dataset and table, and finally popluate the table with the data located in your csv. 

# 5. Once your BigQuery table is popluated we can write SQL queries to gain insights on that data
<img width="1051" alt="Screenshot 2024-03-28 at 12 03 38 AM" src="https://github.com/ohakawati/NBA-Analytics/assets/89810188/753921f7-5c44-45b8-841b-1213f4b1b93c">
In the query editor feel free to pull insights with whatever queries you want, for this specifc project we are interested in calculating a player improvement score based on previous performance and visualizing this is looker to better understand a players potential trajectory in the upcoming season. In this query we look at the main indicators of a well performing player and those are points, asists, and rebounds. Obviously it much more complicated than this but it just gives you a baseline into player performance. The improvment score is normalized to be a double within the range of 0(no improvement) - 1(max improvement). After running this query we can explore directly through the BigQuery UI which will then take you to looker.
<img width="1035" alt="Screenshot 2024-03-28 at 12 09 28 AM" src="https://github.com/ohakawati/NBA-Analytics/assets/89810188/a1b2896d-d467-49d5-90e3-31a9de3786a7">

# 6. Visulaize your data
In looker you can include a number of different charts, graphs, and numerics in order to tell the story. Here is the Dashboard I made to visualize this.
<img width="764" alt="Screenshot 2024-03-28 at 12 13 45 AM" src="https://github.com/ohakawati/NBA-Analytics/assets/89810188/c353a8e0-750d-47d4-b2ec-646bb2583d56">
<img width="772" alt="Screenshot 2024-03-28 at 12 12 17 AM" src="https://github.com/ohakawati/NBA-Analytics/assets/89810188/0c0a92f9-22ec-45cc-a1d6-d56214abaaf0">
<img width="766" alt="Screenshot 2024-03-28 at 12 12 57 AM" src="https://github.com/ohakawati/NBA-Analytics/assets/89810188/5e09d3ed-ed1c-492a-b7d6-02e238da7c6f">
<img width="770" alt="Screenshot 2024-03-28 at 12 13 10 AM" src="https://github.com/ohakawati/NBA-Analytics/assets/89810188/d2febd09-3983-4f69-8ae7-f0818a55166f">

# 7. Save your Dashboard and create different views
You now have a starter dashboard. You can go back to the python scripts and manipulate the request to scrape other data that you desire. You can extent the amount of season data collected(2018-2023 in our case), you can include playoff data, specific game data, and team data. There is endless possiblities you can do with this data, you can create much more detailed and visual charts or even train your own BigQuery ML model on this data.












