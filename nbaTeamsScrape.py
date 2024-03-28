import numpy as np
import pandas as pd
import requests
import time

pd.set_option('display.max_columns', None)

#Headers to mimic a browser request and avoid blocking
api_header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'stats.nba.com',
    'Origin': 'https://www.nba.com',
    'Referer': 'https://www.nba.com/',
    'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

years = ['2018-19', '2019-20', '2020-21', '2021-22', '2022-23', '2023-24']
team_name_to_abbreviation = {
    'Atlanta Hawks': 'ATL', 'Boston Celtics': 'BOS', 'Brooklyn Nets': 'BKN',
    'Charlotte Hornets': 'CHA', 'Chicago Bulls': 'CHI', 'Cleveland Cavaliers': 'CLE',
    'Dallas Mavericks': 'DAL', 'Denver Nuggets': 'DEN', 'Detroit Pistons': 'DET',
    'Golden State Warriors': 'GSW', 'Houston Rockets': 'HOU', 'Indiana Pacers': 'IND',
    'LA Clippers': 'LAC', 'Los Angeles Lakers': 'LAL', 'Memphis Grizzlies': 'MEM',
    'Miami Heat': 'MIA', 'Milwaukee Bucks': 'MIL', 'Minnesota Timberwolves': 'MIN',
    'New Orleans Pelicans': 'NOP', 'New York Knicks': 'NYK', 'Oklahoma City Thunder': 'OKC',
    'Orlando Magic': 'ORL', 'Philadelphia 76ers': 'PHI', 'Phoenix Suns': 'PHX',
    'Portland Trail Blazers': 'POR', 'Sacramento Kings': 'SAC', 'San Antonio Spurs': 'SAS',
    'Toronto Raptors': 'TOR', 'Utah Jazz': 'UTA', 'Washington Wizards': 'WAS',
    }

#Initialize the DataFrame outside the loop
team_df = pd.DataFrame()

begin_time = time.time()
for y in years:
    #Adjust the URL to fetch team data instead
    stats_url = f'https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&Height=&ISTRound=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season={y}&SeasonSegment=&SeasonType=Regular%20Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision='
    r = requests.get(url=stats_url, headers=api_header).json()
    teams_data = r['resultSets'][0]['rowSet']
    columns = r['resultSets'][0]['headers']
    
    #Temporary DataFrame for this year's data
    temp_df = pd.DataFrame(teams_data, columns=columns)
    
    #Select and rename necessary columns, convert team names to abbreviations
    temp_df = temp_df[['TEAM_NAME', 'W', 'L']].copy()
    temp_df['TEAM_NAME'] = temp_df['TEAM_NAME'].map(team_name_to_abbreviation)
    temp_df['SEASON'] = y  # Add a column for the season
    
    #Accumulate data
    team_df = pd.concat([team_df, temp_df], ignore_index=True)
    
    print(f'Finished collecting data for the {y} season.')
    lag = np.random.uniform(low=5, high=15)  #Adjust sleep range as needed
    time.sleep(lag)

total_time = round(time.time() - begin_time, 2)
print(f'Data Collection Complete! Total run time: {total_time} seconds')

#Save to CSV
team_df.to_csv('nba_team_data.csv', index=False)
print(team_df.head())
