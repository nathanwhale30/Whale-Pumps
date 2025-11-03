import pandas as pd
import glob
import os

def create_df(user, df_name):
    try:
        folder = f"{user}_Files"
        pattern = os.path.join(folder, f"{user}'s W8s - " + df_name + "*")
        file = glob.glob(pattern)[0]
        df = pd.read_csv(file)
        return df
    except Exception as e:
        print(f"Error loading raw data for {user}: {e}")
        return pd.DataFrame()