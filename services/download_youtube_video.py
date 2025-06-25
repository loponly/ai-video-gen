import os
from yt_dlp import YoutubeDL
from moviepy import VideoFileClip


def download_youtube_video(url: str, save_dir: str = "./downloads", cookie_file: str = None) -> str:
    """Robustly downloads the best available version of a YouTube video."""
    os.makedirs(save_dir, exist_ok=True)

    ydl_opts = {
     #   "format": "(bv*[ext=mp4]+ba[ext=m4a])/(bv*+ba/best)/best",
        "outtmpl": os.path.join(save_dir, "%(title)s.%(ext)s"),
    }
    if cookie_file:
        ydl_opts["cookiefile"] = cookie_file

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    return os.path.abspath(ydl.prepare_filename(info))


def convert_webm_to_mp4(input_file: str, output_file: str = None) -> str:
    """
    Converts a .webm video to .mp4 using MoviePy.
    
    :param input_file: Path to the input .webm file.
    :param output_file: Optional path for the output .mp4 file.
    :return: The absolute path of the saved MP4.
    """
    if output_file is None:
        # Default output name if not provided
        name, _ = os.path.splitext(input_file)
        output_file = f"{name}.mp4"

    clip = VideoFileClip(input_file)
    clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

    return os.path.abspath(output_file)


# --- Usage example ---
if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=3B-X3c5c9Sc"
    saved_file = download_youtube_video(url, save_dir="./downloads")
    if saved_file.endswith(".webm"):
        saved_file = convert_webm_to_mp4(saved_file)
    print(f"✅ Done! Video saved at: {saved_file}")
