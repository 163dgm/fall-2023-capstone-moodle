from st_pages import add_indentation
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit.runtime.uploaded_file_manager import UploadedFile
from utils import clean_assignment_csv


def find_collaboration(in_df: pd.DataFrame):
    collab = pd.DataFrame()
    time_diff = np.timedelta64(15, "m")

    # Create a new column for the "Completed" time of the previous row
    in_df["Prev Completed"] = in_df["Complete Time"].shift(1)

    # Filter the DataFrame based on the time difference condition
    collab = in_df.loc[
        np.abs(in_df["Start Time"] - in_df["Prev Completed"]) <= time_diff
    ]

    # Drop the temporary column
    collab.drop(columns=["Prev Completed"], inplace=True)

    return collab


def get_assignment_collaboration(file: UploadedFile):
    df = pd.read_csv(file)
    df = clean_assignment_csv(df)
    return find_collaboration(df)


add_indentation()
st.title("Collaboration per Assignment")
st.subheader("Check if students may be working together on assignments")
st.caption(
    "One way students work together is by having one take the assignment using the full amount of time, and the others finish very quickly -- usually achieving the same score. By uploading an assignment we can see how long a student took on an assignment and their score. If there are two lines close to each other it could potentially mean collaboration. However, this is not conclusive evidence."
)


csv = st.file_uploader("Choose a file", type="csv", accept_multiple_files=False)
if csv is not None:
    collabs = get_assignment_collaboration(csv)

    timeline = px.timeline(
        collabs,
        x_start="Start Time",
        x_end="Complete Time",
        y="Grade/20",
        hover_data=["Student ID", "First Name", "Surname"],
        range_y=(0, 23),
    )
    st.plotly_chart(timeline)

    s = collabs.style.format(
        {
            "Student ID": lambda x: "{:}".format(x),
            "Time Taken": lambda x: "{:.2f}".format(x),
        }
    )
    st.dataframe(s)
