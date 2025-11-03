import pandas as pd
import numpy as np

from Create_DF import create_df
from Process_Weights_Helpers import consolidate_strengths, create_total_visual, create_group_visuals, avg_first_last

def process_weights(user, is_runner=False, is_biker=False, start_date=None):
    print(user + "'s Weights Function Running")

    # 1 - Create DataFrames
    raw_df = create_df(user, "Raw")
    exercise_df = create_df(user, "Exercises")
    workout_df = create_df(user, "Workouts")
    run_df = create_df(user, "Runs") if is_runner else None
    bike_df = create_df(user, "Bikes") if is_biker else None

    # 2  - Process DataFrames
    raw_df = raw_df.drop(columns=['Strength', 'Comments'], errors='ignore')                             # Raw - Drop Unused Columns
    raw_df = raw_df.dropna(subset=["Date"])                                                             # Raw - Drop NaN rows
    raw_df['Date'] = pd.to_datetime(raw_df['Date'])                                                     # Raw - Convert Dates 
    workout_df['Date'] = pd.to_datetime(workout_df['Date'])                                             # Workout - Convert Dates
    if is_runner: run_df['Date'] = pd.to_datetime(run_df['Date'])                                       # Run - Convert Dates
    if is_biker: bike_df['Date'] = pd.to_datetime(bike_df['Date'])                                      # Bike - Convert Dates
    raw_df = raw_df.merge(exercise_df[['Exercise', 'BW', '1H']], on='Exercise', how='left')             # Raw - Merge BW, 1H Indicator
    raw_df = raw_df.merge(workout_df[['Date', 'Bodyweight']], on='Date', how='left')                    # Raw - Merge Bodyweights
    raw_df['Weight'] = raw_df['Weight']* (1 + raw_df['1H'])  + raw_df['BW']*raw_df['Bodyweight']        # Raw - Double 1H and add BW where applicable
    raw_df["Strength"] = raw_df["Weight"] * 100 / (48.8 + 53.8 * np.exp(-0.075 * raw_df["Reps"]))       # Raw - Calculate Strength

    # 3 - Consolidate Strengths
    consolidated_df = consolidate_strengths(raw_df)                                                     # Consolidated - Consolidate Strengths
    consolidated_df = consolidated_df.merge(exercise_df[['Exercise', 'Colour', 'LineType']], on='Exercise', how='left') # Consolidated - Merge Groups
   
        # Get 3x8 Weights for Exercises
    recent_strengths = consolidated_df.loc[consolidated_df.groupby('Exercise')['Date'].idxmax()]        # Recent Strengths - Get Recent Strengths
    exercise_df = exercise_df.merge(recent_strengths[['Exercise', 'Max3']], on='Exercise', how='left')  # Exercise Merge Recent Strengths
    exercise_df.rename(columns={'Max3': 'RecentMax3'}, inplace=True)                                    # Exercise - Rename Columns
    exercise_df['3x8 Weight'] = round(exercise_df['RecentMax3'] * 0.783251600392)                       # Exercise - Calculate 3x8 Weights
        
        # Get 1RMs for Exercises
    max_strengths = raw_df.loc[raw_df.groupby('Exercise')['Strength'].idxmax()]                         # Max Strengths - Get Max Strengths
    exercise_df = exercise_df.merge(max_strengths[['Date','Exercise', 'Strength', 'Reps', 'Weight']], on='Exercise', how='left') # Exercise Merge Max Strengths
    exercise_df.rename(columns={'Strength': '1RM Strength','Reps': '1RM Reps','Weight': '1RM Weight','Date': '1RM Date'}, inplace=True) # Exercise - Rename Columns       

        # Get percentage increase
    avg_df = avg_first_last(consolidated_df)
    exercise_df = exercise_df.merge(avg_df, on='Exercise', how='left')

        # Treat as Integers
    exercise_df['3x8 Weight'] = exercise_df['3x8 Weight'].fillna(0).astype(int)
    exercise_df['1RM Strength'] = exercise_df['1RM Strength'].fillna(0).astype(int)
    exercise_df['1RM Reps'] = exercise_df['1RM Reps'].fillna(0).astype(int)
    exercise_df['1RM Weight'] = exercise_df['1RM Weight'].fillna(0).astype(int)
    exercise_df['1RM Date'] = pd.to_datetime(exercise_df['1RM Date']).dt.date

    # 4 - Create Total Visuals
    create_total_visual(raw_df, workout_df, user, run_df=run_df, bike_df=bike_df, start_date=start_date)

    # 5 - Create Group Visuals
    create_group_visuals(consolidated_df, exercise_df, user)

