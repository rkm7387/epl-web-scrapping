# importing important libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup
import openpyxl

# url for web scrapping:
url = 'https://www.bbc.com/sport/football/premier-league/top-scorers'

# List of Columns for Excel
player_names = []
team_names = []
goals = []
assists = []
num_matches = []
shots = []


try:
    response = requests.get(url)
    response.raise_for_status()
except Exception as e:
    print(e)
else:
    soup = BeautifulSoup(response.content, 'html.parser')
    players = soup.find('tbody').find_all(
        'tr', class_='ssrcss-dhlz6k-TableRowBody e1icz100')
    for player in players:
        player_name = player.find(
            'div', class_='ssrcss-m6ah29-PlayerName e1n8xy5b1').get_text(strip=True)
        player_names.append(player_name)

        # Getting Team names:
        team_name = player.find(
            'div', class_='ssrcss-qvpga1-TeamsSummary e1n8xy5b0').get_text(strip=True)
        team_names.append(team_name)

        # Getting Goals:
        goal_scored = int(player.find(
            'div', class_='ssrcss-8k20kk-CellWrapper ef9ipf0').get_text(strip=True))
        goals.append(goal_scored)

        stats = player.find_all(
            'div', class_='ssrcss-150z8d-CellWrapper ef9ipf0')

        assist_made = int(stats[0].get_text(strip=True))
        assists.append(assist_made)

        matches_played = int(stats[2].get_text(strip=True))
        num_matches.append(matches_played)

        shots_taken = int(stats[-3].get_text(strip=True))
        shots.append(shots_taken)

    data = {
        'players': player_names,
        'team': team_names,
        'matches': num_matches,
        'goals': goals,
        'assists': assists,
        'shots': shots
    }

    # making datafram using pandas
    df_players = pd.DataFrame(data)

    # exporting dataframe into excel
    df_players.to_excel('Epl Top Scores.xlsx', index=False)
