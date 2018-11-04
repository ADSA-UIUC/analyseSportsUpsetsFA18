import pandas as pd
import datetime

df_games = pd.read_csv("./Data/2005/game.csv")
df_rankings = pd.read_csv("./Data/2005/rankings_2005.csv")

def _editDateFormatOfGameFile(date):
	year = int(date[6:])
	month = int(date[3,5])
	day = int(date[:2])
	return datetime.datetime(year, month, day) 

def _editDateFormatOfRankingFile(date):
	year = int(date[:4])
	month = int(date[4:6])
	day = int(date[6:])
	return datetime.datetime(year, month, day)

def editDateFormatOfGameFile():
	dates = df_games['Date']
	new_dates = []
	for date in dates:
		new_dates = _editDateFormatOfGameFile(date)
	return new_dates

def editDateFormatOfRankingFile():
	dates = df_rankings['Date']
	new_dates = []
	for date in dates:
		new_dates = _editDateFormatOfRankingFile(date)
	return new_dates

def findMostRecent

