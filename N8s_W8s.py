# 0 - Import Libraries and Data

import pandas as pd
from Process_Weights import process_weights
from Process_Runs import process_runs
from Process_Bikes import process_bikes

# 1- Run Function

user = "N8"

def run_N8s_W8s():
    user_df = pd.read_csv("Users.csv")
    for idx, row in user_df.iterrows():
        if row["User"] == user: 
            if (row["Weights"] == 1): process_weights(user, row["Runs"] == 1, row["Bikes"] == 1, row["Start Date"])
            if (row["Runs"] == 1): process_runs(user, row["Start Date"])
            if (row["Bikes"] == 1): process_bikes(user, row["Start Date"])
            break
        else:
            if (idx == len(user_df)-1): print("User not found")

# 2 - Execute Function
run_N8s_W8s()