import requests
from st_pages import add_indentation
import streamlit as st
import pandas as pd
from streamlit.runtime.uploaded_file_manager import UploadedFile
from utils import chunk_list
import plotly.express as px


def get_batch_coords(ips: list[str]):
    def get_query_dict(ip):
        return {"query": ip, "fields": "lat,lon"}

    body = list(map(lambda x: get_query_dict(x), ips))

    coords = pd.DataFrame()
    for chunk in list(chunk_list(body, 99)):
        response = requests.post(st.secrets["IP_API_URL"], json=chunk)

        if response.status_code == 200:
            data = response.json()
            coords = pd.concat([coords, pd.DataFrame(data)], ignore_index=True)
        else:
            print("Error:", response.status_code, response.text)

    return coords


def geolocate_assignment_submissions(csv: UploadedFile):
    in_df = pd.read_csv(csv)

    df = in_df.loc[in_df["Event name"] == "Quiz attempt submitted"]
    df = df.drop_duplicates("IP address")
    df = df.dropna(subset="IP address").reset_index()

    coords = get_batch_coords(df["IP address"].to_list())
    df = df.join(coords, how="outer")

    return df.dropna(subset=["lat", "lon"])


add_indentation()
st.title("Assignment Submission Locations")
st.subheader("Visualize Where Students Submit Assignments")
st.caption(
    "Time zone difference can have an effect on students and their performance. If a student performed unusually on an assignment, use the map to find if a time difference could be affecting their performance."
)


csv = st.file_uploader(
    "Upload a Moodle log CSV", type="csv", accept_multiple_files=False
)
if csv is not None:
    locations = geolocate_assignment_submissions(csv)

    px.set_mapbox_access_token(st.secrets["MAPBOX_TOKEN"])
    map = px.scatter_mapbox(
        locations,
        lat="lat",
        lon="lon",
        hover_name="User full name",
        zoom=10,
        color_discrete_sequence=px.colors.qualitative.Dark2,
    )
    map.update_traces(cluster=dict(enabled=True))
    st.plotly_chart(map)
