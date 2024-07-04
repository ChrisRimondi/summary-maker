import streamlit as st
import json
import os

# Load feeds from file
def load_feeds():
    if not os.path.exists('data/feeds.json'):
        return {"podcasts": [], "youtube_channels": []}
    with open('data/feeds.json', 'r') as f:
        return json.load(f)

# Save feeds to file
def save_feeds(feeds):
    with open('data/feeds.json', 'w') as f:
        json.dump(feeds, f)

feeds = load_feeds()

st.title("Configuration")

# Podcast feeds management
st.header("Manage Podcast Feeds")
new_podcast = st.text_input("Add new podcast feed URL")
if st.button("Add Podcast Feed"):
    feeds["podcasts"].append(new_podcast)
    save_feeds(feeds)
    st.success("Podcast feed added")

st.subheader("Current Podcast Feeds")
for podcast in feeds["podcasts"]:
    st.write(podcast)

# YouTube channels management
st.header("Manage YouTube Channels")
new_channel = st.text_input("Add new YouTube channel URL")
if st.button("Add YouTube Channel"):
    feeds["youtube_channels"].append(new_channel)
    save_feeds(feeds)
    st.success("YouTube channel added")

st.subheader("Current YouTube Channels")
for channel in feeds["youtube_channels"]:
    st.write(channel)
