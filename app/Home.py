import streamlit as st
from st_pages import Page, Section, show_pages, add_indentation

st.title("Moodle Companion")

add_indentation()

show_pages(
    [
        Page("app/home.py", "Home"),
        Section("Cheating", "🤥"),
        Page("app/pages/cheating/cheating.py", "Term Cheating"),
        Page("app/pages/cheating/collaboration.py", "Assignment Collaboration"),
        Section("Student Performance", "📈"),
        Page("app/pages/performance/location.py", "Submission Location"),
        Page("app/pages/performance/term_performance.py", "Term Performance"),
        Page("app/pages/performance/exams.py", "Exam Performance"),
    ]
)
