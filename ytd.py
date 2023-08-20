import os
from pytube import YouTube
from pytube.exceptions import RegexMatchError

def clean_filename(filename):
    # Remove characters that are not allowed in filenames
    forbidden_chars = r'<>:"/\|?*'
    cleaned_filename = "".join(c if c not in forbidden_chars else "_" for c in filename)
    return cleaned_filename

def download_video(url, output_path=".", quality="highest"):
    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Get the selected resolution stream or the highest resolution stream
        if quality == "highest":
            video_stream = yt.streams.get_highest_resolution()
        else:
            video_stream = yt.streams.filter(res=quality).first()

        if not video_stream:
            print("Selected quality is not available. Downloading highest resolution available.")
            video_stream = yt.streams.get_highest_resolution()

        # Get the video title for naming the downloaded file
        video_title = yt.title
        cleaned_title = clean_filename(video_title)

        # Set the output path for the downloaded video
        output_file = os.path.join(output_path, f"{cleaned_title}.mp4")

        # Download the video
        print(f"Downloading '{video_title}' in {video_stream.resolution}...")
        video_stream.download(output_path=output_path, filename=cleaned_title)
        print("Download completed!")

    except RegexMatchError:
        print("Unable to extract video information. Please check the URL.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    download_quality = input("Enter the desired video quality (e.g., 720p, 1080p, highest): ")
    download_video(video_url, quality=download_quality)