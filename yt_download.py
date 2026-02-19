"""
- script for downloading YouTube videos containing guitar tabs (for YOLO model training!)
- downloads the video to directory YT_DOWNLOADS
- python frames_collection.py --yt_link {paste youtube link here}
"""

import argparse
import yt_dlp
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--yt_link", type=str, default="")

DOWNLOAD_DIRECTORY = Path("YT_DOWNLOADS")
DOWNLOAD_DIRECTORY.mkdir(exist_ok=True, parents=True)

if __name__ == "__main__":
    args = parser.parse_args()

    if len(args.yt_link) > 0:
        link = args.yt_link
        ydl_options = {
            "format": "bv*[ext=mp4][height<=1080]", 
            "outtmpl": str(DOWNLOAD_DIRECTORY / "%(id)s.%(ext)s"),
        }

        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            ydl.download([link])
