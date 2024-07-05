import feedparser
import requests
import subprocess
from typing import List, Tuple

def fetch_feed_episodes(feed_url: str, num_episodes: int) -> List[Tuple[str, str, str, str]]:
    feed = feedparser.parse(feed_url)
    episodes = [(entry.title, entry.link, entry.published, entry.enclosures[0]['href']) for entry in feed.entries]
    return list(filter(lambda x: x is not None, episodes))[:num_episodes]

def download_episode(mp3_url: str, output_path: str) -> None:
    print("Downloading episode link:" + mp3_url)
    response = requests.get(mp3_url)
    with open(output_path, 'wb') as file:
        file.write(response.content)

def convert_mp3_to_wav(mp3_filename: str, wav_filename: str) -> bool:
    command = [
        'ffmpeg',
        '-i', mp3_filename,
        wav_filename
    ]
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting {mp3_filename} to WAV: {e}")
        return False
    
    return True