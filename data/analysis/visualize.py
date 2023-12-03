import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

years = ["F20", "F21", "F22"]


def merge_df(): # creates merged_df_{year}_hw.csv
    # Combine all dataframes into one
    for year in years:
        dir_list = sorted(os.listdir(f"../clean/{year}/HW"))
        df_total = pd.DataFrame()  # Create an empty DataFrame

        for path in dir_list:
            df = pd.read_csv(f"../clean/{year}/HW/{path}")  # Read each file
            df_total = pd.concat([df_total, df], axis=0)

        df_total.columns = df_total.columns.str.lower() #case insensitive
        
        # Select specific columns in the DataFrame
        df_total["id number"] = df_total["id number"].astype(int)
        #print(type(df_total["id number"]))
        selected_columns = ["id number", "state", "started on", "completed", "time taken", "grade/20.00"]
        df_total = df_total[selected_columns]
        # print(df_total)
        
        # Write a separate CSV file for each year
        output_file = f"merged_df_{year}_hw.csv"
        df_total.to_csv(output_file, index=False)


def time_taken_corr_grade():
    for year in years:
        df = pd.read_csv(f"merged_df_{year}_hw.csv")
        time_taken = df["time taken"]
        grade = df["grade/20.00"]
        # Perform linear regression to find the line of best fit
        slope, intercept = np.polyfit(time_taken, grade, 1)
        # Create the line of best fit
        line_of_best_fit = slope * np.array(time_taken) + intercept
        plt.scatter(time_taken, grade)
        # Plot the line of best fit
        plt.plot(time_taken, line_of_best_fit, color="red", label="Line of Best Fit")
        # Set labels and title
        plt.xlabel("Time Taken")
        plt.ylabel("Grade/20.00")
        plt.title(f"Grade vs. Time Taken for {year}")
        # Show legend
        plt.legend()
        plt.show()


def time_of_day_grade(): # time of day assignment is submitted, corresponding grade
    # group by time of day they do it, assume time of day they do it is submission time
    # 4 groups: morning (6am-12pm), afternoon (12:01pm-5pm), 
    # evening (5:01pm-8pm), night (8:01pm-5:59am)
    # take average of each group, bar chart 
    # y-axis: grade/20, x-axis: group
    # DICT: KEY IS TIME, VALUE IS PERFORMANCE
    
    # Define time ranges
    morning_range = pd.to_datetime(["06:00:00", "12:00:00"]).time
    afternoon_range = pd.to_datetime(["12:01:00", "17:00:00"]).time
    evening_range = pd.to_datetime(["17:01:00", "20:00:00"]).time
    night_range = pd.to_datetime(["20:01:00", "23:59:59"]).time

    years = ["F20", "F22"]  # no visualization for F21 because time (AM/PM) is not noted
    
    for year in years:
        df = pd.read_csv(f"merged_df_{year}_hw.csv")
        date_string = df["completed"]
        date_format = "%d %B %Y %I:%M %p"  # converting date
        parsed_date = pd.to_datetime(date_string, format=date_format)
        time = parsed_date.dt.time

        # Initialize dictionaries to store grades for each time of day
        morning = dict()
        afternoon = dict()
        evening = dict()
        night = dict()

        # Loop through each row in the dataframe
        for index, row in df.iterrows():
            grade = row["grade/20.00"]

            # Determine the time of day and add the grade to the corresponding dictionary
            if morning_range[0] <= time[index] <= morning_range[1]:
                morning[index] = grade
            elif afternoon_range[0] <= time[index] <= afternoon_range[1]:
                afternoon[index] = grade
            elif evening_range[0] <= time[index] <= evening_range[1]:
                evening[index] = grade
            elif night_range[0] <= time[index] <= night_range[1]:
                night[index] = grade

        # Calculate average grade for each time of day
        avg_morning = sum(morning.values()) / len(morning) if morning else 0
        avg_afternoon = sum(afternoon.values()) / len(afternoon) if afternoon else 0
        avg_evening = sum(evening.values()) / len(evening) if evening else 0
        avg_night = sum(night.values()) / len(night) if night else 0

        # Plotting
        times_of_day = ["Morning", "Afternoon", "Evening", "Night"]
        average_grades = [avg_morning, avg_afternoon, avg_evening, avg_night]
        plt.bar(times_of_day, average_grades)
        plt.xlabel("Time of Day")
        plt.ylabel("Average Grade/20.00")
        plt.title(f"Average Grade vs. Time of Day for {year}")
        plt.show()



def group_hw_grades_by_id():
    for year in years:
        hw_dir = f"../clean/{year}/HW"
        hw_files = sorted(os.listdir(hw_dir))

        combined_df = pd.DataFrame(columns=["ID number"])

        for file in hw_files:
            current_df = pd.read_csv(f"{hw_dir}/{file}")
            df_grades = current_df[["id number", "grade/20.00"]]
            combined_df = pd.merge(
                combined_df,
                df_grades,
                on="id number",
                how="outer",
                suffixes=("", "_" + file[:-4]),
            )

        output_file = f"{year}_hw_grades_by_id.csv"
        combined_df.to_csv(output_file, index=False)

def find_hw_length_corr_grade():
    return



if __name__ == "__main__":
    #find_hw_length_corr_grade()
   time_of_day_grade()

  
