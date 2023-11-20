import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

years = ["F20", "F21", "F22"]


def merge_df():
    # Combine all dataframes into one
    for year in years:
        dir_list = sorted(os.listdir(f"../clean/{year}/HW"))
        df_total = pd.DataFrame()  # Create an empty DataFrame

        for path in dir_list:
            df = pd.read_csv(f"../clean/{year}/HW/{path}")  # Read each file
            df_total = pd.concat([df_total, df], axis=0)

        # Select specific columns in the DataFrame
        df_total = df_total[
            ["State", "Started on", "Completed", "Time taken", "Grade/20.00"]
        ]

        # Write a separate CSV file for each year
        output_file = f"merged_df_{year}_hw.csv"
        df_total.to_csv(output_file, index=False)


def time_taken_corr_grade():
    for year in years:
        df = pd.read_csv(f"merged_df_{year}_hw.csv")
        time_taken = df["Time taken"]
        grade = df["Grade/20.00"]
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


def time_of_day_grade():
    years = ["F20", "F22"]  # no visualization for F21 because time (AM/PM) is not noted
    for year in years:
        df = pd.read_csv(f"merged_df_{year}_hw.csv")
        grade = df["Grade/20.00"]
        date_string = df["Completed"]
        date_format = "%d %B %Y %I:%M %p"  # converting date
        parsed_date = pd.to_datetime(date_string, format=date_format)
        # time = parsed_date.dt.time
        # Calculate time in hours since midnight
        time_hours = parsed_date.dt.hour + parsed_date.dt.minute / 60
        plt.scatter(time_hours, grade)
        plt.xlabel("Time in Hours Since 12AM")
        plt.ylabel("Grade/20.00")
        plt.title(f"Grade vs. Assignment Submission Time for {year}")
        # Show legend
        plt.legend()
        plt.show()


def group_hw_grades_by_id():
    for year in years:
        hw_dir = f"../clean/{year}/HW"
        hw_files = sorted(os.listdir(hw_dir))

        combined_df = pd.DataFrame(columns=["ID number"])

        for file in hw_files:
            current_df = pd.read_csv(f"{hw_dir}/{file}")
            df_grades = current_df[["ID number", "Grade/20.00"]]
            combined_df = pd.merge(
                combined_df,
                df_grades,
                on="ID number",
                how="outer",
                suffixes=("", "_" + file[:-4]),
            )

        output_file = f"{year}_hw_grades_by_id.csv"
        combined_df.to_csv(output_file, index=False)

def find_hw_length_corr_grade():
    return



if __name__ == "__main__":
    #find_hw_length_corr_grade()
    merge_df()
