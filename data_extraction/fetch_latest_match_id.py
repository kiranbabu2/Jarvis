from espncricinfo.summary import Summary
from espncricinfo.match import Match
import pandas as pd
import os
import time
import csv
import json

df = pd.DataFrame()
arr = []
for match in Summary().match_ids:
    m = Match(match)
    if 'indian premier league' in m.description.lower():
        arr.append(match)
df['matches'] = arr
df.to_csv('current_matches.csv',index = False)