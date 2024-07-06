import streamlit as st
import json
import os
import feedparser
from yt_utils import get_recent_videos_from_channel, yt_generate_transcript
import hashlib
from transcribe import transcribe_audio_locally
from summarize import summarize_transcription, summarize_article
from utils import download_episode, convert_mp3_to_wav
from rss_utils import get_seroter_daily_entries, expand_entry
from typing import Dict, List, Any
import csv

# Load feeds from file
def load_feeds() -> Dict[str, List[Dict[str, str]]]:
    if not os.path.exists('data/feeds.json'):
        return {"podcasts": [], "youtube_channels": []}
    with open('data/feeds.json', 'r') as f:
        return json.load(f)

# Save feeds to file
def save_feeds(feeds: Dict[str, List[Dict[str, str]]]) -> None:
    with open('data/feeds.json', 'w') as f:
        json.dump(feeds, f)

feeds = load_feeds()

# Refresh podcast feeds
def refresh_podcast(feed_url: str) -> List[feedparser.FeedParserDict]:
    feed = feedparser.parse(feed_url)
    return feed.entries[:10]

# Save summary of content as a dict to a JSON file
def save_content(content_record: Dict[str, Any]) -> None:
    """
    Saves a dictionary to a CSV file, mapping keys to column names.
    If the CSV file already exists, it appends to the next free row.

    Args:
        file_path (str): The path to the CSV file.
        data (Dict[str, Any]): The dictionary to save to the CSV file.
    """
    file_path = "data/saved_content.csv"
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=content_record.keys())
        
        if not file_exists:
            writer.writeheader()  # File does not exist, write the header
        
        writer.writerow(content_record)

# Generate a transcript
def generate_transcript(url: str) -> str:
    # Implement transcription logic here
    episode_id = hashlib.sha256(url.encode()).hexdigest()[:6]
    mp3_path = f"data/podcasts/episode_{episode_id}.mp3"
    wav_path = f"data/podcasts/episode_{episode_id}.wav"
    download_episode(url, mp3_path)
    convert_mp3_to_wav(mp3_path, wav_path)
    return transcribe_audio_locally(wav_path).strip()


st.title("Content Summarizer")


# Selector for viewing Podcasts or YouTube videos
view_option = st.radio("Choose content type to view:", ("Podcasts", "YouTube Videos", "Seroter"))

if view_option == "Podcasts":
    # Podcast dropdown
    podcast_feed = st.selectbox("Select Podcast Feed", options=[f"{podcast['short_name']} ({podcast['url']})" for podcast in feeds["podcasts"]])
    if podcast_feed:
        feed_url = podcast_feed.split(" (")[-1][:-1]  # Extract URL from selected option
        podcast_entries = refresh_podcast(feed_url)
        for entry in podcast_entries:
            st.write(entry.title)
            download_url = entry.enclosures[0]['href']
            file_name = "data/transcriptions/" + hashlib.sha256(download_url.encode()).hexdigest()[:6] + ".txt"
            if os.path.exists(file_name):
                with open(file_name, "r") as file:
                    summary = file.read()
                    with st.expander("Show Summary"):
                        st.markdown(summary.replace('\\n', '\n'))
                
            else: 
                if st.button(f"Summarize Transcript for {entry.title}", key=f"summarize-podcast-{entry.link}"):
                    summary = entry.title + '\n\n' + summarize_transcription(generate_transcript(download_url))
                    summary = summary.replace("ChatCompletionMessage(content='", "")
                    summary = summary.replace("\", role='assistant', function_call=None, tool_calls=None)","")
                    with open(file_name, 'w') as file:
                        file.write(summary.replace('\\n', '\n'))
                    save_content({'type': 'podcast', 'feed': podcast_feed, 'title': entry.title, 'file_location':  file_name})
                    
                
elif view_option == "YouTube Videos":
    # Youtube dropdown
    youtube_channel = st.selectbox("Select YouTube Channel", options=[f"{channel['short_name']} ({channel['url']})" for channel in feeds["youtube_channels"]])
    if youtube_channel:
        channel_url = youtube_channel.split(" (")[-1][:-1]  # Extract URL from selected option
        youtube_entries = get_recent_videos_from_channel(channel_url)
        for entry in youtube_entries:
            download_url = entry['link']
            file_name = "data/yt_audio/" + hashlib.sha256(download_url.encode()).hexdigest()[:6] + ".txt"
            if os.path.exists(file_name):
                with open(file_name, "r") as file:
                    summary = file.read()
                    with st.expander("Show Summary"):
                        st.markdown(summary.replace('\\n', '\n'))
            else: 
                if st.button(f"Summarize Transcript for {entry['title']}", key=f"summarize-yt-{entry['link']}"):
                    summary = entry['title'] + '\n\n' + summarize_transcription(yt_generate_transcript(entry['link']))
                    summary = summary.replace("ChatCompletionMessage(content='", "")
                    summary = summary.replace("\", role='assistant', function_call=None, tool_calls=None)","")
                    with open(file_name, 'w') as file:
                        file.write(summary.replace('\\n', '\n'))
                    save_content({'type': 'youtube', 'feed': youtube_channel, 'title': entry['title'], 'file_location':  file_name})
elif view_option == "Seroter":
    
    # Seroter dropdown
    seroter_daily = st.selectbox("Select Daily Post", options=get_seroter_daily_entries())
    if seroter_daily:
        # Iterate over the output and print each text and href pair
        for item in expand_entry(seroter_daily):
            if st.button(f"Summarize Article for {item['text']}", key=f"summarize-podcast-{item['href']}"):
                summary = item['text'] + '\n\n' + summarize_article(item['href'])
                summary = summary.replace("ChatCompletionMessage(content='", "")
                summary = summary.replace("\", role='assistant', function_call=None, tool_calls=None)","")
                st.markdown(summary)
                file_name = "data/article_summaries/" + hashlib.sha256(item['href'].encode()).hexdigest()[:6] + ".txt"
                with open(file_name, 'w') as file:
                        file.write(summary.replace('\\n', '\n'))
                save_content({'type': 'seroter', 'feed': seroter_daily, 'title': item['text'], 'file_location':  file_name})
