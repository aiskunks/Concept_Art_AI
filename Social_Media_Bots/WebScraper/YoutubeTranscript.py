import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
# Replace with your own API key
API_KEY = "xxxxxxxxxxxxxxxxxxxxxxx"
# Replace with the name of the YouTube channel
CHANNEL_NAME = "Python Programmer"
# Initialize the YouTube API client
# youtube = build('youtube', 'v3', developerKey=API_KEY)
flow = InstalledAppFlow.from_client_secrets_file("E:\Projects\TransferPlaylist\server\client_secret.json", scopes=["https://www.googleapis.com/auth/youtube.force-ssl"])
credentials = flow.run_local_server(port=6150, prompt='consent')

youtube = build('youtube', 'v3', credentials=credentials)

# Get the channel ID by channel name
def get_channel_id(channel_name):
  response = youtube.search().list(
    q=channel_name,
    type='channel',
    part='id'
  ).execute()
  return response['items'][0]['id']['channelId']
# Get all video IDs from a channel
def get_video_ids(channel_id):
  video_ids = []
  next_page_token = None
  while True:
    response = youtube.search().list(
      channelId=channel_id,
      type='video',
      part='id',
      maxResults=50,
      pageToken=next_page_token
    ).execute()
    for item in response['items']:
      video_ids.append(item['id']['videoId'])
    next_page_token = response.get('nextPageToken')
    if not next_page_token:
      break
  return video_ids
# Get the transcript for a video

def get_video_transcript(video_id):
  captions_response = youtube.captions().list(part="id, snippet",videoId = video_id).execute()

  # Find the auto-generated caption track
  auto_generated_caption_track = next((item for item in captions_response.get('items', []) if item['snippet']['trackKind'] == 'ASR'),None)

  if auto_generated_caption_track:
    auto_generated_caption_track_id = auto_generated_caption_track['id']

    # Download the auto-generated caption track
    caption_response = youtube.captions().download(
        id=auto_generated_caption_track_id,
        tfmt='srt'  # You can choose a different format if needed
    ).execute()

    # Save the captions to a file
    transcript = caption_response.decode('utf-8')
    return transcript
  else:
    print('Auto-generated captions not found for the specified video.')
  
# Create a directory to save transcripts
if not os.path.exists(CHANNEL_NAME):
  os.makedirs(CHANNEL_NAME)
# Get the channel ID
channel_id = get_channel_id(CHANNEL_NAME)
# Get the video IDs from the channel
video_ids = get_video_ids(channel_id)
# Download transcripts for each video
for video_id in video_ids:
  transcript = get_video_transcript(video_id)
  if transcript:
    with open(f"{CHANNEL_NAME}/{video_id}.srt", "w", encoding="utf-8") as file:
      file.write(transcript)
print(f"Transcripts downloaded for {len(video_ids)} videos.")
