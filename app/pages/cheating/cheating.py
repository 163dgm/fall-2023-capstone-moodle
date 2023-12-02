import pandas as pd
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from st_pages import add_indentation
from utils import clean_assignment_csv, get_col_by_id


def find_potential_cheaters(df: pd.DataFrame) -> pd.DataFrame:
    outliers = pd.DataFrame()
    time_col = df["Time Taken"]

    # IQR lower bound was returning negative numbers so it was inaccurate, instead
    # we check if the time taken was two standard deviations from the mean
    mean = time_col.mean()
    std = time_col.std()

    # Select all columns where the time was less than 1 standard dev from mean
    outliers = df[time_col < (mean - (1 * std))]

    return outliers[outliers["Grade/20"].astype("float") > 18]


def find_cheaters_in_multiple_files(files: list[UploadedFile]):
    repeat_offenders = {}
    for file in files:
        df = pd.read_csv(file)
        df = clean_assignment_csv(df)
        cheaters = find_potential_cheaters(df)

        for id in cheaters["Student ID"]:
            repeat_offenders[id] = repeat_offenders.get(
                id,
                [
                    get_col_by_id(df, id, "First Name"),
                    get_col_by_id(df, id, "Surname"),
                    0,
                    set(),
                ],
            )
            repeat_offenders[id][3].add(file.name.split(".csv")[0])
            repeat_offenders[id][2] = len(repeat_offenders[id][3])

    df = pd.DataFrame(
        data=list(map(lambda x: [x[0]] + x[1], repeat_offenders.items())),
        columns=[
            "Student ID",
            "First Name",
            "Last Name",
            "Assignments Flagged",
            "Assignment Names",
        ],
    )
    df["Assignment Names"] = df["Assignment Names"].apply(lambda x: sorted(x))

    return df


def get_assignments_cheated_on(cheaters: pd.DataFrame):
    exploded = cheaters.explode("Assignment Names")
    assgn_cheated = (
        exploded.groupby("Assignment Names")
        .size()
        .reset_index(name="Total Students Flagged")
    )

    assgn_cheated.columns = ["Assignment Name", "Total Students Flagged"]

    return assgn_cheated


add_indentation()
st.title("Detect Cheating in Recent Assignments")


csvs = st.file_uploader("Choose a file", type="csv", accept_multiple_files=True)
if len(csvs) > 0:
    cheaters = find_cheaters_in_multiple_files(csvs)
    s = cheaters.style.format({"Student ID": lambda x: "{:}".format(x)})

    st.dataframe(s, use_container_width=True)

    assignments_cheated_on = get_assignments_cheated_on(cheaters)
    st.bar_chart(
        assignments_cheated_on, x="Assignment Name", y="Total Students Flagged"
    )
