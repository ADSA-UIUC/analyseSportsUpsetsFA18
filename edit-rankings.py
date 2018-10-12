import pandas as pd

df = pd.read_csv("./Data/2005/cf2005.csv")
df = df.drop(columns=['Code','Ranking Group Abbreviation','Ranking Group'])
teams = df['Team']
new_teams = []
for i in range(len(teams)):
    team = teams[i].strip()
    if (" St" in team and " State" not in team):        
        team = team.replace(" St", " State")
    elif (team == "ULL"):
        team = "Louisiana-Lafayette"
    elif (team == "Florida Intl"):
        team = "Florida International"
    elif (team == "FL Atlantic"):
        team = "Florida Atlantic"
    elif (team == "Miami FL"):
        team = "Miami (Florida)"
    new_teams.append(team)
df['Team'] = pd.Series(new_teams)
print(df)