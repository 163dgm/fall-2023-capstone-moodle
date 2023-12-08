import streamlit as st
from st_pages import Page, Section, show_pages, add_indentation

# Set page title
st.title("A Behavior Analysis of Online Assignment Submission Patterns")

# Add indentation for a cleaner look
add_indentation()

# Define the structure of your app
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

# Add a brief introduction to the homepage
st.write(
    """
    Welcome to our web application that analyzes online assignment submission patterns using Moodle datasets. 
    Explore different sections to gain insights into student performance, submission patterns, and potential cheating or collaboration.
    """
)

# Add any additional content or information you want on the homepage
st.write(
    """
    ## Key Features
    - Analyze submission patterns to understand student behavior.
    - Explore performance metrics to identify areas for improvement.
    - Detect potential cheating and collaboration among students.

    ## How to Use
    Navigate through the sections using the sidebar to explore various aspects of the analysis.

    Enjoy exploring the insights from our investigation!
    """
)
