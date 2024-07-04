import streamlit as st
import json
import os

# Load saved content from file
def load_content():
    if not os.path.exists('data/saved_content.json'):
        return {}
    with open('data/saved_content.json', 'r') as f:
        return json.load(f)

st.title("Summarized Content")
# Selector for Content
view_option = st.radio("Choose content type to view:", ("Podcasts", "YouTube Videos", "Seroter"))

if view_option == "Podcasts":
    st.header("Podcast Content")
    for entry in load_content():
        st.write(entry)
elif view_option == "YouTube Videos":
    st.header("Youtube Content")
elif view_option == "Seroter":
    st.header("Seroter Links")