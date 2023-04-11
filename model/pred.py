import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt


#write a method to get match_id from the user
def get_match_id():
    df_current = pd.read_csv('../current_matches.csv')
    match_id = df_current['   matches'][0].split(' ')[-1]
    return match_id

# write a method to read the data with match_id as parameter
def read_data(match_id):
    df = pd.read_csv('../data_extraction/data/{}_filtered.csv'.format(match_id))
    #append match_id to the dataframe
    df['match_id'] = match_id
    return df

# read the model
def read_model():
    model = pd.read_pickle('model.pkl')
    return model

#get the predictions
def get_preds(df,model):
    x_cols = ['inning','over','total_runs','player_dismissed','innings_wickets','innings_score','score_target','remaining_target','run_rate',
 'required_run_rate','runrate_diff','is_batting_team']
    val_df = df[x_cols[:]]
    # predict the values
    val_X = np.array(val_df)#[:-1,:]
    xgtest = xgb.DMatrix(val_X)
    preds = model.predict(xgtest)
    return preds

#get the result dataframe
def get_result_df(df,preds):
    out_df = pd.DataFrame({'Team1':df.team1.values}) #mumbai indians for colab data
    out_df['match_id'] = df.match_id.values
    out_df['is_batting_team'] = df.is_batting_team.values
    out_df['Team2'] = df.team2.values
    #get length of innings 1 in df
    innings1_length = len(df[df.inning==1])
    innings2_length = len(df[df.inning==2])
    out_df['innings_over'] = np.array(df.apply(lambda row: str(row['inning']) + "_" + str(row['over']), axis=1))
    out_df['innings_score'] = df.innings_score.values
    out_df['innings_wickets'] = df.innings_wickets.values
    out_df['score_target'] = df.score_target.values
    out_df['total_runs'] = df.total_runs.values
    out_df['player_dismissed'] = df.player_dismissed.values
    out_df['predictions'] = list(preds)
    #out_df['run_rate_imp'] = val_df.run_rate_imp.values
    out_df['wickets_in_over'] = df.player_dismissed.values
    out_df['required_run_rate'] = df.required_run_rate.values
    out_df['predicted_team1'] = preds
    out_df['predicted_team2'] = 1 - preds
    return out_df,innings1_length,innings2_length

# get plots from the final dataframe
def get_plot1(out_df,match_id):
    plt.figure(figsize=[8,6])

    team_1 = out_df.Team1.values[0]
    team_2 = out_df.Team2.values[0]

    # Create data
    over= out_df.innings_over.values
    Team1=100*out_df.predicted_team1.values
    Team2= 100*out_df.predicted_team2.values

    #plot a horizontal line at 50% probability with thickness 2
    plt.plot([0, len(over)-1], [50, 50], 'r--', linewidth=4,markersize=12)

    plt.xticks(rotation=90)
    plt.ylabel('Winning Probability')
    plt.xlabel('Innings_score')

    # Basic stacked area chart.
    plt.stackplot(over,Team1, Team2, labels=['{}'.format(team_2),'{}'.format(team_1)],colors=['blue','#FFCCCB'])
    plt.legend(loc='upper left')
    #plt.show()

    #save the plot
    plt.savefig('../model/plot_1.png')
    plt.close()

def get_plot2(out_df,match_id,preds,team_1,team_2):
    plt.plot(100*preds)
    #make the plot red if value is less than 0.5
    plt.plot([0, len(preds)], [50, 50], 'r--')
    #make preds lineplot red if value is less than 0.5
    plt.fill_between(range(len(preds)), 100*preds, 50, where=100*preds<50, facecolor='red', alpha=0.5)

    #make the plot green if value is greater than 0.5
    plt.plot([0, len(preds)], [50, 50], 'g--')
    #make preds lineplot green if value is greater than 0.5
    plt.fill_between(range(len(preds)), 100*preds, 50, where=100*preds>50, facecolor='green', alpha=0.5)

    #make the plot more beautiful
    plt.title('Predictions for {} - Match ID {}'.format(team_2, match_id))
    plt.xlabel('Inning_Over')
    plt.ylabel('Probability of winning (%)')

    #make the background more beautiful

    plt.savefig('../model/plot_2.png')
    plt.close()

def get_plot3(out_df,match_id,preds,team_1,team_2,innings1_length,innings2_length):
    fig, ax1 = plt.subplots()
    # set the figure size
    fig.set_size_inches(10, 10)
    ax1.set_xlabel('innings_over')
    ax1.set_ylabel('run_rate')
    ax1.bar(out_df['innings_over'], out_df['innings_score'], color=['yellow']*innings1_length + ['#90ee90']*innings2_length)
    ax1.legend(loc=2)
    # make the x axis labels vertical
    plt.xticks(rotation=90)
    ax2 = ax1.twinx()
    ax2.set_ylabel('predictions')
    wicket_indices = [i for i, x in enumerate(out_df['player_dismissed']) if x >= 1]
    ax2.plot(out_df['innings_over'], np.array(out_df['predicted_team1'])*100, color='blue',marker='o',markevery=wicket_indices,markerfacecolor='red' )


    #change the size of ma

    #set axis1 ylabel first half as team1 and second half as team2
    ax1.set_yticks(np.arange(0, 10, 1))

    label = '{}                                  {}'.format(team_2,team_1)

    ax1.set_ylabel(label)

    #make ax2 y ticks from 100 to 50 in 1st half and 50 to 100 in 2nd half


    # remove yticks for ax1
    ax1.set_yticks([])




    #make a horizonal line for pred at 0.5
    ax2.plot(out_df['innings_over'],np.array([50]*len(out_df['predicted_team1'])),color='red', marker='o')
    ax2.set_yticks(np.arange(0, 105, 5))
    ax2.legend(loc=1)

    plt.title('Predictions for {} vs {} with run rate in each innings'.format(team_1,team_2))
    #plt.show()
    plt.savefig('../model/plot_3.png')
    plt.close()


def main():
    match_id = get_match_id()
    df = read_data(match_id)
    model = read_model()
    preds = get_preds(df,model)
    out_df,innings1_length,innings2_length = get_result_df(df,preds)
    get_plot1(out_df,match_id)
    get_plot2(out_df,match_id,preds,out_df.Team1.values[0],out_df.Team2.values[0])
    get_plot3(out_df,match_id,preds,out_df.Team1.values[0],out_df.Team2.values[0],innings1_length,innings2_length)
    out_df.to_csv('../model/{}_results.csv'.format(match_id))



if __name__=='__main__':
    main()






