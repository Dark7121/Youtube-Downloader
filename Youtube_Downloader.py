from pytube import Playlist, YouTube
from clint.textui import progress
import requests
import os

def download_video(video, output_path):
    try:
        stream = video.streams.get_highest_resolution()
        video_title = video.title
        filename = f"{video_title}.mp4"
        filepath = os.path.join(output_path, filename)
        response = requests.get(stream.url, stream=True)
        total_length = int(response.headers.get('content-length'))
        with open(filepath, 'wb') as f:
            for chunk in progress.bar(response.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded: {video_title}")
    except Exception as e:
        print(f"Error downloading {video.title}: {e}")

def download_playlist(url):
    video_type = "playlist" if "playlist" in url else "video"
    if video_type == "playlist":
        playlist = Playlist(url)
        for video in playlist.videos:
            download_video(video, output_path)
    elif video_type == "video":
        yt = YouTube(url)
        download_video(yt, output_path)
    else:
        print("Error: Invalid video type")

if __name__ == "__main__":
    video_type = input("Type 'video' for downloading a single YouTube video or 'playlist' for downloading a YouTube playlist: ").lower()
    playlist_url = input("Enter the URL of the YouTube video/playlist: ")
    output_path = input("Enter the output directory path: ")
    download_playlist(playlist_url)
