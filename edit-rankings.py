import pandas as pd

df = pd.read_csv("./Data/2005/cf2005.csv")

ranking_group = df['Ranking Group Abbreviation']

df = df.drop(columns=['Code','Ranking Group'])

df2 = pd.read_csv("./Data/2005/team.csv")

teams = df['Team']
ranks = df["Rank"]

new_teams = []
new_ranks = []
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

ranking_group = df['Ranking Group Abbreviation']
modified_df = pd.DataFrame(columns=['Year','Team','Ranking Group Abbreviation','Date','Rank'])
count = 0
for j in range(len(ranking_group)):
    if (" ARG" == ranking_group[j]):
        modified_df.loc[count] = df.iloc[j]
        count += 1
modified_df = modified_df.drop(columns=['Year','Ranking Group Abbreviation'])
other_teams = df2['Name']
allGood = True
for name in new_teams:
    if (name in other_teams == False):
        allGood = False
        print(name)
modified_df['Team'] = pd.Series(new_teams)
if (allGood):
    modified_df.to_csv("rankings_2005.csv")
    print("Good")
else:
    print("Not completely synced")

