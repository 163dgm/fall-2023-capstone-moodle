import os
import pandas as pd

def merge_df():
    # Combine all dataframes into one
    years = ["F20", "F21", "F22"]
    for year in years:
        dir_list = sorted(os.listdir(f"../data/clean/{year}/HW"))
        df_total = pd.DataFrame()  # Create an empty DataFrame

        for path in dir_list:
            df = pd.read_csv(f"../data/clean/{year}/HW/{path}")  # Read each file
            df_total = pd.concat([df_total, df], axis=0)

        # Select specific columns in the DataFrame
        df_total = df_total[['State', 'Started on', 'Completed', 'Time taken', 'Grade/20.00']]

        # Write a separate CSV file for each year
        output_file = f'merged_df_{year}.csv'
        df_total.to_csv(output_file, index=False)



def time_taken_corr_grade():
    df = pd.read_csv('merged_df.csv') 
    time_taken = df[['Time taken']]
    grade = df[['Grade/20.00']]

    for time in time_taken:
        min = time



    # find min and max times for time taken
    # find min and max grade 
    # plot 


if __name__ == "__main__":
	merge_df()
    #time_taken_corr_grade()