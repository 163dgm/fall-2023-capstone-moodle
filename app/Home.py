import streamlit as st
from st_pages import Page, Section, show_pages, add_indentation

st.title("Moodle Companion")

add_indentation()

show_pages(
    [
        Page("app/Home.py", "Home"),
        Section("Student Performance", "📈"),
        Page("app/pages/performance/submission_patterns.py", "Submission Patterns"),
        Page("app/pages/performance/location.py", "Submission Location"),
        Page("app/pages/performance/time_of_day.py", "Time of Day"),
        Page("app/pages/performance/exams.py", "Exam Performance"),
        Section("Cheating", "🤥"),
        Page("app/pages/cheating/cheating.py", "Term Cheating"),
        Page("app/pages/cheating/collaboration.py", "Assignment Collaboration"),
    ]
)
