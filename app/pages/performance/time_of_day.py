import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

# from datetime import datetime
from st_pages import add_indentation
from utils import clean_assignment_csv

# import plotly.express as px
import pandas as pd
import plotly.express as px
# import matplotlib.pyplot as plt


def read_assignment(csv: UploadedFile):
    assignments = pd.read_csv(csv)
    assignments = clean_assignment_csv(assignments)
    # print(assignments)
    return assignments


def time_of_day_grade(csv):  # time of day assignment is submitted, corresponding grade
    # group by time of day they do it, assume time of day they do it is submission time
    # 4 groups: morning (6am-12pm), afternoon (12:01pm-5pm),
    # evening (5:01pm-8pm), night (8:01pm-5:59am)
    # take average of each group, bar chart
    # y-axis: grade/20, x-axis: group
    # DICT: KEY IS TIME, VALUE IS PERFORMANCE

    # Define time ranges
    morning_range = pd.to_datetime(["06:00:00", "12:00:00"]).time
    afternoon_range = pd.to_datetime(["12:01:00", "17:00:00"]).time
    evening_range = pd.to_datetime(["17:01:00", "20:00:00"]).time
    night_range = pd.to_datetime(["20:01:00", "23:59:59"]).time

    df = read_assignment(csv)
    date_string = df["Complete Time"]
    date_format = "%d %B %Y %I:%M %p"  # converting date
    parsed_date = pd.to_datetime(date_string, format=date_format)
    time = parsed_date.dt.time

    # Initialize dictionaries to store grades for each time of day
    morning = dict()
    afternoon = dict()
    evening = dict()
    night = dict()

    # Loop through each row in the dataframe
    for index, row in df.iterrows():
        grade = row["Grade/20"]

        # Determine the time of day and add the grade to the corresponding dictionary
        if morning_range[0] <= time[index] <= morning_range[1]:
            morning[index] = grade
        elif afternoon_range[0] <= time[index] <= afternoon_range[1]:
            afternoon[index] = grade
        elif evening_range[0] <= time[index] <= evening_range[1]:
            evening[index] = grade
        elif night_range[0] <= time[index] <= night_range[1]:
            night[index] = grade

    # Calculate average grade for each time of day
    avg_morning = sum(morning.values()) / len(morning) if morning else 0
    avg_afternoon = sum(afternoon.values()) / len(afternoon) if afternoon else 0
    avg_evening = sum(evening.values()) / len(evening) if evening else 0
    avg_night = sum(night.values()) / len(night) if night else 0
    times_of_day = ["Morning", "Afternoon", "Evening", "Night"]
    average_grades = [avg_morning, avg_afternoon, avg_evening, avg_night]

    new_df = pd.DataFrame(
        zip(times_of_day, average_grades), columns=["Time of Day", "Average Grade"]
    )

    return new_df


add_indentation()
st.title("Time of Day and Performance per Assignment")
st.subheader("Visualize When Students Complete Assignments")
st.caption(
    "See if students' performance is affected by the time of day at which they complete their assignments. Students are categorized into four groups according to when they do their assignments. These groups are 'Morning', 'Afteroon', 'Evening', and 'Night', which are defined as 6am-12pm, 12pm-5pm, 5pm-8pm, and 8pm-5am, respectively."
)
csv = st.file_uploader("Choose a file", type="csv", accept_multiple_files=False)
if csv is not None:
    df = time_of_day_grade(csv)
    st.markdown("### Average Grade vs. Time of Day")
    bar_chart = px.bar(
        df,
        x="Time of Day",
        y="Average Grade",
        category_orders={"Time of Day": ["Morning", "Afternoon", "Evening", "Night"]},
        range_y=(0, 23),
    )
    st.plotly_chart(bar_chart)
