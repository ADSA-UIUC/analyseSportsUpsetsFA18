import pandas as pd

years = ['2005', '2006', '2008', '2009', '2010', '2011', '2012', '2013']

columns = ["Game Code", "Winning Team Code", "Losing Team Code", "Winning Team Points", "Losing Team Points", "Winning Team Seed", "Losing Team Seed", "Upset Factor"]
games = pd.DataFrame(columns= columns)

for year in years:
	team_game_statistics = pd.read_csv('./Data/' + year + '/team-game-statistics.csv')
	used_games = []
	for index, row in team_game_statistics.iterrows():
		if row["Game Code"] not in used_games:
			new_row = pd.DataFrame(columns=columns)
			used_games.append(row["Game Code"])
			new_row.loc[0, "Game Code"] = row["Game Code"]
			new_row.loc[0, "Winning Team Code"] = row["Team Code"]
			new_row.loc[0, "Winning Team Points"] = row["Points"]

			games = games.append(new_row, ignore_index=True)
		else:
			row_values = games.loc[games['Game Code'] == row['Game Code']]
			edit_row_index = games.index[games['Game Code'] == row['Game Code']]
			if row_values.iloc[0]['Winning Team Points'] < row['Points']:
				games.loc[edit_row_index, 'Losing Team Points'] = row_values.iloc[0]['Winning Team Points']
				games.loc[edit_row_index, 'Winning Team Points'] = row['Points']
				games.loc[edit_row_index, 'Losing Team Code'] = row_values.iloc[0]['Winning Team Code']
				games.loc[edit_row_index, 'Winning Team Code'] = row['Team Code']
			else:
				games.loc[edit_row_index, 'Losing Team Points'] = row['Points']
				games.loc[edit_row_index, 'Losing Team Code'] = row['Team Code']
	print(games)

		


			




