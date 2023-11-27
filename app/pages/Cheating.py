import pandas as pd
import streamlit as st


def str_time_to_minutes(time_str: str) -> int:
    hour_strs = ["hour", "hours"]
    min_strs = ["min", "mins"]
    sec_strs = ["sec", "secs"]

    def count_occurance(orig_str: list[str], terms: list[str]) -> int:
        count = 0
        for term in terms:
            if term in split_str:
                count = int(orig_str[orig_str.index(term) - 1])
        return count

    split_str = time_str.split(" ")

    hours = count_occurance(split_str, hour_strs)
    mins = count_occurance(split_str, min_strs)
    secs = count_occurance(split_str, sec_strs)

    total_mins = (hours * 60) + mins + (secs / 60)
    return round(total_mins, 2)


def get_col_by_id(df: pd.DataFrame, given_id: int, col_to_find: str):
    return df.loc[df["ID number"] == given_id, col_to_find].values[0]


def find_potential_cheaters(df: pd.DataFrame) -> pd.DataFrame:
    outliers = pd.DataFrame()
    time_col = df["Time taken"]

    # IQR lower bound was returning negative numbers so it was inaccurate, instead
    # we check if the time taken was two standard deviations from the mean
    mean = time_col.mean()
    std = time_col.std()

    # Select all columns where the time was less than 1 standard dev from mean
    outliers = df[time_col < (mean - (1 * std))]

    return outliers[outliers["Grade/20.00"].astype("float") > 18]


def clean_csv(df: str):
    df = df.drop(df[df["State"] != "Finished"].index)

    # Convert string time taken to minutes
    df["Time taken"] = df["Time taken"].apply(str_time_to_minutes)

    return df


def find_cheaters_in_multiple_files(files: list[str]):
    repeat_offenders = {}

    for file in files:
        df = pd.read_csv(file)
        df = clean_csv(df)
        cheaters = find_potential_cheaters(df)

        for id in cheaters["ID number"]:
            repeat_offenders[id] = repeat_offenders.get(
                id,
                [
                    get_col_by_id(df, id, "First name"),
                    get_col_by_id(df, id, "Surname"),
                    0,
                ],
            )
            repeat_offenders[id][2] += 1

    df = pd.DataFrame(
        data=list(map(lambda x: [x[0]] + x[1], repeat_offenders.items())),
        columns=["Student ID", "First Name", "Last Name", "Assignments Flagged"],
    )
    df["Student ID"] = df["Student ID"].astype("longlong")

    # df.set_index("Student ID", inplace=True)

    return df


st.title("Detect Cheating in Recent Assignments")

csvs = st.file_uploader("Choose a file", type="csv", accept_multiple_files=True)
if len(csvs) > 0:
    cheaters = find_cheaters_in_multiple_files(csvs)
    cheaters = cheaters.style.hide(axis="index")
    st.dataframe(data=cheaters)
