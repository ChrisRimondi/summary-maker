import yt_dlp as youtube_dl
import hashlib
from transcribe import transcribe_audio_locally


def get_recent_videos_from_channel(channel_url, max_videos=5):
    # Options to extract video URLs from a channel
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,
        'dump_single_json': True,
    }
    
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(channel_url, download=False)
            #print(json.dumps(info, indent=4))  # Print the entire info structure for debugging
        
        video_urls = []
        if 'entries' in info:
            for entry in info['entries']:
                if len(video_urls) >= max_videos:
                    break
                # Check if entry is a video
                if 'id' in entry and entry.get('ie_key') == 'Youtube' and entry.get('_type') != 'playlist':
                    video_urls.append({'link':f"https://www.youtube.com/watch?v={entry['id']}", 'title': entry['title']})
                    #print(entry['title'])
                else:
                    print(f"Non-video entry skipped: {entry}")
        else:
            print(f"No entries found in channel info: {info}")
        return video_urls
    except Exception as e:
        print(f"Error extracting videos from channel: {e}")
        return []

def download_audio(video_url):
    # Define the options to download the audio in .wav format
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': "data/yt_audio/" + hashlib.sha256(video_url.encode()).hexdigest()[:6]
    }
    
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            print(f"Audio downloaded for video: {video_url}")
            return True
    except Exception as e:
        print(f"Failed to download audio for video: {video_url} ({e})")
        return False

def main(channel_url):
    # Get the 10 most recent videos from the channel
    video_urls = get_recent_videos_from_channel(channel_url, max_videos=10)
    
    if not video_urls:
        print("No videos found or error extracting videos from channel.")
        return

    # Try downloading audio for the first available video
    for video_url in video_urls:
        if download_audio(video_url):
            break  # Stop after successfully downloading the first available video

# Generate a transcript
def yt_generate_transcript(url):
    # Implement transcription logic here
    download_audio(url)
    wav_path = "data/yt_audio/" + hashlib.sha256(url.encode()).hexdigest()[:6] + ".wav"
    return transcribe_audio_locally(wav_path).strip()

if __name__ == "__main__":
    channel_url = 'https://www.youtube.com/@KARATEbyJesse/videos'
    #channel_url = 'https://www.youtube.com/@fightscience'
    main(channel_url)
