import numpy as np
import pandas as pd
import streamlit as st
from st_pages import add_indentation
from streamlit.runtime.uploaded_file_manager import UploadedFile
from utils import clean_assignment_csv
import plotly.express as px
import openpyxl


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


def set_time_window(deadlines: pd.DataFrame) -> pd.DataFrame:
    def calculate_windows(total_seconds: int, window: str) -> tuple[int, int]:
        # Define time window ranges for grouping
        early_range = (0, 0.25)  # student started within 0-25% of elapsed time
        mid_range = (0.25, 0.75)  # student started within 25%-75% of elapsed time
        late_range = (0.75, 1.0)  # student started within 75-100% of elapsed time

        start = 0
        end = 0

        if window == "early":
            start = total_seconds
            end = total_seconds - total_seconds * early_range[1]
        elif window == "mid":
            start = total_seconds - total_seconds * mid_range[0]
            end = total_seconds - total_seconds * mid_range[1]
        elif window == "late":
            start = total_seconds - total_seconds * late_range[0]
            end = 0

        return (int(start), int(end))

    # Calculate the time window for each assignment
    deadlines["time_window"] = deadlines.apply(
        lambda row: row["Close Datetime"] - row["Open Datetime"], axis=1
    )

    # Convert days to hours and extract components (hours, minutes, seconds)
    deadlines["hours"] = deadlines["time_window"].dt.total_seconds() / 3600
    deadlines["minutes"] = deadlines["time_window"].dt.components["minutes"]
    deadlines["seconds"] = deadlines["time_window"].dt.components["seconds"]

    # Format the result as HH:MM:SS
    deadlines["formatted_time"] = deadlines.apply(
        lambda row: f"{int(row['hours'])}:{row['minutes']}:{row['seconds']}",
        axis=1,
    )

    # Convert formatted time to total seconds
    deadlines["total_seconds"] = pd.to_timedelta(
        deadlines["formatted_time"]
    ).dt.total_seconds()

    # Calculate time windows for grouping
    deadlines["early_window"] = deadlines["total_seconds"].apply(
        lambda secs: calculate_windows(secs, "early")
    )

    deadlines["middle_window"] = deadlines["total_seconds"].apply(
        lambda secs: calculate_windows(secs, "mid")
    )

    deadlines["late_window"] = deadlines["total_seconds"].apply(
        lambda secs: calculate_windows(secs, "late")
    )

    return deadlines


