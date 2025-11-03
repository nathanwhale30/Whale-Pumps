import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from statistics import mean

def consolidate_strengths(df):
    output_data = []
    curr_date = None
    curr_exercise = None
    curr_strength_arr = []

    for i, row in df.iterrows():
        if curr_date != row['Date'] or curr_exercise != row['Exercise']:
            # Upload exercise values
            if curr_strength_arr:
                if len(curr_strength_arr) > 2:
                    avg_all = round(mean(curr_strength_arr))
                    avg_max3 = round(mean(sorted(curr_strength_arr, reverse=True)[:3]))
                else:
                    avg_all = np.nan
                    avg_max3 = np.nan
                max1 = max(curr_strength_arr)
                if curr_date is not None and curr_exercise is not None:
                    output_data.append({
                        'Date': curr_date,
                        'Exercise': curr_exercise,
                        'Max1': max1,
                        'Max3': avg_max3,
                        'Max All': avg_all
                    })
            # Reset for new exercise/date
            curr_date = row['Date']
            curr_exercise = row['Exercise']
            curr_strength_arr = []

        # Upload a new value if Set != 0
        if row['Set'] != 0 and not pd.isna(row['Strength']):
            curr_strength_arr.append(row['Strength'])

    # Handle the last group after the loop
    if curr_strength_arr:
        if len(curr_strength_arr) > 2:
            avg_all = round(mean(curr_strength_arr))
            avg_max3 = round(mean(sorted(curr_strength_arr, reverse=True)[:3]))
        else:
            avg_all = np.nan
            avg_max3 = np.nan
        max1 = max(curr_strength_arr)
        output_data.append({
            'Date': curr_date,
            'Exercise': curr_exercise,
            'Max1': max1,
            'Max3': avg_max3,
            'Max All': avg_all
        })
    
    # Convert to DataFrame
    output_df = pd.DataFrame(output_data)

    # Remove rows without Max3 (i.e. NaN)
    output_df = output_df.dropna(subset=['Max3']).reset_index(drop=True)

    return output_df


