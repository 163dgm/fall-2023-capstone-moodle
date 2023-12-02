import pandas as pd
import streamlit as st
from st_pages import add_indentation
from streamlit.runtime.uploaded_file_manager import UploadedFile
from utils import clean_assignment_csv
import plotly.express as px


def read_assignments(csvs: list[UploadedFile]):
    assignments = pd.DataFrame()
    for csv in csvs:
        df = pd.read_csv(csv)
        df = clean_assignment_csv(df)
        df["Assignment Name"] = csv.name.split(".csv")[0]
        assignments = pd.concat([assignments, df], ignore_index=True)
    return assignments


add_indentation()
st.title("Student Term Performance")

csvs = st.file_uploader("Choose a file", type="csv", accept_multiple_files=True)
if len(csvs) > 0:
    assignments = read_assignments(csvs)
    id = st.text_input("Enter a Student ID")
    if len(id) > 0 and str.isdigit(id):
        # 28609357
        student_assignments = assignments.loc[
            assignments["Student ID"] == int(id)
        ].sort_values(by="Assignment Name")
        graph_title = f"{student_assignments['First Name'].values[0]} {student_assignments['Surname'].values[0]}'s Term Assignment Performance"
        graph = px.line(
            student_assignments,
            x="Assignment Name",
            y="Grade/20",
            markers=True,
            title=graph_title,
            hover_data=["Time Taken", "Start Time"],
        )
        st.plotly_chart(graph)
        st.dataframe(
            student_assignments.describe(include=[float, int])
            .drop(
                columns="Student ID",
            )
            .drop(["count"]),
            use_container_width=True,
        )
