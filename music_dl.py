#!/bin/env python
# Requires: yt_dlp module
# Requires: ffmpeg
# Usage:
#
# python music_dl.py <URL>, ...
# 
# Example:
# 
# For ZSH on MacOS you need the quotes around the URL!
#
# python music_dl.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

import json
import sys
from yt_dlp import YoutubeDL

ydl_opts = {
    'format': 'm4a/bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
        # 'preferredquality': '192',
    }],
}

if __name__ == "__main__":
    with YoutubeDL(ydl_opts) as ydl:
        URL = sys.argv[1:]
        ydl.download(URL)
