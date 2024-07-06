import streamlit as st
import os
from typing import Any, Dict, List
import csv

def read_csv_to_dict(file_path: str) -> List[Dict[str, Any]]:
    """
    Reads a CSV file and returns its contents as a list of dictionaries.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing the rows in the CSV file.
    """
    data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(dict(row))
    return data


st.title("Summarized Content")
# Selector for Content
view_option = st.radio("Choose content type to view:", ("Podcasts", "YouTube Videos", "Seroter"))
content = read_csv_to_dict("data/saved_contet.csv")

if view_option == "Podcasts":
    header = "Podcast Content"
    content_option = "podcast"
elif view_option == "YouTube Videos":
    header = "Youtube Content"
    content_option = "youtube"
elif view_option == "Seroter":
    header = "Seroter Content"
    content_option = "seroter"


for content_record in content:
    if content_record['type'] == content_option:
        file_name = content_record['file_location']
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                summary = file.read()
                st.write(content_record['feed'])
                with st.expander("Show Summary for: " + content_record['title']):
                    st.markdown(summary.replace('\\n', '\n'))
