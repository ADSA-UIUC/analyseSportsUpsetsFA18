import pandas as pd
import datetime

games = pd.read_csv("./Data/2005/game.csv")
rankings = pd.read_csv("./Data/2005/rankings_2005.csv")
teams = pd.read_csv("./Data/2005/team.csv")
team_game_stats = pd.read_csv("./Data/2005/team-game-statistics.csv")

'''
creates a new column in rankings data called 'Datetime', which contains datetime objects that can be compared
'''
def rankings_dates_to_datetime():
	current_dates = rankings['Date']
	dates = []
	for date in current_dates:
		date = str(date)
		year = int(date[0:4])
		month = int(date[4:6])
		day = int(date[6:])
		dates.append(datetime.datetime(year, month, day))
	rankings['Datetime'] = dates

'''
creates a new column in game data called 'Datetime', which contains datetime objects that can be compared
'''
def game_dates_to_datetime():
	current_dates = games['Date']
	dates = []
	for date in current_dates:
		year = int(date[6:])
		month = int(date[0:2])
		day = int(date[3:5])
		dates.append(datetime.datetime(year, month, day))
	games['Datetime'] = dates

'''
Finds team name that corresponds to team code that is passed into function.
Returns a string.
'''
def match_team_code_to_team(team_code):
	team_names = teams['Name']
	team_name = list(teams[teams['Team Code'] == team_code]['Name'])
	return team_name[0]

'''
Given the date of the game as a datetime object, finds and returns the date of the most recent ranking.
Returns a datetime object.
'''
def match_game_date_to_ranking_date(game_date):
	ranking_dates = list(rankings['Datetime'])
	for i in range(len(ranking_dates)):
		if (ranking_dates[i] > game_date):
			return ranking_dates[i - 1]
	return sorted(list(rankings['Datetime']))[-1]

'''
Retrieves the ranking for a team given the team code of the team and the date of the game.
Date must be given as a datetime object
Returns a default ranking if team is not ranked.
'''
def get_team_ranking(team_code, game_date, default_ranking):
	team_name = match_team_code_to_team(team_code)
	ranking_date = match_game_date_to_ranking_date(game_date)
	all_rankings_for_date = rankings[rankings['Datetime'] == ranking_date]
	if team_name not in list(all_rankings_for_date['Team']):
		return default_ranking
	else:
		return list(all_rankings_for_date[all_rankings_for_date['Team'] == team_name]['Rank'])[0]

'''
Gets the number of points scored by a team given the team code of the home team and the game code
'''
def get_team_points(team_code, game_code):
	all_team_games = team_game_stats[team_game_stats['Team Code'] == team_code]
	specified_game = all_team_games[all_team_games['Game Code'] == game_code]
	return list(specified_game['Points'])[0]

'''
Given a game code, returns 'Home' if home team won, or 'Away' if away team won.
'''
def determine_winning_team(game_code):
	game = games[games['Game Code'] == game_code]
	home_team_code = list(game['Home Team Code'])[0]
	away_team_code = list(game['Visit Team Code'])[0]
	home_team_points = get_team_points(home_team_code, game_code)
	away_team_points = get_team_points(away_team_code, game_code)
	if (home_team_points > away_team_points):
		return "Home"
	else:
		return "Away"

'''
Returns the date of the game given a game code
'''
def get_game_date(game_code):
	current_game = games[games['Game Code'] == game_code]
	return list(current_game['Datetime'])[0]

rankings_dates_to_datetime()
game_dates_to_datetime()
winning_team_ranks = []
losing_team_ranks = []
for index, game in games.iterrows():
	winning_team = determine_winning_team(game['Game Code'])
	if (winning_team == "Home"):
		winning_team_ranks.append(get_team_ranking(game['Home Team Code'], game['Datetime'], 130))
		losing_team_ranks.append(get_team_ranking(game['Visit Team Code'], game['Datetime'], 130))
	else:
		winning_team_ranks.append(get_team_ranking(game['Visit Team Code'], game['Datetime'], 130))
		losing_team_ranks.append(get_team_ranking(game['Home Team Code'], game['Datetime'], 130))
	
