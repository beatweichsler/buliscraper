import requests
from lxml import html, etree
import pandas as pd

def scrape_games(): 

    #Initialize Dataframe
    column_names = ["game_day", "home_team", "home_score", "home_points", "away_team", "away_score", "away_points"]
    df = pd.DataFrame(columns=column_names)

    #Scrape Game Data and insert into dataframe
    for i in range(1, 6): 
        response = requests.get('https://www.bundesliga.com/de/bundesliga/spieltag/2023-2024/{}'.format(i))
        tree = html.fromstring(response.content)

        for j in range(1, 10):
            home_team = tree.xpath('//*[@id="fixtures"]/fixturescomponent/div/div[{}]/a/match-fixture/match-team[1]/div/div'.format(j))
            home_score = tree.xpath('//*[@id="fixtures"]/fixturescomponent/div/div[{}]/a/match-fixture/score-bug/div/div[1]/div[2]'.format(j))

            away_score = tree.xpath('//*[@id="fixtures"]/fixturescomponent/div/div[{}]/a/match-fixture/score-bug/div/div[2]/div[2]'.format(j))
            away_team = tree.xpath('//*[@id="fixtures"]/fixturescomponent/div/div[{}]/a/match-fixture/match-team[2]/div/div'.format(j))

            if home_score[0].text_content().strip() == away_score[0].text_content().strip():
                home_points = 1
                away_points = 1

            elif home_score[0].text_content().strip() > away_score[0].text_content().strip():
                home_points = 3
                away_points = 0
            else:
                away_points = 3
                home_points = 0

            new_row = {"game_day": i, "home_team": home_team[0].text_content().strip(), "home_score": home_score[0].text_content().strip(), "home_points": home_points, "away_team": away_team[0].text_content().strip(), "away_score": away_score[0].text_content().strip(), "away_points": away_points}
            df = df._append(new_row, ignore_index=True)
    
    return df

def calculate_standings(games):


    games['home_points'] = games['home_points'].astype(int)
    games['away_points'] = games['away_points'].astype(int)
    games['home_score'] = games['home_score'].astype(int)
    games['away_score'] = games['away_score'].astype(int)

    #Initialize Dataframe
    column_names = ["team", "points", "goal_made", "goal_received", "goal_difference"]
    standings = pd.DataFrame(columns=column_names)

    #Insert all Team Names, inserted from games
    for i in range(0,9):
        new_row = pd.DataFrame({'team': [games.iloc[i]['home_team']]})
        standings = standings._append(new_row, ignore_index=True)
        new_row = pd.DataFrame({'team': [games.iloc[i]['away_team']]})
        standings = standings._append(new_row, ignore_index=True)


    for standings_index, standings_row in standings.iterrows():
        points = 0
        goal_made = 0
        goal_received = 0

        for games_index, games_row in games.iterrows():
            if standings_row['team'] == games_row['home_team']:
                points += games_row['home_points']
                goal_made += games_row['home_score']
                goal_received += games_row['away_score']
            
            if standings_row['team'] == games_row['away_team']:
                points += games_row['away_points']
                goal_made += games_row['away_score']
                goal_received += games_row['home_score']
        
        standings.loc[standings_index, 'points'] = points
        standings.loc[standings_index, 'goal_made'] = goal_made
        standings.loc[standings_index, 'goal_received'] = goal_received
        standings.loc[standings_index, 'goal_difference'] = (goal_made - goal_received)


    standings.sort_values(by=['points', 'goal_difference', 'goal_made'], ascending=[False, False, False], inplace=True)
    return standings





