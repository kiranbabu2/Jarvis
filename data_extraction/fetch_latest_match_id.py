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

g = github.Github('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')
new_repo = g.get_user().get_repo('Jarvis')

with open('data_extraction/current_matches.csv', mode ='r')as file:
  data = file.read()
 
print(data)

new_repo.create_file("data_extraction/current_matches.csv", "updating file", str(df), branch= 'main')
