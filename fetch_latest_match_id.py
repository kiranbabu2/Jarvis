from espncricinfo.summary import Summary
from espncricinfo.match import Match
import pandas as pd
import github
from github_helper import *

df = pd.DataFrame()
arr = []
for match in Summary().match_ids:
    try:
        m = Match(match)
        if 'indian premier league' in m.description.lower():
            arr.append(match)
    except Exception as e:
        print(match, e)
        pass
df['matches'] = arr
df.to_csv('./current_matches.csv',index = False)
data = get_csv_contents('./current_matches.csv')
save_file(repo,data,'./current_matches.csv','Added latest matches')