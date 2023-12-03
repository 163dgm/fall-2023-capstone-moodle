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

    return df


def mark_submission_status(assignments, deadlines):
    marked_assignments = pd.DataFrame()

    for index, row in deadlines.iterrows():
        assignment_name = row["Quizz type"]
        # assignment_close_time = row["close_datetime"]

        # Filter assignments for the specific assignment
        assignment_submissions = assignments[
            assignments["Quizz type"] == assignment_name
        ]

        for _, student_submission in assignment_submissions.iterrows():
            student_id = student_submission["ID Number"]
            student_start_time = student_submission["Started on"]
            date_format = "%d %B %Y %I:%M %p"  # converting date
            parsed_date = pd.to_datetime(student_start_time, format=date_format)
            student_start_time = parsed_date.dt.time
            print(student_start_time)

            # Calculate the difference between assignment open time and student start time
            time_difference = (
                student_start_time - row["open_datetime"]
            ).total_seconds()

            # Mark students based on time difference
            if time_difference >= row["early_window"][1]:
                status = "Early"
            elif row["middle_window"][1] <= time_difference < row["middle_window"][0]:
                status = "Middle"
            else:
                status = "Late"

            # Append the marked assignment to the result DataFrame
            marked_assignments = marked_assignments.append(
                {
                    "Student ID": student_id,
                    "Assignment Name": assignment_name,
                    "Submission Status": status,
                },
                ignore_index=True,
            )

    return marked_assignments


df = pd.read_csv("HW01.csv")
df = clean_assignment_csv(df)

deadlines = pd.read_csv("test.csv")
deadlines["open_datetime"] = pd.to_datetime(
    deadlines["Open date"] + " " + deadlines["Open time"]
)
deadlines["close_datetime"] = pd.to_datetime(
    deadlines["Close date"] + " " + deadlines["Close time"]
)

# Calculate the time window for each assignment
deadlines["time_window"] = deadlines.apply(
    lambda row: row["close_datetime"] - row["open_datetime"], axis=1
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
print(deadlines["total_seconds"])

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

# print(deadlines[["early_window", "middle_window", "late_window"]])
