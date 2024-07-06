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
new_podcast_url = st.text_input("Add new podcast feed URL")
new_podcast_name = st.text_input("Add short name for podcast feed")
if st.button("Add Podcast Feed"):
    if new_podcast_url and new_podcast_name:
        feeds["podcasts"].append({"url": new_podcast_url, "short_name": new_podcast_name})
        save_feeds(feeds)
        st.success("Podcast feed added")
    else:
        st.error("Both URL and short name are required")

st.subheader("Current Podcast Feeds")
for podcast in feeds["podcasts"]:
    st.write(f"{podcast['short_name']}: {podcast['url']}")

# YouTube channels management
st.header("Manage YouTube Channels")
new_channel_url = st.text_input("Add new YouTube channel URL")
new_channel_name = st.text_input("Add short name for YouTube channel")
if st.button("Add YouTube Channel"):
    if new_channel_url and new_channel_name:
        feeds["youtube_channels"].append({"url": new_channel_url, "short_name": new_channel_name})
        save_feeds(feeds)
        st.success("YouTube channel added")
    else:
        st.error("Both URL and short name are required")

st.subheader("Current YouTube Channels")
for channel in feeds["youtube_channels"]:
    st.write(f"{channel['short_name']}: {channel['url']}")
