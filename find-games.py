import pandas as pd

years = ['2005', '2006', '2008', '2009', '2010', '2011', '2012', '2013']

games = pd.DataFrame(columns=["Game Code", "Winning Team Code", "Losing Team Code", "Winning Team Points", "Losing Team Points", "Winning Team Seed", "Losing Team Seed", "Upset Factor"])

for year in years:
	team_statistics = pd.read_csv('./Data/' + year + '/cfbstats-com-' + year + '-1-5-0/team-game-statistics.csv')
	print(team_statistics)