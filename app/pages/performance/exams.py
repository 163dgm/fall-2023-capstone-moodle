from st_pages import add_indentation
import streamlit as st
import pandas as pd
from streamlit.runtime.uploaded_file_manager import UploadedFile
from utils import clean_assignment_csv, get_col_value_by_student_id
import plotly.express as px


def get_grade_color_ranges():
    """
    Color ranges for pie chart, each corresponds to a letter grade.
    """
    return [
        "rgb(165,0,38)",  # Dark red
        "rgb(215,48,39)",  # Red
        "rgb(255,255,191)",  # Yellow
        "rgb(26,152,80)",  # Light green
        "rgb(0,104,55)",  # Dark green
    ]


def grade_to_letter(grade: int):
    """
    Convert number grade to letter grade.
    """
    if grade >= 18:
        return "A"
    elif grade >= 16:
        return "B"
    elif grade >= 14:
        return "C"
    elif grade >= 12:
        return "D"
    else:
        return "F"


def clean_exam(csv: UploadedFile):
    df = pd.read_csv(csv)
    df = clean_assignment_csv(df)
    # Add a new column "Letter Grade" that takes the adjacent Grade/20 and converts it to a letter
    df["Letter Grade"] = df["Grade/20"].apply(grade_to_letter)
    # Add new column "Assignment Name" that is the name of the file uploaded (without .csv)
    df["Assignment Name"] = csv.name.split(".csv")[0]
    # The pie chart wants to sum together a column's values. This sets each row to have the number 1,
    # so it can be summed and show the total number of students that got a certain grade.
    df["Students"] = 1
    return df


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


def clean_exam_for_table(exam: pd.DataFrame) -> pd.DataFrame:
    cols_not_to_drop = [
        "First Name",
        "Surname",
        "Grade/20",
        "Student ID",
        "Letter Grade",
    ]
    cols_to_drop = [col for col in exam.columns if col not in cols_not_to_drop]
    # Drop columns that are not listed in cols_not_to_drop
    cleaned_exam_df = exam.drop(columns=cols_to_drop)

    # streamlit dataframe tables show Student IDs and Grade/20 columns weirdly.
    # This format dict makes them look normal
    cleaned_exam_df = cleaned_exam_df.style.format(
        {
            # Removes decimals and commas from Student ID
            "Student ID": lambda x: "{:}".format(x),
            # Limits Grades to 2 decimal places
            "Grade/20": lambda x: "{:.2f}".format(x),
        }
    )

    return cleaned_exam_df


def combine_student_assignments_exam(
    student_assignments: pd.DataFrame, exam: pd.DataFrame
) -> pd.DataFrame:
    """
    Combine a student's assignments dataframe and their exam dataframe for displaying a bar chart.
    """
    # Get student ID from assignments since this only contains one student
    student_id = student_assignments["Student ID"].values[0]
    # Create new dataframe that is just average of the assignments
    assignment_avg = pd.DataFrame(
        {
            "Surname": get_col_value_by_student_id(
                student_assignments, student_id, "Surname"
            ),
            "First Name": get_col_value_by_student_id(
                student_assignments, student_id, "First Name"
            ),
            "Student ID": student_id,
            "Assignment Name": "Assignment Mean",
            "Grade/20": student_assignments["Grade/20"].mean(),
        },
        # Have to mannually add an index
        index=[0],
    )
    student_assignments = pd.concat([student_assignments, assignment_avg])

    combined = pd.concat([student_assignments, exam], ignore_index=True)
    # Exam dataframe contains other students so we locate the student we want
    student_comparison = combined.loc[combined["Student ID"] == student_id].sort_values(
        by="Assignment Name"
    )
    return student_comparison


add_indentation()
st.title("Exam Performance")
st.subheader("Visualize exam results in relation to previous assignments")
st.caption(
    "Class assignments are a reflection of the material students will be tested on. Use this page to upload exam results and see if students are performing the same on exams as assignments."
)


exam_csv = st.file_uploader(
    "Upload an exam file", type="csv", accept_multiple_files=False
)
if exam_csv is not None:
    exam = clean_exam(exam_csv)

    left_col, right_col = st.columns(2)
    with left_col:
        table_exam = clean_exam_for_table(exam)
        st.dataframe(
            table_exam,
            column_order=(
                "Student ID",
                "Surname",
                "First Name",
                "Letter Grade",
                "Grade/20",
            ),
            hide_index=True,
        )
    with right_col:
        pie = px.pie(
            exam,
            values="Students",
            names="Letter Grade",
            color_discrete_sequence=get_grade_color_ranges(),
        )
        st.plotly_chart(pie, use_container_width=True)

    assignment_csvs = st.file_uploader(
        "Upload pre-exam assignment CSVs", type="csv", accept_multiple_files=True
    )
    if len(assignment_csvs) > 0:
        assignments = read_assignments(assignment_csvs)
        input = st.text_input("Enter a Student ID")
        # Make sure the inputted value is a number and not a string
        if len(input) > 0 and str.isdigit(input):
            # Cast to input int
            id = int(input)

            student_assignments = get_assignments_by_student_id(assignments, id)

            # Make sure the student who took the exam actually has completed assignments
            # Not sure why they would take an exam without completing any assignments but it happens
            if len(student_assignments) > 0:
                combined_student_assignment_exam = combine_student_assignments_exam(
                    student_assignments, exam
                )

                exam_name = exam["Assignment Name"].values[0]
                # Set explicit order for bar chart
                # We want it to be HW1, HW2, ..., HWx, HW Mean, Exam
                x_axis_order = [
                    col
                    for col in combined_student_assignment_exam[
                        "Assignment Name"
                    ].values
                    if col not in ["Assignment Mean", exam_name]
                ] + ["Assignment Mean", exam_name]
                bars = px.bar(
                    combined_student_assignment_exam,
                    x="Assignment Name",
                    y="Grade/20",
                    range_y=(0, 20),
                    category_orders={"Assignment Name": x_axis_order},
                )
                st.plotly_chart(bars)
