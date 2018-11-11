import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets.samples_generator import make_blobs

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

'''
Returns tuple in the form (winning_team_code, losing_team_code)
'''
def get_winning_team_and_losing_team(game_code):
	current_game = team_game_stats[team_game_stats['Game Code'] == game_code]
	team_codes = list(current_game['Team Code'])
	team_1_score = int(current_game[current_game['Team Code'] == team_codes[0]]['Points'])
	team_2_score = int(current_game[current_game['Team Code'] == team_codes[1]]['Points'])
	if team_1_score > team_2_score:
		return (team_codes[0], team_codes[1])
	else:
		return (team_codes[1], team_codes[0])

'''
Given game codes of upsets, creates csv files that relate to the winner of the game
'''
def create_winning_team_csv_files(game_codes):
	winning_team_stats_for_game = pd.DataFrame()
	winning_team_average_stats = pd.DataFrame()
	home_or_away = []
	for game_code in game_codes:
		winning_team_code = get_winning_team_and_losing_team(game_code)[0]
		home_team_code = str(game_code)[len(str(game_code))-12:len(str(game_code))-8]
		if winning_team_code == int(home_team_code):
			home_or_away.append("Home")
		else:
			home_or_away.append("Away")
		game_stats = team_game_stats[team_game_stats["Game Code"] == game_code]
		game_stats_winning_team = game_stats[game_stats["Team Code"] == winning_team_code]
		winning_team_stats_for_game = winning_team_stats_for_game.append(game_stats_winning_team)
		all_game_stats_for_winning_team = team_game_stats[team_game_stats["Team Code"] == winning_team_code]
		to_average = all_game_stats_for_winning_team[all_game_stats_for_winning_team["Game Code"] != game_code]
		averages = pd.DataFrame(to_average.mean())
		averages = averages.transpose()
		averages["Game Code"] = game_code
		averages["Team Code"] = winning_team_code
		winning_team_average_stats = winning_team_average_stats.append(averages)
	winning_team_average_stats = winning_team_average_stats.add_prefix("Average ")
	new_columns = winning_team_average_stats.columns.values
	new_columns[0] = 'Team Code'
	new_columns[1] = 'Game Code'
	winning_team_average_stats.columns = new_columns
	winning_team_stats_for_game["Home or Away"] = home_or_away
	winning_team_average_stats["Home or Away"] = home_or_away
	print(winning_team_stats_for_game)
	print(winning_team_average_stats)

'''
Given game codes of upsets, creates csv files that relate to the winner of the game
'''
def create_losing_team_csv_files(game_codes):
	losing_team_stats_for_game = pd.DataFrame()
	losing_team_average_stats = pd.DataFrame()
	home_or_away = []
	for game_code in game_codes:
		losing_team_code = get_winning_team_and_losing_team(game_code)[1]
		home_team_code = str(game_code)[len(str(game_code))-12:len(str(game_code))-8]
		if losing_team_code == int(home_team_code):
			home_or_away.append("Home")
		else:
			home_or_away.append("Away")
		game_stats = team_game_stats[team_game_stats["Game Code"] == game_code]
		game_stats_losing_team = game_stats[game_stats["Team Code"] == losing_team_code]
		losing_team_stats_for_game = losing_team_stats_for_game.append(game_stats_losing_team)
		all_game_stats_for_losing_team = team_game_stats[team_game_stats["Team Code"] == losing_team_code]
		to_average = all_game_stats_for_losing_team[all_game_stats_for_losing_team["Game Code"] != game_code]
		averages = pd.DataFrame(to_average.mean())
		averages = averages.transpose()
		averages["Game Code"] = game_code
		averages["Team Code"] = losing_team_code
		losing_team_average_stats = losing_team_average_stats.append(averages)
	losing_team_average_stats = losing_team_average_stats.add_prefix("Average ")
	new_columns = losing_team_average_stats.columns.values
	new_columns[0] = 'Team Code'
	new_columns[1] = 'Game Code'
	losing_team_average_stats.columns = new_columns
	losing_team_stats_for_game["Home or Away"] = home_or_away
	losing_team_average_stats["Home or Away"] = home_or_away
	print(losing_team_stats_for_game)
	print(losing_team_average_stats)


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
plotlist = np.column_stack((winning_team_ranks, losing_team_ranks))
 
game_code_list = games['Game Code'].tolist()
 
kmeans = KMeans(n_clusters=20)
kmeans.fit(plotlist)
y_kmeans = kmeans.predict(plotlist)
 
 
plt.scatter(plotlist[:, 0], plotlist[:, 1], c=y_kmeans, s=50, cmap='viridis')
 
for i in range(len(game_code_list)):
    plt.annotate(game_code_list[i], (plotlist[i, 0], plotlist[i, 1]))
 
centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
 
for i in range(len(centers)):
    plt.annotate(str(i-1), (centers[i, 0], centers[i, 1]))
 
mydict = {i: np.where(kmeans.labels_ == i)[0] for i in range(kmeans.n_clusters)}
 
dictlist = []
for key, value in mydict.items():
    temp = [key,value]
    dictlist.append(temp)
games_in_cluster = dictlist[0]
for j in games_in_cluster[1]:
	print(game_code_list[j])
''' 
for i in dictlist:
    print('#############')
    print('Cluster ' + str(i[0]) + ';')
    for j in i[1]:
        print(game_code_list[j])
''' 
plt.show()