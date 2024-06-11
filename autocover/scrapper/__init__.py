from pytube import YouTube
import moviepy.editor as mp

AUDIO_DOWNLOAD_DIR = "../isolator/downloaded_audio"


def YoutubeAudioDownload(video_url):
    try:
        # Download the video in its original format
        video = YouTube(video_url)
        audio_stream = video.streams.filter(only_audio=True).first()
        audio_stream.download(AUDIO_DOWNLOAD_DIR, filename="temp_audio.mp4")

        # Convert the downloaded video to MP3
        video_path = f"{AUDIO_DOWNLOAD_DIR}/temp_audio.mp4"
        mp.AudioFileClip(video_path).write_audiofile(f"{AUDIO_DOWNLOAD_DIR}/audio2.mp3")

        # Clean up temporary files
        mp.os.remove(video_path)

        print("Audio was downloaded and converted to MP3 successfully.")
    except Exception as e:
        print("Failed to download and convert audio:", str(e))

# Example usage
YoutubeAudioDownload("https://www.youtube.com/watch?v=Q7IVjcgfYRg")
