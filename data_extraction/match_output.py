from espncricinfo.summary import Summary
from espncricinfo.match import Match
import pandas as pd
import os
import time
import csv
import json
import github

# match_id = '1339606'

# for match in Summary().match_ids:
#     print(match, Match(match).description)
path = "./data/"
isExist = os.path.exists(path)
if not isExist:
    os.makedirs(path)

def get_team_from_id(m,bat_id):
    print(bat_id)
    if m.team_1_id==bat_id:
        return m.team_1_abbreviation
    elif m.team_2_id==bat_id:
        return m.team_2_abbreviation
    else:
        return "NA"
    
def represents_int(s):
    try: 
        int(s)
    except ValueError:
        return False
    else:
        return True
    

def get_toss_decision(m):
    toss_decision_name = 'NA'
    if not m.status == 'dormant':
        toss_decision_name = m.toss_decision_name
    return toss_decision_name

def get_toss_winner(m):
    toss_winner = 'NA'
    if not m.status == 'dormant':
        toss_winner = get_team_from_id(m,m.toss_winner_team_id)
    return toss_winner

def get_over_information(out):
    d = dict()
    for comm in out['comms']:
        if 'runs' in comm.keys():
            d[int(comm['over_number'])] = {'innings_score':int(comm['runs']),'innings_wickets':int(comm['wickets']),'current_innings':int(comm['innings_number'])}

    for key in d.copy():
        if key-1 in d.keys():
            d[key]['total_runs'] = d[key]['innings_score']-d[key-1]['innings_score']
            d[key]['player_dismised'] = d[key]['innings_wickets']-d[key-1]['innings_wickets']
            d[key]['overs'] = key
            d[key]['current_innings'] = d[key]['current_innings']
        elif key==1:
            d[key]['total_runs'] = d[key]['innings_score']
            d[key]['player_dismised'] = d[key]['innings_wickets']
            d[key]['overs'] = key
            d[key]['current_innings'] = d[key]['current_innings']
        else:
            d.pop(key)
    return d

def get_rrr_rrd(df,total_overs):
    rrrl = []
    rrdl = []
    for i in range(len(df)):
        if total_overs != df['overs'][i]:
            rrr = df['remaining_target'][i]/(total_overs-df['overs'][i])
            rrd = df['run_rate'][i] - rrr
        else:
            rrr = 99
            rrd = df['run_rate'][i] - rrr
        rrrl.append(rrr)
        rrdl.append(rrd)
    df['required_run_rate'] = rrrl
    df['run_rate_diff'] = rrdl
    return df

def get_team(team1,team2,batting_team,innings):
    if innings==1:
        if batting_team==team1:
            return team1,team2
        else:
            return team2,team1
    else:
        if batting_team==team1:
            return team2,team1
        else:
            return team1,team2
        

def main(match_id):
    m = Match(match_id)  
    data = data = m.get_json()
    col ={'runs':0,'wickets':0,'overs':'0','target':0}
    
    for i in data.get('innings'):
        if i.get('live_current') == 1 and i.get('live_current_name') == 'current innings':
            col = i
    
    comms_out = list(get_over_information(data).values())
    if len(comms_out):
        df = pd.DataFrame(comms_out)
    #     df['current_innings'] = col.get('innings_number')

        df['team1'],df['team2'] = get_team(m.team_1_abbreviation,m.team_2_abbreviation,get_team_from_id(m,str(col.get('batting_team_id'))),df['current_innings'].unique()[0])
        df['batting_team'] = get_team_from_id(m,str(col.get('batting_team_id')))
        df['toss_decision'] = get_toss_decision(m)
        df['toss_winner'] = get_toss_winner(m)
        df['score_target'] = col['target']
        df['run_rate'] = df['innings_score']/df['overs']
        if str(col['target']) == str(0):
            df['remaining_target'],df['score_target'],df['required_run_rate'],df['run_rate_diff'] = -1,-1,-1,-1
        else:
            df['remaining_target'] = df['score_target'] - df['innings_score']
            df = get_rrr_rrd(df,col['ball_limit']/6)


        if not os.path.isfile('data_extraction/data/{}_v2.csv'.format(match_id)):
            df.to_csv('data_extraction/data/{}_v2.csv'.format(match_id), mode='w', index = False)
        df.to_csv('data_extraction/data/{}_v2.csv'.format(match_id), mode='a', header=False, index = False)
        
        g = github.Github('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')
        repo = g.get_user().get_repo('Jarvis')

        with open('data_extraction/data/{}_v2.csv', mode ='r')as file:
          data = file.read()

#         print(data)

        # new_repo.create_file("data_extraction/current_matches.csv", "updating file", str(df), branch= 'main')

        contents = repo.get_contents("data_extraction/data/{}_v2.csv", ref="main")
        repo.update_file(contents.path, "more tests", data, contents.sha, branch="main")

        df1 = pd.read_csv('data_extraction/data/{}_v2.csv'.format(match_id))
        df1 = df1.drop_duplicates().sort_values(by=['current_innings','overs']).reset_index(drop=True)

        columns = ['inning', 'over', 'total_runs', 'player_dismissed', 'innings_wickets', 'innings_score', \
         'score_target', 'remaining_target', 'run_rate', 'required_run_rate', 'runrate_diff', 'is_batting_team', 'is_toss_winner','team1','team2']

        df1['inning'] = df1['current_innings']
        df1['over'] = df1['overs']
        df1['player_dismissed'] = df1['player_dismised']
        df1['runrate_diff'] = df1['run_rate_diff']
        df1['is_batting_team'] = [int(i) for i in df1['batting_team']==df1['team1']]
        df1['is_toss_winner'] = [int(i) for i in df1['toss_winner']==df1['team1']]
        df1 = df1[columns]


        df1.drop_duplicates().to_csv('data_extraction/data/{}_filtered.csv'.format(match_id),index=False)
        
        g = github.Github('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')
        repo = g.get_user().get_repo('Jarvis')

        with open('data_extraction/data/{}_filtered.csv', mode ='r')as file:
          data = file.read()

#         print(data)

        # new_repo.create_file("data_extraction/current_matches.csv", "updating file", str(df), branch= 'main')

        contents = repo.get_contents("data_extraction/data/{}_filtered.csv", ref="main")
        repo.update_file(contents.path, "more tests", data, contents.sha, branch="main")
    else:
        print('Match not yet started')  
    return

df_match = pd.read_csv('data_extraction/current_matches.csv')
for match in df_match['matches']:
    print(match)
    main(match)



