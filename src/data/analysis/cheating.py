import os
import numpy as np
import pandas as pd


def find_potential_cheaters(df: pd.DataFrame) -> pd.DataFrame:
    outliers = pd.DataFrame()
    time_col = df["Time taken"]

    desc = time_col.describe()
    # IQR lower bound was returning negative numbers so it was inaccurate, instead
    # we check if the time taken was two standard deviations from the mean
    mean = desc["mean"]
    std = desc["std"]

    # Select all columns where the time was less than 1 standard dev from mean
    outliers = df[time_col < (mean - (1 * std))]

    return outliers[outliers["Grade/20.00"] > 18]


def find_cheaters_in_multiple_files(files: list[str]):
    repeat_offenders = {}

    for file in files:
        df = pd.read_csv(file)
        cheaters = find_potential_cheaters(df)
        # print(f"{year} {file} potential cheaters", cheaters["ID number"].to_list())

        for id in cheaters["ID number"]:
            repeat_offenders[id] = repeat_offenders.get(id, 0) + 1

    return repeat_offenders


def print_all_cheaters():
    years = ["F20", "F21", "F22"]

    for year in years:
        hw_dir = f"../clean/{year}/HW"
        hw_files = list(map(lambda x: hw_dir + "/" + x, sorted(os.listdir(hw_dir))))
        find_cheaters_in_multiple_files(hw_files)


if __name__ == "__main__":
    print_all_cheaters()
