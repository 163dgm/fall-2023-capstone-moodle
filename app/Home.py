import streamlit as st
from st_pages import Page, Section, show_pages, add_indentation

st.title("Moodle Companion")

add_indentation()

show_pages(
    [
        Page("app/home.py", "Home"),
        Section("Cheating"),
        Page("app/pages/cheating/cheating.py", "Term Cheating"),
        Page("app/pages/cheating/collaboration.py", "Assignment Collaboration"),
        Page("app/pages/performance.py", "Performance", in_section=False),
    ]
)
