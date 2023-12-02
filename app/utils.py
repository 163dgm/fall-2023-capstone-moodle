import pandas as pd

COLUMN_RENAME_MAP = {
    "Surname": "Surname",
    "First name": "First Name",
    "ID number": "Student ID",
    "Email address": "Email Address",
    "State": "Status",
    "Started on": "Start Time",
    "Completed": "Complete Time",
    "Time taken": "Time Taken",
    "Grade/20.00": "Grade/20",
}


def rename_columns(df: pd.DataFrame):
    return df.rename(columns=COLUMN_RENAME_MAP)


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


def clean_assignment_csv(df: pd.DataFrame):
    df = df.drop(df[df["State"] != "Finished"].index)

    # Convert string time taken to minutes
    df["Time taken"] = df["Time taken"].apply(str_time_to_minutes)
    df["Started on"] = pd.to_datetime(df["Started on"], format="%d %B %Y %I:%M %p")
    df["Completed"] = pd.to_datetime(df["Completed"], format="%d %B %Y %I:%M %p")
    df["ID number"] = df["ID number"].astype("int")
    df["Grade/20.00"] = df["Grade/20.00"].astype("float")

    df = rename_columns(df)

    return df


def get_col_by_id(df: pd.DataFrame, given_id: int, col_to_find: str):
    return df.loc[df["Student ID"] == given_id, col_to_find].values[0]


def chunk_list(lst: list, num: int):
    for i in range(0, len(lst), num):
        yield lst[i : i + num]
