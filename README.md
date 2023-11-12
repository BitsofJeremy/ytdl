# YouTube Subscription Downloader

Using YouTube RSS feeds, and YT-DLP to download channel videos

### TODO

- Add Flask frontend for administration
- Refactor video filtering completely [Started]
  - Add some sort of simple regex?
- Fix datetime things [remove Arrow dependency]
- Move to 2 directory structure [one for downloading, one for JellyFin] **DONE**
  - Move files from download directory to JellyFin library, on finish **DONE**
- Trigger JellyFin Library refresh on finish  **DONE**
- Build MVP, possible simple Flask frontend for watching ??

### Install

 - Clone the repo
 - Create a virtualenv
 - Activate the virtualenv
 - Install the requirements for your system
 - Edit the config section to your liking [DL_DIR, TTD, OPML_FILE]
 - Create the database
 
   ```python dbconfig.py```

 - Import your subscription CSV into the DB [Google Export]
   - Update the config.py CSV_FILE to point to your CSV from Google

      ```python import_csv_to_db.py```

 - [If old OPML file] Import the channels into the DB

   ```python import_opml_to_db.py```

 - Run it

   ```sh run_yt_dl.sh```


#### BONUS FILE: Music/Audio Only Downloading

   ```python music_dl.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"```


https://github.com/yt-dlp/yt-dlp#format-selection-examples


      import yt_dlp

      URLS = ['https://www.youtube.com/watch?v=BaW_jenozKc']

      ydl_opts = {
          'format': 'm4a/bestaudio/best',
          # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
          'postprocessors': [{  # Extract audio using ffmpeg
              'key': 'FFmpegExtractAudio',
              'preferredcodec': 'm4a',
          }]
      }

      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
          error_code = ydl.download(URLS)



### For JellyFin Users

# Jellyfin Youtube Metadata Plugin
  - This plugin enables JellyFin to 'see' and parse the downloaded videos so that they show up nicely with thumbnails and metadata.
    - https://github.com/ankenyr/jellyfin-youtube-metadata-plugin
    



