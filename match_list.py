from espncricinfo.summary import Summary
from espncricinfo.match import Match
import pandas as pd
import os
import time
import csv
import json

# match_id = '1339606'

# for match in Summary().match_ids:
#     print(match, Match(match).description)

def get_batting_team_from_id(m,bat_id):
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
    
def fetch_over_details(over_list,over):
    wicket = 0
    runs = 0
    try:
        for o in over_list:
            if str(o[0].get('over_number'))==over:
                for b in o:
                    if b.get('ball')=='W':
                        wicket = wicket + 1
                    elif b.get('ball')=='&bull;':
                        continue
                    elif represents_int(b.get('ball')):
                        runs = runs + b.get('ball')
    except:
        pass
    return runs,wicket

def get_score_until_previous_over(total_runs,total_wickets,total_overs,over_list):
    current_over = int(total_overs.split('.')[0])+1
    if int(total_overs.split('.')[1])!=0:
        if int(total_overs.split('.')[0])==0:
            return 0,0
        elif int(total_overs.split('.')[0])==1:
            return fetch_over_details(over_list,'1')
        else:
            current_over_runs,current_over_wickets = fetch_over_details(over_list,str(current_over))
            return total_runs-current_over_runs, total_wickets-current_over_wickets
    else:
        return total_runs,total_wickets


def get_completed_over(over):
    try:
        return over.split('.')[0]
    except:
        return '0'
    
def get_match_winner(m):
    match_winner = 'NA'
    if not m.status == 'dormant':
        match_winner = m.match_winner
    return match_winner

def get_toss_decision(m):
    toss_decision_name = 'NA'
    if not m.status == 'dormant':
        toss_decision_name = m.toss_decision_name
    return toss_decision_name

def get_run_rate(completed_over,innings_runs):
    if completed_over!='0':
        run_rate= innings_runs/int(completed_over)
    else:
        run_rate = 0
    return run_rate



a = 1
match_id = '1365095'

while a:
    m = Match(match_id)    
    # res = pd.DataFrame(columns=['inning', 'over', 'team1', 'team2', 'batting_team', 'winner', 'total_runs', 'player_dismised', 'innings_wickets', 'innings_score', 'score_target', 'remaining_target', 'run_rate', 'required_run_rate', 'runrate_diff'])

    col ={'runs':0,'wickets':0,'overs':'0','target':0}
    with open('data_analysis/data_{}.json'.format(str(a)),'w') as f:
        data = m.get_json()
        json.dump(data,f)
    for i in data.get('innings'):
        if i.get('live_current') == 1 and i.get('live_current_name') == 'current innings':
            col = i
    

    a = a+1

    current_innings = col.get('innings_number')
    completed_over = get_completed_over(col.get('overs'))
    team1 = m.team_1_abbreviation
    team2 = m.team_2_abbreviation
    batting_team = get_batting_team_from_id(m,str(col.get('batting_team_id')))
    match_winner = get_match_winner(m)
    over_list = data.get('live').get('recent_overs')
    over_runs,over_wickets = fetch_over_details(over_list,completed_over)
    innings_runs,innings_wickets = get_score_until_previous_over(int(col['runs']),int(col['wickets']),col['overs'],over_list) 

    toss = get_toss_decision(m)
    target = col['target']

    run_rate = get_run_rate(completed_over,innings_runs)
    if str(target) == str(0):
        remaining_target,target,required_run_rate,run_rate_diff = -1,-1,-1,-1
    else:
        remaining_target = target - innings_runs
        if m.scheduled_overs!=int(completed_over):
            required_run_rate = remaining_target/(int(m.scheduled_overs) - int(completed_over))
            run_rate_diff = required_run_rate - run_rate
        else:
            # a = 0
            required_run_rate = 0
            run_rate_diff = 0
        

    if not os.path.isfile('{}.csv'.format(match_id)):
        df_temp = pd.DataFrame(columns = ['inning', 'over', 'team1', 'team2', 'batting_team', 'winner', 'total_runs', 'player_dismised', 'innings_wickets', 'innings_score', 'score_target', 'remaining_target', 'run_rate', 'required_run_rate', 'runrate_diff','toss'] )
        df_temp.to_csv('{}.csv'.format(match_id),index = False)


    with open('{}.csv'.format(match_id), 'a',newline='') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
        # writing the fields 
        print([current_innings, completed_over, team1, team2, batting_team, match_winner, over_runs, over_wickets, \
                            innings_wickets, innings_runs, target, remaining_target, run_rate, required_run_rate, \
                                run_rate_diff,toss])
        csvwriter.writerow([current_innings, completed_over, team1, team2, batting_team, match_winner, over_runs, over_wickets, \
                            innings_wickets, innings_runs, target, remaining_target, run_rate, required_run_rate, \
                                run_rate_diff,toss]) 
    time.sleep(60)



