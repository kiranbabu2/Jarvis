from espncricinfo.summary import Summary
from espncricinfo.match import Match
import pandas as pd
import os
import time
import csv
import json
import github

df = pd.DataFrame()
arr = []
for match in Summary().match_ids:
    m = Match(match)
    if 'indian premier league' in m.description.lower():
        arr.append(match)
df['matches'] = arr
df.to_csv('data_extraction/current_matches.csv',index = False)

# g = github.Github('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')
# new_repo = g.get_user().get_repo('Jarvis')

# new_repo.create_file("current_matches.txt", "updating file", str(arr))
