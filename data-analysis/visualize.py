import pandas as pd
import os

def time_taken_grade():
    # combine all dataframes into one
    # find min and max times for time taken
    # find min and max grade 
    # plot 
    years = ["F20", "F21", "F22"]
    for year in years:
        dir_list = sorted(os.listdir(f"../data/clean/{year}/HW"))
        print("directory list: ", dir_list)
        df_total = pd.DataFrame(list()) # create empty csv file 
        df_total.to_csv('merged_df.csv')
        print(df_total)
        print("-----------------")
        for path in dir_list:
            print("path: " + path) # name of file
            df = pd.read_csv(f"data/clean/{year}/HW/{path}") # reading each file 

            df_total = pd.merge(df, df_total, how='inner',on=['Time taken','Grade/20.00'])

    print(df_total)




   # data = pd.read_csv(f'data/clean/{year}/HW') # reading csv

if __name__ == "__main__":
	time_taken_grade()