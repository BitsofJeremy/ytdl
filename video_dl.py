#!/bin/env python
# Requires: yt_dlp module
# Requires: ffmpeg
# Usage:
#
# python video_dl.py <URL>, ...
#
# Example:
#
# For ZSH on MacOS you need the quotes around the URL!
#
# python video_dl.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

import json
import sys
from yt_dlp import YoutubeDL


ydl_opts = {
    # New File output:
    # Example Output: <video_title>-[<video_id>].mp4
    'outtmpl': '%(title)s-[%(id)s].%(ext)s',
    # Download the best mp4 video available, or the best video if no mp4 available
    # 'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b',
    'format': '(bv*[vcodec~="^((he|a)vc|h26[45])"]+ba) / (bv*+ba/b)',
    # No color in terminal
    'no_color': True,
    # Send to ffmpeg for MP4
    'postprocessors': [
        {'key': 'FFmpegMetadata'},
    ],
    # Number of retries
    'retries': 2,
}


if __name__ == "__main__":
    with YoutubeDL(ydl_opts) as ydl:
        URL = sys.argv[1:]
        ydl.download(URL)
