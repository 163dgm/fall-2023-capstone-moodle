import pandas as pd
import os

def merge_df():
    # combine all dataframes into one
    # find min and max times for time taken
    # find min and max grade 
    # plot 
    years = ["F20", "F21", "F22"]
    for year in years:
        dir_list = sorted(os.listdir(f"../data/clean/{year}/HW"))
        df_total = pd.DataFrame(list()) # create empty csv file 
        df_total.to_csv('merged_df.csv')
        for path in dir_list:
            df = pd.read_csv(f"../data/clean/{year}/HW/{path}") # reading each file 
            df_total = pd.concat([df_total, df], axis = 0)
        # Select specific columns in the DataFrame
        df_total = df_total[['State', 'Started on','Completed','Time taken','Grade/20.00']]

    df_total.to_csv('merged_df.csv', index=False)

   # data = pd.read_csv(f'data/clean/{year}/HW') # reading csv

if __name__ == "__main__":
	merge_df()