def create_total_visual(raw_df, workout_df, user, run_df=None, bike_df=None, start_date=None):

    # 1.1 Totals (Since 2025-01-01) ---------------------------------------------
    raw2_df = raw_df[raw_df['Date'] >= start_date]
    workout2_df = workout_df[workout_df['Date'] >= start_date]
    if run_df is not None: run2_df = run_df[run_df['Date'] >= start_date]
    if bike_df is not None: bike2_df = bike_df[bike_df['Date'] >= start_date]         

    total_time2 = workout2_df["Mins"].sum()
    total_days2 = total_time2 // 1440
    total_hours2 = total_time2 % 1440 // 60
    total_minutes2 = total_time2 % 60

    totalWorkouts2 = raw2_df["Date"].nunique()
    totalSets2 = raw2_df.shape[0]
    totalWeight2 = round((raw2_df["Weight"] * raw2_df["Reps"]).sum())
    totalWorkoutCals2 = round((workout2_df["Cals"]).sum())

    if run_df is not None: 
        totalRunDistance2 = round((run2_df["Distance"]).sum(), 2)
        totalRunCals2 = round((run2_df["Cals"]).sum())

    if bike_df is not None:
        totalBikeDistance2 = round((bike2_df["Distance"]).sum(), 2)
        totalBikeCals2 = round((bike2_df["Cals"]).sum())

    # 1.2 Totals (30-Days) ---------------------------------------------------------
    today = pd.Timestamp.today().normalize()

    raw3_df = raw_df[raw_df['Date'] >= (today - pd.Timedelta(days=30))]
    workout3_df = workout_df[workout_df['Date'] >= (today - pd.Timedelta(days=30))]
    if run_df is not None: run3_df = run_df[run_df['Date'] >= (today - pd.Timedelta(days=30))]
    if bike_df is not None: bike3_df = bike_df[bike_df['Date'] >= (today - pd.Timedelta(days=30))]

    total_time3 = workout3_df["Mins"].sum()
    total_days3 = total_time3 // 1440
    total_hours3 = total_time3 % 1440 // 60
    total_minutes3 = total_time3 % 60

    totalWorkouts3 = raw3_df["Date"].nunique()
    totalSets3 = raw3_df.shape[0]
    totalWeight3 = round((raw3_df["Weight"] * raw3_df["Reps"]).sum())
    totalWorkoutCals3 = round((workout3_df["Cals"]).sum())

    if run_df is not None: 
        totalRunDistance3 = round((run3_df["Distance"]).sum(), 2)
        totalRunCals3 = round((run3_df["Cals"]).sum())

    if bike_df is not None:
        totalBikeDistance3 = round((bike3_df["Distance"]).sum(), 2)
        totalBikeCals3 = round((bike3_df["Cals"]).sum())

    # 2.1 Create Figure ---------------------------------------------------------
    fig = plt.figure(figsize=(11, 20))

    # 2.2 Print Info ---------------------------------------------------------
    fig.suptitle(user + "’s W8s - Totals", fontsize=16, fontweight="bold", y=0.95, ha='center')
    current_date = today.strftime("%Y-%m-%d")
    fig.text(0.5, 0.93, "Updated: " + current_date, ha='center', fontsize=10)

    fig.text(0.1, 0.91, user + "'s Totals - All Time", fontsize=12, fontweight="bold")
    fig.text(0.1, 0.905, f"Since documentation started on {start_date}", fontsize=7.5)
    fig.text(0.1, 0.9, f"Total Workout Time: {total_days2} days, {total_hours2} hours, {total_minutes2} mins \nTotal Workouts: {totalWorkouts2} \nTotal Sets: {totalSets2} \nTotal Weight: {totalWeight2} lbs\nTotal Workout Moving Cals: {totalWorkoutCals2}\n", fontsize=10, va="top")
    if run_df is not None: fig.text(0.1, 0.85, f"Total Run Distance: {totalRunDistance2} kms \nTotal Run Cals: {totalRunCals2}\n", fontsize=10, va="top")
    if bike_df is not None: fig.text(0.1, 0.825, f"Total Bike Distance: {totalBikeDistance2} kms \nTotal Bike Cals: {totalBikeCals2}\n", fontsize=10, va="top")

    fig.text(0.55, 0.91, user + "'s Totals - Last 30 Days", fontsize=12, fontweight="bold")
    fig.text(0.55, 0.9, f"Total Workout Time: {total_days3} days, {total_hours3} hours, {total_minutes3} mins \nTotal Workouts: {totalWorkouts3} \nTotal Sets: {totalSets3} \nTotal Weight: {totalWeight3} lbs\nTotal Workout Moving Cals: {totalWorkoutCals3}\n", fontsize=10, va="top")
    if run_df is not None: fig.text(0.55, 0.85, f"Total Run Distance: {totalRunDistance3} kms \nTotal Run Cals: {totalRunCals3}\n", fontsize=10, va="top")
    if bike_df is not None: fig.text(0.55, 0.825, f"Total Bike Distance: {totalBikeDistance3} kms \nTotal Bike Cals: {totalBikeCals3}\n", fontsize=10, va="top")

    # 2.3 BW by Month ---------------------------------------------------------
    ax1 = fig.add_subplot(7, 1, 2)
    monthly_weights = workout2_df.groupby(workout2_df['Date'].dt.to_period('M'))['Bodyweight'].mean().reset_index()
    monthly_weights['Date'] = monthly_weights['Date'].dt.to_timestamp()
    ax1.plot(monthly_weights['Date'], monthly_weights['Bodyweight'], marker='o', color='purple')
    ax1.set_title("Average Bodyweight by Month")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Bodyweight (lbs)")
    ax1.grid(True)
    ax1.set_xlim(pd.Timestamp(start_date), today)

    # 2.4 WO Cals by Month ---------------------------------------------------------
    ax2 = fig.add_subplot(7, 1, 3)
    monthly_wo_cals = workout2_df.groupby(workout2_df['Date'].dt.to_period('M'))['Cals'].sum().reset_index()
    monthly_wo_cals['Date'] = monthly_wo_cals['Date'].dt.to_timestamp()
    ax2.plot(monthly_wo_cals['Date'], monthly_wo_cals['Cals'], marker='o', color='red')
    ax2.set_title("Total Workout Cals by Month")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Workout Cals")
    ax2.grid(True)
    ax2.set_xlim(pd.Timestamp(start_date), today)

    # 2.5 Total WO by Month ---------------------------------------------------------
    ax3 = fig.add_subplot(7, 1, 4)
    monthly_num_wo = workout2_df.groupby(workout2_df['Date'].dt.to_period('M'))['Mins'].count().reset_index()
    monthly_num_wo['Date'] = monthly_num_wo['Date'].dt.to_timestamp()
    ax3.plot(monthly_num_wo['Date'], monthly_num_wo['Mins'], marker='o', color='blue')
    ax3.set_title("Total Workouts by Month")
    ax3.set_xlabel("Month")
    ax3.set_ylabel("Number of Workouts")
    ax3.grid(True)
    ax3.set_xlim(pd.Timestamp(start_date), today)

    # 2.6 Bench/Squat 1RM by Month ---------------------------------------------------------
    ax4 = fig.add_subplot(7, 1, 5)

    monthly_bench_1rm = raw2_df.where(raw2_df['Exercise'] == 'Bench (BB, Flat)').groupby(raw2_df['Date'].dt.to_period('M'))['Strength'].max().reset_index()
    monthly_bench_1rm['Date'] = monthly_bench_1rm['Date'].dt.to_timestamp()
    ax4.plot(monthly_bench_1rm['Date'], monthly_bench_1rm['Strength'], marker='o', color='green', label='Bench (BB, Flat)')

    monthly_squat_1rm = raw2_df.where(raw2_df['Exercise'] == 'Squats (BB)').groupby(raw2_df['Date'].dt.to_period('M'))['Strength'].max().reset_index()
    monthly_squat_1rm['Date'] = monthly_squat_1rm['Date'].dt.to_timestamp()
    ax4.plot(monthly_squat_1rm['Date'], monthly_squat_1rm['Strength'], marker='o', color='black', label='Squats (BB)')

    ax4.set_title("Bench/Squat 1RM Strength by Month")
    ax4.set_xlabel("Month")
    ax4.set_ylabel("1RM Strength (lbs)")
    ax4.grid(True)
    ax4.legend(loc='upper left', fontsize=9, frameon=True)
    ax4.set_xlim(pd.Timestamp(start_date), today)

    # 2.4 Run Km by Month ---------------------------------------------------------
    if run_df is not None:
        ax5 = fig.add_subplot(7, 1, 6)
        monthly_run_kms = run_df.groupby(run_df['Date'].dt.to_period('M'))['Distance'].sum().reset_index()
        monthly_run_kms['Date'] = monthly_run_kms['Date'].dt.to_timestamp()
        ax5.plot(monthly_run_kms['Date'], monthly_run_kms['Distance'], marker='o', color='orange')
        ax5.set_title("Total Run Distance by Month")
        ax5.set_xlabel("Month")
        ax5.set_ylabel("Distance (kms)")
        ax5.grid(True)
        ax5.set_xlim(pd.Timestamp(start_date), today)

    # 2.5 Bike Km by Month ---------------------------------------------------------
    if bike_df is not None:
        ax6 = fig.add_subplot(7, 1, 7)
        monthly_bike_kms = bike_df.groupby(bike_df['Date'].dt.to_period('M'))['Distance'].sum().reset_index()
        monthly_bike_kms['Date'] = monthly_bike_kms['Date'].dt.to_timestamp()
        ax6.plot(monthly_bike_kms['Date'], monthly_bike_kms['Distance'], marker='o', color='brown')
        ax6.set_title("Total Bike Distance by Month")
        ax6.set_xlabel("Month")
        ax6.set_ylabel("Distance (kms)")
        ax6.grid(True)
        ax6.set_xlim(pd.Timestamp(start_date), today)

    # 3 - Save Figure ---------------------------------------------------------
    plt.subplots_adjust(hspace=0.4)

    graphics_folder = f"{user}_Graphics"
    os.makedirs(graphics_folder, exist_ok=True)  # create folder if it doesn't exist
    file_path = os.path.join(graphics_folder, user + "_Weight_Totals.png")
    plt.savefig(file_path, dpi=100, bbox_inches="tight")