def clean_deadlines(df: pd.DataFrame):
    df.rename(
        columns={
            "Quiz type": "Assignment Type",
            "Quizz type": "Assignment Type",
            "Quiz number": "Assignment Number",
        },
        inplace=True,
    )
    df["Assignment"] = df["Assignment Type"] + " " + df["Assignment Number"].astype(str)

    df["Open date"] = df["Open date"].astype(str)
    df["Open time"] = (
        df["Open time"].astype(str).apply(lambda x: x.replace("1900-01-01", ""))
    )

    df["Open Datetime"] = pd.to_datetime(
        df["Open date"] + " " + df["Open time"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce",
    )

    df["Close date"] = df["Close date"].astype(str)
    df["Close time"] = (
        df["Close time"].astype(str).apply(lambda x: x.replace("1900-01-01", ""))
    )
    df["Close Datetime"] = pd.to_datetime(
        df["Close date"] + " " + df["Close time"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce",
    )

    df["Open Datetime"].fillna(pd.to_datetime(0), inplace=True)
    df["Close Datetime"].fillna(pd.to_datetime(0), inplace=True)

    df = set_time_window(df)
    df.drop(
        [
            "Open date",
            "Open time",
            "Close date",
            "Close time",
        ],
        axis=1,
        inplace=True,
    )

    return df


def show_student_list(in_df: pd.DataFrame):
    cols_not_to_drop = ["First Name", "Surname", "Student ID", "Email Address"]
    cols_to_drop = [col for col in in_df.columns if col not in cols_not_to_drop]
    student_list = in_df.drop_duplicates(subset="Student ID").drop(columns=cols_to_drop)

    return student_list


def get_assignments_by_student_id(
    assignments: pd.DataFrame, student_id: int
) -> pd.DataFrame:
    """
    Returns all assignments for a given student id in one dataframe.
    """
    student_assignments = assignments.loc[
        assignments["Student ID"] == student_id
    ].sort_values(by="Assignment Name")

    return student_assignments


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


def get_assignment_deadline_row(assignment_name: str, deadlines: pd.DataFrame):
    assignment_type_map = {
        "Homework": ["homework", "hw"],
        "Lab": ["lab", "lb"],
        "Midterm": ["midterm", "me"],
        "Final": ["final", "fe"],
        "Project": ["project", "pj"],
    }
    assignment_type = None
    assignment_num = None
    for key, val in assignment_type_map.items():
        for term in val:
            if term in assignment_name.lower():
                assignment_type = key
                assignment_num = int(assignment_name.lower().split(term)[1])

    deadline = deadlines.loc[
        (deadlines["Assignment Type"] == assignment_type)
        & (deadlines["Assignment Number"] == assignment_num)
    ]
    return deadline


def mark_submission_status(
    assignment: pd.DataFrame, deadlines: pd.DataFrame
) -> pd.DataFrame:
    def set_submission_status(row: object, deadlines: pd.DataFrame):
        deadline = get_assignment_deadline_row(row["Assignment Name"], deadlines)

        student_start: np.datetime64 = np.datetime64(row["Start Time"])
        assignment_open: np.datetime64 = deadline["Open Datetime"].values[0]
        time_difference_nano = student_start - assignment_open
        time_difference = time_difference_nano.astype("timedelta64[s]").astype(int)

        status = None
        early_window: tuple[int, int] = deadline["early_window"].values[0]
        middle_window: tuple[int, int] = deadline["middle_window"].values[0]
        late_window: tuple[int, int] = deadline["late_window"].values[0]
        if time_difference >= early_window[1]:
            status = "Last Minute"
        elif middle_window[1] <= time_difference < middle_window[0]:
            status = "Moderate"
        else:
            status = "Early Bird"

        return status

    assignment["Submission Type"] = assignment.apply(
        lambda row: set_submission_status(row, deadlines), axis="columns"
    )
    assignment["Assignment Closed"] = assignment.apply(
        lambda row: get_assignment_deadline_row(row["Assignment Name"], deadlines)[
            "Close Datetime"
        ].values[0],
        axis="columns",
    )
    return assignment


def create_student_line_chart(student_assignments: pd.DataFrame):
    """
    Creates a line chart to show a students grade for each assignment.
    """
    graph_title = f"{student_assignments['First Name'].values[0]} {student_assignments['Surname'].values[0]}'s Term Assignment Performance"
    line_chart = px.scatter(
        student_assignments,
        x="Assignment Name",
        y="Grade/20",
        range_y=(0, 23),
        title=graph_title,
        category_orders={
            "Assignment Name": student_assignments["Assignment Name"]
            .sort_values()
            .tolist()
        },
        color="Submission Type",
        color_discrete_map={
            "Early Bird": "green",
            "Moderate": "orange",
            "Last Minute": "red",
        },
        hover_data=[
            "Time Taken",
            "Start Time",
            "Submission Type",
            "Assignment Closed",
        ],
    )

    return line_chart


def student_submissions_page_content(csvs: list[UploadedFile], assignment_type: str):
    if len(csvs) > 0:
        deadlines_file = st.file_uploader(
            "Upload the file containing the deadlines",
            type=["csv", "xlsx"],
            accept_multiple_files=False,
        )
        if deadlines_file is not None:
            assignments = read_assignments(csvs)
            deadlines_df = None
            deadlines_filetype = deadlines_file.name.split(".")[-1]
            if deadlines_filetype == "xlsx":
                excel = pd.ExcelFile(deadlines_file)
                sheet_name = st.selectbox(
                    "Multiple sheets detected, select deadline sheet:",
                    excel.sheet_names,
                    index=None,
                )
                if sheet_name is not None:
                    deadlines_df = pd.read_excel(excel, sheet_name=sheet_name)
            elif deadlines_filetype == "csv":
                deadlines_df = pd.read_csv(deadlines_file)

            if deadlines_df is not None:
                deadlines = clean_deadlines(deadlines_df)
                student_roster = show_student_list(assignments)
                st.header("Class List")
                st.dataframe(
                    student_roster.style.format(
                        {"Student ID": lambda x: "{:}".format(x)}
                    ),
                    use_container_width=True,
                )
                inp = st.text_input("Enter a Student ID for class performance")
                id = "".join(inp.split(","))
                if (
                    len(id) > 0
                    and str.isdigit(id)
                    and int(id) in assignments["Student ID"].astype("int").tolist()
                ):
                    student_assignments = get_assignments_by_student_id(
                        assignments, int(id)
                    )
                    student_submission_patterns = mark_submission_status(
                        student_assignments, deadlines
                    )
                    # Show table of a student's assignment metrics (mean, std, mode, etc)
                    description = get_student_assignments_description(
                        student_assignments
                    )
                    st.dataframe(
                        description,
                        use_container_width=True,
                    )

                    # Create line chart figure
                    line_chart = create_student_line_chart(student_submission_patterns)
                    # Display line chart on site
                    st.plotly_chart(line_chart)


add_indentation()
st.title("Student Submission Patterns")
st.subheader("Analysis and Visualization of Students' Submission Patterns")
st.caption(
    "Students can be categorized into three categories: those who start assignments early, those who start assignments in the middle, and those who start assignments late. Students who start within 25% of the elapsed time from when the assignment opened are considered 'early,' students who start within 25-75% of the elapsed time are considered 'middle,' and those who start after 75% of the elapsed time are considered 'late.' Upload a file containing the deadlines of each assignment and the assignment name first. Then upload multiple assignment files, and use this page to search for specific students to see their submission patterns ('early', 'middle', or 'late') and their corresponding performance throughout the term."
)

hw_tab, lab_tab, midterm_tab, final_tab, project_tab = st.tabs(
    ["Homework", "Lab", "Midterm", "Final", "Project"]
)
csvs: list[UploadedFile] = []
assignment_type = ""
with hw_tab:
    csvs = st.file_uploader(
        "Upload homework CSVs", type=["csv", "xlsx"], accept_multiple_files=True
    )
    assignment_type = "Homework"
    student_submissions_page_content(csvs, assignment_type)

with lab_tab:
    csvs = st.file_uploader(
        "Upload lab CSVs", type=["csv", "xlsx"], accept_multiple_files=True
    )
    assignment_type = "Lab"
    student_submissions_page_content(csvs, assignment_type)
with midterm_tab:
    csvs = st.file_uploader(
        "Upload midterm exam CSVs", type=["csv", "xlsx"], accept_multiple_files=True
    )
    assignment_type = "Midterm"
    student_submissions_page_content(csvs, assignment_type)
with final_tab:
    csvs = st.file_uploader(
        "Upload final exam CSVs", type=["csv", "xlsx"], accept_multiple_files=True
    )
    assignment_type = "Final"
    student_submissions_page_content(csvs, assignment_type)
with project_tab:
    csvs = st.file_uploader(
        "Upload project CSVs", type=["csv", "xlsx"], accept_multiple_files=True
    )
    assignment_type = "Project"
    student_submissions_page_content(csvs, assignment_type)
