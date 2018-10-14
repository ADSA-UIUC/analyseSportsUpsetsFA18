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
    elif (team == "ULM"):
        team = "Louisiana-Monroe"
    elif (team == "Kent"):
        team = "Kent State"
    elif (team == "MTSU"):
        team = "Middle Tennessee"
    elif (team == "Southern Miss"):
        team = "Southern Mississippi"
    elif (team == "NC State"):
        team = "North Carolina State"
    elif (team == "Florida Intl"):
        team = "Florida International"
    elif (team == "FL Atlantic"):
        team = "Florida Atlantic"
    elif (team == "Miami FL"):
        team = "Miami (Florida)"
    elif (team == "Miami OH"):
        team = "Miami (Ohio)"
    elif (team == "Hawaii"):
        team = "Hawai'i"
    elif ("N " in team and "Northern " not in team):        
        team = team.replace("N ", "Northern ")
    elif ("W " in team and "Western " not in team):        
        team = team.replace("W ", "Western ")
    elif ("E " in team and "Eastern " not in team):        
        team = team.replace("E ", "Eastern ")
    elif ("S " in team and "Southern " not in team):        
        team = team.replace("S ", "Southern ")
    elif ("C " in team and "Central " not in team):        
        team = team.replace("C ", "Central ")
    new_teams.append(team)

df['Team'] = pd.Series(new_teams)
print(df)