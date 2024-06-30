import os
import csv
from datetime import datetime
from googleapiclient.discovery import build

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_IDS = ["UCpWaR3gNAQGsX48cIlQC0qw", "UCYnvxJ-PKiGXo_tYXpWAC-w"]
LOCAL_STORAGE_PATH = "/app/local_storage"
DEBUG_LOG_FILE = "/app/local_storage/debug.log"

def log_debug_message(message):
    with open(DEBUG_LOG_FILE, 'a') as f:
        f.write(f"{datetime.now()}: {message}\n")

def get_youtube_data():
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    data = []
    for channel_id in CHANNEL_IDS:
        channel_request = youtube.channels().list(part="snippet,statistics", id=channel_id)
        channel_response = channel_request.execute()
        channel_data = channel_response['items'][0]
        
        # Get the latest video from the channel
        search_request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            type="video",
            order="date",
            maxResults=1
        )
        search_response = search_request.execute()
        
        if search_response['items']:
            video_id = search_response['items'][0]['id']['videoId']
            video_request = youtube.videos().list(part="statistics,snippet", id=video_id)
            video_response = video_request.execute()
            video_data = video_response['items'][0]
            
            data.append({
                'channel_id': channel_id,
                'channel_title': channel_data['snippet']['title'],
                'channel_description': channel_data['snippet']['description'],
                'subscriber_count': channel_data['statistics']['subscriberCount'],
                'video_count': channel_data['statistics']['videoCount'],
                'video_title': video_data['snippet']['title'],
                'video_description': video_data['snippet']['description'],
                'view_count': video_data['statistics']['viewCount'],
                'likes_count': video_data['statistics'].get('likeCount', 0),
                'comments_count': video_data['statistics'].get('commentCount', 0),
                'publication_date': video_data['snippet']['publishedAt']
            })
    return data

def save_to_csv(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{LOCAL_STORAGE_PATH}/youtube_data_{timestamp}.csv"
    
    fieldnames = [
        'channel_id', 'channel_title', 'channel_description',
        'subscriber_count', 'video_count', 'video_title', 
        'video_description', 'view_count', 'likes_count', 
        'comments_count', 'publication_date'
    ]
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            log_debug_message(f"Processing item: {item}")
            filtered_item = {key: item.get(key, '') for key in fieldnames}
            writer.writerow(filtered_item)
    log_debug_message(f"Data saved to {filename}")

def run_retrieval_job():
    data = get_youtube_data()
    log_debug_message(f"Data retrieved: {data}")
    save_to_csv(data)

if __name__ == "__main__":
    run_retrieval_job()
