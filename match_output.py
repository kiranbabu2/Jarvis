from espncricinfo.summary import Summary
from espncricinfo.match import Match
import pandas as pd
import os
import time
import csv
import json
import io
from github_helper import *

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
            d[int(comm['over_number'])] = {'innings_score':int(comm['runs']),'innings_wickets':int(comm['wickets']),'inning':int(comm['innings_number'])}

    for key in d.copy():
        if key-1 in d.keys():
            d[key]['total_runs'] = d[key]['innings_score']-d[key-1]['innings_score']
            d[key]['player_dismissed'] = d[key]['innings_wickets']-d[key-1]['innings_wickets']
            d[key]['over'] = key
            d[key]['inning'] = d[key]['inning']
        elif key==1:
            d[key]['total_runs'] = d[key]['innings_score']
            d[key]['player_dismissed'] = d[key]['innings_wickets']
            d[key]['over'] = key
            d[key]['inning'] = d[key]['inning']
        else:
            d.pop(key)
    return d

def get_rrr_rrd(df,total_overs):
    rrrl = []
    rrdl = []
    for i in range(len(df)):
        if total_overs != df['over'][i]:
            rrr = df['remaining_target'][i]/(total_overs-df['over'][i])
            rrd = df['run_rate'][i] - rrr
        else:
            rrr = 99
            rrd = df['run_rate'][i] - rrr
        rrrl.append(rrr)
        rrdl.append(rrd)
    df['required_run_rate'] = rrrl
    df['runrate_diff'] = rrdl
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
        df[df['inning']==df['inning'].max()].reset_index(drop=True)
        df['team1'],df['team2'] = get_team(m.team_1_abbreviation,m.team_2_abbreviation,get_team_from_id(m,str(col.get('batting_team_id')))\
                                            ,df['inning'].unique()[0])
        df['batting_team'] = get_team_from_id(m,str(col.get('batting_team_id')))
        df['toss_decision'] = get_toss_decision(m)
        df['toss_winner'] = get_toss_winner(m)
        df['score_target'] = col['target']
        df['run_rate'] = df['innings_score']/df['over']
        if str(col['target']) == str(0):
            df['remaining_target'],df['score_target'],df['required_run_rate'],df['runrate_diff'] = -1,-1,-1,-1
        else:
            df['remaining_target'] = df['score_target'] - df['innings_score']
            df = get_rrr_rrd(df,col['ball_limit']/6)
        df['is_batting_team'] = [int(i) for i in df['batting_team']==df['team1']]
        df['is_toss_winner'] = [int(i) for i in df['toss_winner']==df['team1']]

        columns = ['inning', 'over', 'total_runs', 'player_dismissed', 'innings_wickets', 'innings_score', \
            'score_target', 'remaining_target', 'run_rate', 'required_run_rate', 'runrate_diff', 'is_batting_team', 'is_toss_winner','team1','team2']

        df = df[columns]
        try:
            contents = repo.get_contents("./data/{}.csv".format(match_id), ref="main")
            existing_df = pd.read_csv(io.StringIO(contents.decoded_content.decode('utf-8')))
            df = existing_df.append(df, ignore_index=True)
            df = df.drop_duplicates(subset=['inning', 'over'], keep='last').sort_values(by=['inning','over']).reset_index(drop=True)
            df.to_csv('./data/{}.csv'.format(match_id), index = False) 
            with open('./data/{}.csv'.format(match_id), mode ='r') as file:
                data = file.read()
            repo.update_file(contents.path, "more tests", data, contents.sha, branch="main")
        except:
            df = df.drop_duplicates(subset=['inning', 'over'], keep='last').sort_values(by=['inning','over']).reset_index(drop=True)
            df.to_csv('./data/{}.csv'.format(match_id), index = False)
            with open('./data/{}.csv'.format(match_id), mode ='r') as file:
                data = file.read()
            repo.create_file("./data/{}.csv".format(match_id), "init commit", data)
    else:
        print('Match not yet started')  
    return


cm_contents = repo.get_contents("./current_matches.csv", ref="main")
df_match = pd.read_csv(io.StringIO(cm_contents.decoded_content.decode('utf-8')))
for match in df_match['matches']:
    print(match)
    main(match)



