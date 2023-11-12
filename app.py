
# TODO Update dates to use the datetime module instead of arrow
import shutil

import arrow
import logging
import os
import config
from utils import *

# ######## LOGGING ########
LOG_FILENAME = 'main.log'
logger = logging.getLogger(LOG_FILENAME)
logger.setLevel(logging.INFO)
# Create file handler which logs event error messages
fh = logging.FileHandler(LOG_FILENAME)
fh.setLevel(logging.INFO)
# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# Add rotation based on size and 5 log files
log_rotation = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=5242880, backupCount=5)
# Add the handlers to logger
logger.addHandler(fh)
logger.addHandler(log_rotation)


def main():
    # Get today's date
    today = get_date()
    # Get all channels
    channels = get_channels()
    # Loop through all channels to get their video data for today
    for channel in channels:
        logging.info(f'getting {channel} videos')
        channel_name = channel['channel_name']
        channel_url = channel['url']
        # Get all videos for today
        got_em = get_videos_details(
            url=channel_url,
            channel_name=channel_name,
            today=today
        )
        if got_em:
            logging.info(f"{channel_name} FINISHED")
        else:
            logging.info("Something went wrong in parsing the feed")
            logging.info(f"{channel_name}")

    # #### Get the Videos ####
    # All videos for today are in the DB, download the videos, and the mark them downloaded
    today_videos = get_today_videos(today)
    for video in today_videos:
        # Check for videos we already downloaded today.
        if video['downloaded']:
            logging.info(f"{video['id']} ALREADY DOWNLOADED, SKIPPING")
        else:
            downloaded = download_video(
                download_dir=config.DL_DIR,
                channel_name=video['channel_name'],
                url=video['video_url']
            )
            if downloaded:
                # Update DB vide has been downloaded
                updated = update_video(_id=video['id'], downloaded=True)
                if updated:
                    if config.JELLY_ENABLED:
                        # JellyFin is enabled so move the file
                        # Find the video, returns a list
                        video_file = find_video_file(
                            video_id=video['video_id'],
                            path=f"{config.DL_DIR}/{video['channel_name']}/"
                        )
                        print(video_file)
                        destination = f"{config.JELLY_DIR}/{video['channel_name']}/"
                        # Make destination if not there
                        os.makedirs(destination, exist_ok=True)
                        shutil.move(src=video_file[0], dst=destination)
                        updated = update_video(_id=video['id'], moved=True)
                        if updated:
                            logging.info(f"VIDEO {video['id']} ENTRY UPDATED [moved]")
                        else:
                            logging.info("Something Failed in the Database, DOH!")
                    logging.info(f"VIDEO {video['id']} ENTRY UPDATED [downloaded]")
                else:
                    logging.info("Something Failed in the Database, DOH!")
            else:
                logging.info("DOWNLOAD FAILED")

    # #### Clean Up ####
    # Videos downloaded, time to clean up old videos, and mark them removed
    # Remove videos determined by TTD variable
    # Initialize Arrow for today
    a = arrow.get(today)
    # Shift back according to TTD [default: 7 days]
    lw = a.shift(days=config.TTD)
    # Format for search
    last_week = lw.format('YYYY-MM-DD')
    # Get a list of old videos
    old_videos = get_old_videos(last_week)
    if len(old_videos) >= 1:
        # We have videos to delete
        for video in old_videos:
            # TODO Verify this works, might be broken
            logging.info(video)
            if video['moved']:
                # Video was moved to JellyFin directory
                # Find the video
                x = find_video_file(
                    video_id=video['video_id'],
                    path=config.JELLY_DIR
                )
            else:
                # Video was not moved
                # Find the video
                x = find_video_file(
                    video_id=video['video_id'],
                    path=config.DL_DIR
                )
            # Remove the video
            try:
                os.remove(x[0])
                # Update DB
                updated = update_video(_id=video['id'], removed=True)
                if updated:
                    logging.info(f"VIDEO {video['id']} ENTRY UPDATED")
                else:
                    logging.info("Something Failed in the Database, DOH!")
            except FileNotFoundError:
                logging.info(f"{video['id']} - {video['video_title']} NOT FOUND")
    else:
        logging.info(f'No videos for {last_week} to remove.')

    if config.JELLY_ENABLED:
        refreshed = refresh_jellyfin_library(
            server_ip=config.JELLY_IP,
            api_key=config.JELLY_API_KEY
        )
        if refreshed:
            logging.info('Library Updated')
    # Done with this run
    return logging.info('Finished')


if __name__ == '__main__':
    main()
