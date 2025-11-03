import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt
import numpy as np
import datetime
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import ScalarFormatter
import glob
from Create_DF import create_df

from Process_Runs_Helpers import findFastRow, pace_formatter, create_run_visual

def process_runs(user, start_date):
    print(user + "'s Runs Function Running")

    # 1 - Create DataFrame
    run_df = create_df(user, "Runs")

    # 2 - Process DataFrame
    run_df['Date'] = pd.to_datetime(run_df['Date'])
    
    start_date = pd.to_datetime(start_date)
    run_df = run_df[run_df['Date'] >= start_date].reset_index(drop=True)


    run_df = run_df.drop(columns=['Comments'])
    run_df['Contingency'] = run_df['Contingency'].fillna('NA')

    run_df['Time_min'] = pd.to_timedelta(run_df['Time']).dt.total_seconds()/3600
    run_df['Pace_min'] = run_df['Time_min'] / run_df['Distance']


    # 3 - Create Run Distance dfs ------------------------
    run_0k_df = run_df[(run_df['Distance'] < 5)]
    run_5k_df = run_df[(run_df['Distance'] >= 5) & (run_df['Distance'] < 10)]
    run_10k_df = run_df[(run_df['Distance'] >= 10) & (run_df['Distance'] < 21)]
    run_21k_df = run_df[(run_df['Distance'] >= 21) & (run_df['Distance'] < 42)]
    run_42k_df = run_df[(run_df['Distance'] >= 42)]

    # Remove Contingencies
    distance_dfs = [run_0k_df, run_5k_df, run_10k_df, run_21k_df, run_42k_df]
    distance_labels = ['<5k', '5k', '10k', '21k', '42k']
    distance_dfs = [df[df['Contingency'] == 'NA'].copy() for df in distance_dfs]  # Use .copy() to avoid SettingWithCopyWarning

    # Add rolling average of pace
    for df in distance_dfs:
        df['last3_pace'] = df['Pace_min'].rolling(window=3).mean()

    # Updated dataframes
    run_0k_df, run_5k_df, run_10k_df, run_21k_df, run_42k_df = distance_dfs

    # 2.2 - Run 1RM DF ----------------------------------

    group_df = []

    for label, distance_df in zip(distance_labels, distance_dfs):
        fastRun = findFastRow(distance_df)
        row = {}
        row['Type'] = label
        if fastRun is not None:
            row['Date'] = fastRun['Date']
            row['Pace'] = fastRun['Pace']
            row['Distance'] = fastRun['Distance']
            row['Time'] = fastRun['Time']
        else:
            row['Date'] = pd.NaT
            row['Pace'] = np.nan
            row['Distance'] = np.nan
            row['Time'] = np.nan
        group_df.append(row)

    run_stat_df = pd.DataFrame(group_df)

    run_stat_df['Pace'] = run_stat_df['Pace'].apply(lambda x: str(x)[:4] if not pd.isna(x) else "nan")
    run_stat_df['Date'] = run_stat_df['Date'].apply(lambda x: str(x)[0:10] if not pd.isna(x) else "Get on it!")

    create_run_visual(run_0k_df, run_5k_df, run_10k_df, run_21k_df, run_42k_df, run_stat_df, user)