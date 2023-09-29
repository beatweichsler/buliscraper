import requests
from lxml import html, etree
import pandas as pd


data = {
    "game_day": [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    "home_team": ["SV Werder Bremen", "VfB Stuttgart", "FC Augsburg", "TSG Hoffenheim", "VfL Wolfsburg", "Bayer 04 Leverkusen", "Borussia Dortmund", "1. FC Union Berlin", "Eintracht Frankfurt", "RB Leipzig", "SV Darmstadt 98", "1. FC Heidenheim 1846", "VfL Bochum 1848", "1. FC Köln", "Sport-Club Freiburg", "Borussia Mönchengladbach", "1. FSV Mainz 05", "FC Bayern München", "Borussia Dortmund", "VfB Stuttgart", "FC Augsburg", "SV Werder Bremen", "TSG Hoffenheim", "Bayer 04 Leverkusen", "Borussia Mönchengladbach", "Eintracht Frankfurt", "1. FC Union Berlin", "FC Bayern München", "1. FC Köln", "1. FSV Mainz 05", "VfL Wolfsburg", "Sport-Club Freiburg", "RB Leipzig", "VfL Bochum 1848", "1. FC Heidenheim 1846", "SV Darmstadt 98", "VfB Stuttgart", "FC Augsburg", "Borussia Mönchengladbach", "1. FC Union Berlin", "Borussia Dortmund", "FC Bayern München", "SV Werder Bremen", "Bayer 04 Leverkusen", "Eintracht Frankfurt"],
    "home_score": [0, 5, 4, 1, 2, 3, 1, 4, 1, 5, 1, 2, 1, 1, 1, 0, 1, 3, 2, 5, 2, 4, 3, 5, 1, 1, 0, 2, 1, 1, 2, 2, 3, 1, 4, 3, 3, 2, 0, 0, 1, 7, 2, 4, 0],
    "home_points": [0, 3, 1, 0, 3, 3, 3, 3, 3, 3, 0, 0, 1, 0, 3, 0, 1, 3, 1, 3, 1, 3, 3, 3, 0, 1, 0, 1, 0, 0, 3, 0, 3, 1, 3, 1, 3, 3, 0, 0, 3, 3, 3, 3, 1],
    "away_team": ["FC Bayern München", "VfL Bochum 1848", "Borussia Mönchengladbach", "Sport-Club Freiburg", "1. FC Heidenheim 1846", "RB Leipzig", "1. FC Köln", "1. FSV Mainz 05", "SV Darmstadt 98", "VfB Stuttgart", "1. FC Union Berlin", "TSG Hoffenheim", "Borussia Dortmund", "VfL Wolfsburg", "SV Werder Bremen", "Bayer 04 Leverkusen", "Eintracht Frankfurt", "FC Augsburg", "1. FC Heidenheim 1846", "Sport-Club Freiburg", "VfL Bochum 1848", "1. FSV Mainz 05", "VfL Wolfsburg", "SV Darmstadt 98", "FC Bayern München", "1. FC Köln", "RB Leipzig", "Bayer 04 Leverkusen", "TSG Hoffenheim", "VfB Stuttgart", "1. FC Union Berlin", "Borussia Dortmund", "FC Augsburg", "Eintracht Frankfurt", "SV Werder Bremen", "Borussia Mönchengladbach", "SV Darmstadt 98", "1. FSV Mainz 05", "RB Leipzig", "TSG Hoffenheim", "VfL Wolfsburg", "VfL Bochum 1848", "1. FC Köln", "1. FC Heidenheim 1846", "Sport-Club Freiburg"],
    "away_score": [4, 0, 4, 2, 0, 2, 0, 1, 0, 1, 4, 3, 1, 2, 0, 3, 1, 1, 2, 0, 2, 0, 1, 1, 2, 1, 3, 2, 3, 3, 1, 4, 0, 1, 2, 3, 1, 1, 1, 2, 0, 0, 1, 1, 0],
    "away_points": [3, 0, 1, 3, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 0, 3, 1, 0, 1, 0, 1, 0, 0, 0, 3, 1, 3, 1, 3, 3, 0, 3, 0, 1, 0, 1, 0, 0, 3, 3, 0, 0, 0, 0, 1]
}

games = pd.DataFrame(data)

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
print(standings)   