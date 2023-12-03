import pandas as pd
import streamlit as st
from st_pages import add_indentation
from streamlit.runtime.uploaded_file_manager import UploadedFile
from utils import clean_assignment_csv
import os
import plotly.express as px


def read_assignments(csvs: list[UploadedFile]):
    """
    Take multiple assignment CSVs and combine them into one big dataframe.
    """
    combined_assignments = pd.DataFrame()
    for csv in csvs:
        df = pd.read_csv(csv)
        df = clean_assignment_csv(df)
        # Add new column "Assignment Name" that is the name of the file uploaded (without .csv)
        df["Assignment Name"] = csv.name.split(".csv")[0]

        # Add cleaned assignment dataframe to one big dataframe
        combined_assignments = pd.concat([combined_assignments, df], ignore_index=True)

    return combined_assignments


def get_assignments_by_student_id(
    assignments: pd.DataFrame, student_id: int
) -> pd.DataFrame:
    """
    Returns all assignments for a given student id in one dataframe.
    """
    return assignments.loc[assignments["Student ID"] == student_id].sort_values(
        by="Assignment Name"
    )


def create_student_line_chart(student_assignments: pd.DataFrame):
    """
    Creates a line chart to show a students grade for each assignment.
    """
    graph_title = f"{student_assignments['First Name'].values[0]} {student_assignments['Surname'].values[0]}'s Term Assignment Performance"
    line_chart = px.line(
        student_assignments,
        x="Assignment Name",
        y="Grade/20",
        markers=True,
        title=graph_title,
        hover_data=["Time Taken", "Start Time"],
    )

    return line_chart


def get_student_assignments_description(student_assignments: pd.DataFrame):
    """
    Gets the descriptive statistics of a given student's assignments.
    """
    filtered_description = (
        # Get mean median mode, etc of student assignments but only for int/float values
        student_assignments.describe(include=[float, int])
        # Get rid of Student ID since its an int, but not useful to us
        .drop(
            columns="Student ID",
        )
        # Drop count, don't need this for assignments
        .drop(["count"])
    )

    return filtered_description

# Example usage:
# Assuming you have a DataFrame 'hw_assignments' with columns like 'student_id', 'open_day', 'open_time', 'close_day', 'close_time'
# grouped_assignments = group_students(hw_assignments)

# You can then analyze or visualize the grouped_assignments DataFrame as needed.

    


# search for one student
# flag the assignment if they have a 10% difference of the average of their previous ones
# if they fail one, dont count that towards average--> ignore flagged hw

#def ignore_flagged_hw():


add_indentation()
st.title("Student Submission Patterns")

deadlines = st.file_uploader("Upload the file containing the deadlines", type="csv", accept_multiple_files=False)

csvs = st.file_uploader("Choose a file", type="csv", accept_multiple_files=True)
if len(csvs) > 0:
    id = st.text_input("Enter a Student ID")
    if len(id) > 0 and str.isdigit(id):
        # 28609357
        assignments = read_assignments(csvs)
        student_assignments = get_assignments_by_student_id(assignments, int(id))

        # Create line chart figure
        line_chart = create_student_line_chart(student_assignments)
        # Display line chart on site
        st.plotly_chart(line_chart)

        # Show table of a student's assignment metrics (mean, std, mode, etc)
        description = get_student_assignments_description(student_assignments)
        st.dataframe(
            description,
            use_container_width=True,
        )
