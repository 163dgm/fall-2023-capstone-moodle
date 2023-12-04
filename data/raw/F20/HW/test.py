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


def rename_columns(df: pd.DataFrame):
    return df.rename(columns=COLUMN_RENAME_MAP)


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


def clean_assignment_csv(df: pd.DataFrame):
    df = df.drop(df[df["State"] != "Finished"].index)

    # Convert string time taken to minutes
    df["Time taken"] = df["Time taken"].apply(str_time_to_minutes)
    df["Started on"] = pd.to_datetime(df["Started on"], format="%d %B %Y %I:%M %p")
    df["Completed"] = pd.to_datetime(df["Completed"], format="%d %B %Y %I:%M %p")
    df["ID number"] = df["ID number"].astype("int")
    df["Grade/20.00"] = df["Grade/20.00"].astype("float")

    df = rename_columns(df)
    df = df[
        [
            "Surname",
            "First Name",
            "Student ID",
            "Email Address",
            "Status",
            "Start Time",
            "Complete Time",
            "Time Taken",
            "Grade/20",
        ]
    ]

    return df


def clean_deadlines_csv(df: pd.DataFrame):
    df["Assignment"] = df["Quizz type"] + " " + df["Quiz number"].astype(str)
    df["Open Datetime"] = pd.to_datetime(
        df["Open date"] + " " + df["Open time"],
    )
    df["Close Datetime"] = pd.to_datetime(df["Close date"] + " " + df["Close time"])
    df.drop(
        [
            "Quizz type",
            "Quiz number",
            "Open date",
            "Open time",
            "Close date",
            "Close time",
        ],
        axis=1,
        inplace=True,
    )

    return df


# i want for each assignment to get the deadline close_date from my already created deadlines
# dataframe called deadlines.  then, i want to check for each student in HW01.csv the time
# they started the homework. then, i want to find the difference between when the assignment
# opened and the time the student started the assignement. i want to then cross check this
# difference with the early, middle, and late windows, effectively marking each student as early,
#  middle, or late


def mark_submission_status(
    assignment: pd.DataFrame, deadlines: pd.DataFrame
) -> (
    pd.DataFrame
):  # assignment is HW01 dataset, deadlines is test.csv (the deadlines dataset)
    marked_assignments = pd.DataFrame(
        columns=[
            "Student ID",
            "Assignment Name",
            "Submission Status",
            "Deadline Close Date",
        ]
    )

    # in deadlines, find close datetime
    for _, row in deadlines.iterrows():
        assignment_type = row["Assignment"]
        deadline_close_date = row["Close Datetime"]

        # in HW01 dataset, find "Start Time"

        for _, student_submission in assignment.iterrows():
            student_id = student_submission["Student ID"]  # keep track of ID

            student_start_time = pd.to_datetime(
                student_submission["Start Time"].to_pydatetime()
            )

            # Calculate the difference between assignment open time and student start time
            time_difference = (
                student_start_time - row["Open Datetime"].to_pydatetime()
            ).total_seconds()

            # Mark students based on time difference
            if time_difference >= row["early_window"][1]:
                status = "Late"  # i know this part looks wrong, but i tested a lot and its right
            elif row["middle_window"][1] <= time_difference < row["middle_window"][0]:
                status = "Middle"
            else:
                status = "Early"  # same here, naming is confusing but this correctly labels status of students

            # Append the marked assignment to the result DataFrame
            marked_assignments = pd.concat(
                [
                    marked_assignments,
                    pd.DataFrame(
                        [[student_id, assignment_type, status, deadline_close_date]],
                        columns=[
                            "Student ID",
                            "Assignment Name",
                            "Submission Status",
                            "Deadline Close Date",
                        ],
                    ),
                ],
                ignore_index=True,
            )

    return marked_assignments


def find_time_window(deadlines: pd.DataFrame) -> pd.DataFrame:
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
        lambda row: f"{int(row['hours']):02d}:{row['minutes']:02d}:{row['seconds']:02d}",
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
    return deadlines[["early_window", "middle_window", "late_window"]]


# assignment = pd.read_csv("../../../analysis/merged_df_F20_hw.csv")
assignment = pd.read_csv("HW01.csv")

assignment = clean_assignment_csv(assignment)

# deadlines = pd.read_excel("../../Moodle Datasets.xlsx")
deadlines = pd.read_csv("test.csv")
deadlines = clean_deadlines_csv(deadlines)
windows = find_time_window(deadlines)
marked_assignments = mark_submission_status(assignment, deadlines)

# sprint(marked_assignments)
