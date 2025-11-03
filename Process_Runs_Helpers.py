import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from statistics import mean
from matplotlib.ticker import FuncFormatter

def findFastRow(distance_df):
        if distance_df.empty:
            return None
        if 'Pace_min' not in distance_df.columns:
            return None
        fastest_idx = distance_df['Pace_min'].idxmin()
        fast_row = distance_df.loc[fastest_idx]
        return fast_row

def pace_formatter(x, pos):
    minutes = int(x)
    seconds = int(round((x - minutes) * 60))
    return f"{minutes}:{seconds:02d}"

def create_run_visual(run_0k_df, run_5k_df, run_10k_df, run_21k_df, run_42k_df, run_stat_df,user): 

    # 1 - Create Figure ---------------------------------------------------------
    fig = plt.figure(figsize=(11, 8.5))
    fig.suptitle(user + "’s Runs - " + " Run Pace by Distance", fontsize=16, fontweight="bold", y=0.95, ha='center')
    current_date = pd.Timestamp.today().normalize().strftime("%Y-%m-%d")
    fig.text(0.5, 0.915, "Updated: " + current_date, ha='center', fontsize=10)

    # 2 - Create Graph ---------------------------------------------------------
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.plot(run_0k_df['Date'], run_0k_df['Pace_min'], linestyle='--', color='blue', alpha=0.5, label='_nolegend_')
    ax1.plot(run_5k_df['Date'], run_5k_df['Pace_min'], linestyle='--', color='green', alpha=0.5, label='_nolegend_')
    ax1.plot(run_10k_df['Date'], run_10k_df['Pace_min'], linestyle='--', color='#BDB76B', alpha=0.5, label='_nolegend_')
    ax1.plot(run_21k_df['Date'], run_21k_df['Pace_min'], linestyle='--', color='orange', alpha=0.5, label='_nolegend_')
    ax1.plot(run_42k_df['Date'], run_42k_df['Pace_min'], linestyle='--', color='red', alpha=0.5, label='_nolegend_')


    ax1.plot(run_0k_df['Date'], run_0k_df['last3_pace'], color='blue', label='<5k Pace (Last 3 Avg)')
    ax1.plot(run_5k_df['Date'], run_5k_df['last3_pace'], color='green', label='5k Pace (Last 3 Avg)')
    ax1.plot(run_10k_df['Date'], run_10k_df['last3_pace'], color='#BDB76B', label='10k Pace (Last 3 Avg)')
    ax1.plot(run_21k_df['Date'], run_21k_df['last3_pace'], color='orange', label='21k Pace (Last 3 Avg)')
    ax1.plot(run_42k_df['Date'], run_42k_df['last3_pace'], color='red', label='42k Pace (Last 3 Avg)')


    ax1.yaxis.set_major_formatter(FuncFormatter(pace_formatter))
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Pace')
    ax1.set_title('Runs')
    ax1.legend(fontsize=6, loc='upper left')
    ax1.grid(True)


    # 3  - Create table --------------------------
    ax2 = fig.add_subplot(2, 1, 2)
    ax2.axis('off')  # Hide axes
    
    table = ax2.table(
        cellText=run_stat_df.values,
        colLabels=run_stat_df.columns,
        loc='upper center',
        cellLoc='center',
        bbox=[0.0, -0.05, 1.0, 1.0]
    )
    # table.scale(1, 2.1)
    table.scale(1.2, 1.4) 
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    for key, cell in table.get_celld().items():
        row, col = key
        if row == 0:
            cell.set_text_props(weight='bold')
    # ax2.set_title("Fastest Runs by Distance", fontweight="bold", fontsize=10, pad=10)
    ax2.text(0.5, 1, "Fastest Runs by Distance",
             ha='center', va='top', fontweight='bold', fontsize=10)

    # 4 - Save Figure ---------------------------------------------------------
    graphics_folder = f"{user}_Graphics"
    os.makedirs(graphics_folder, exist_ok=True)  # create folder if it doesn't exist
    file_path = os.path.join(graphics_folder, user + "_Runs.png")
    plt.savefig(file_path, dpi=100, bbox_inches="tight")
