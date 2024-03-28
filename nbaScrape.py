import numpy as np
import pandas as pd
import requests
import time

pd.set_option('display.max_columns', None)

#headers to mimic a browser request and avoid blocking
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

#Initialize the DataFrame outside the loop
df = pd.DataFrame()

begin_time = time.time()
for y in years:
    stats_url = f'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season={y}&SeasonType=Regular%20Season&StatCategory=PTS'
    r = requests.get(url=stats_url, headers=api_header).json()
    table_headers = r['resultSet']['headers']
    nba_df = pd.DataFrame(r['resultSet']['rowSet'], columns=table_headers)
    year_df = pd.DataFrame({'Year': [y for _ in range(len(nba_df))]})
    full_df = pd.concat([year_df, nba_df], axis=1)
    
    #Accumulate data
    df = pd.concat([df, full_df], ignore_index=True)
    
    print(f'Finished collecting data for the {y} season.')
    lag = np.random.uniform(low=10, high=30)
    print(f'.....collecting..... {round(lag, 1)} seconds.')
    time.sleep(lag)

total_time = round(time.time() - begin_time, 2)
print(f'Data Collection Complete! Total run time: {total_time} seconds')

#save to CSV
df.to_csv('nba_data.csv', index=False)
print(df.head())  
