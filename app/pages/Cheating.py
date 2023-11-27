from io import StringIO
import pandas as pd
import streamlit as st

st.title("Analyze ")

uploaded_file = st.file_uploader(
    "Choose a file", type="csv", accept_multiple_files=True
)
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)