# Helper for the below function
def create_group_visual(exercise_df, group_df, group_exercises, group, user):
    # 1 Create Figure ---------------------------------------------------------
    fig = plt.figure(figsize=(11, 8.5))
    fig.suptitle(user + "’s W8s - " + group + " Max3 Strength Over Time", fontsize=16, fontweight="bold", y=0.95, ha='center')
    current_date = pd.Timestamp.today().normalize().strftime("%Y-%m-%d")
    fig.text(0.5, 0.905, "Updated: " + current_date, ha='center', fontsize=10)

    # 2 Create Graph ---------------------------------------------------------
    ax1 = fig.add_subplot(2, 1, 1)
    for exercise in group_exercises:
        ex_df = group_df[group_df['Exercise'] == exercise]
        if ex_df.empty:
            # print(f"Skipping {exercise} (no data in consolidated_df)")
            continue

        # Get color and linetype for this exercise
        colour = ex_df['Colour'].iloc[0] if 'Colour' in ex_df else 'black'
        linetype = ex_df['LineType'].iloc[0] if 'LineType' in ex_df else 'solid'

        # Plot line using those style attributes
        ax1.plot(ex_df['Date'], ex_df['Max3'],
                 label=exercise,
                 color=colour,
                 linestyle=linetype)
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Strength")
    ax1.legend(bbox_to_anchor=(0, 1), loc='upper left', fontsize=8)

    # 2 Create Table ---------------------------------------------------------
    ax2 = fig.add_subplot(2, 1, 2)
    ax2.axis('off')  # Hide axes
    table_data = exercise_df[exercise_df['Exercise'].isin(group_df['Exercise'])][['Exercise', '3x8 Weight', '1RM Date', '1RM Strength', '1RM Weight', '1RM Reps', 'Last3 Avg Strength', 'Percent Change (6m)', 'Percent Change (All Time)']]

    table = ax2.table(cellText=table_data.values, colLabels=table_data.columns, cellLoc='center', loc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(6)   # 🔹 Increase or decrease Font size
    table.scale(1.2, 1.4) 

    # 3 - Save Figure ---------------------------------------------------------
    graphics_folder = f"{user}_Graphics"
    os.makedirs(graphics_folder, exist_ok=True)  # create folder if it doesn't exist
    file_path = os.path.join(graphics_folder, user + "_Weight_" + group + ".png")
    plt.savefig(file_path, dpi=100, bbox_inches="tight")


def create_group_visuals(consolidated_df, exercise_df, user):
    groups = exercise_df["Area"].unique()
    for group in groups:
        group_exercises = exercise_df[exercise_df["Area"] == group]["Exercise"].tolist()
        group_df = consolidated_df[consolidated_df['Exercise'].isin(group_exercises)]
        # COULD TAKE THE ROLLING AVERAGE HERE IF DESIRED
        if not group_df.empty:
            create_group_visual(exercise_df, group_df, group_exercises,  group, user)

# Return avg of first n and last n Max3 per exercise.
def avg_first_last(df, n=3):
    results = []
    for exercise, group in df.groupby('Exercise'):
        group_sorted = group.sort_values('Date')
        if len(group_sorted) < n:
            continue  # skip exercises with fewer than n records

        first_avg = group_sorted['Max3'].head(n).mean()
        last_avg = group_sorted['Max3'].tail(n).mean()

        # Compute 6m-ago window
        most_recent_date = group_sorted['Date'].max()
        six_month_cutoff = most_recent_date - pd.DateOffset(months=6)
        six_month_group = group_sorted[group_sorted['Date'] <= six_month_cutoff]
        if len(six_month_group) >= n:
            sixmo_avg = six_month_group['Max3'].tail(n).mean()
        else:
            sixmo_avg = np.nan

        # Compute percent changes
        if pd.notna(first_avg) and pd.notna(last_avg) and first_avg != 0:
            pct_change = ((last_avg - first_avg) / first_avg) * 100
        else:
            pct_change = np.nan

        if pd.notna(sixmo_avg) and pd.notna(last_avg) and sixmo_avg != 0:
            pct_change_6m = ((last_avg - sixmo_avg) / sixmo_avg) * 100
        else:
            pct_change_6m = np.nan

        results.append({
            'Exercise': exercise,
            'First3 Avg': round(first_avg, 1) if pd.notna(first_avg) else np.nan,
            '6m Ago Avg': round(sixmo_avg, 1) if pd.notna(sixmo_avg) else np.nan,
            'Last3 Avg Strength': round(last_avg, 1) if pd.notna(last_avg) else np.nan,
            'Percent Change (6m)': round(pct_change_6m, 1) if pd.notna(pct_change_6m) else np.nan,
            'Percent Change (All Time)': round(pct_change, 1) if pd.notna(pct_change) else np.nan
        })
    return pd.DataFrame(results)