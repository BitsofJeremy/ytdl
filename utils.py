# TODO Update dates to use the datetime module instead of arrow

import arrow
import feedparser
import fnmatch
import logging
import os
import requests
from yt_dlp import YoutubeDL
from dbconfig import Channels, Session, Videos, VideoFilters
from video_filter import vfilter


# ######## LOGGING ########
LOG_FILENAME = 'util.log'
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


# ##### MISC HELPERS #####
def get_date():
    """ Gets time and returns a string """
    utc = arrow.utcnow()
    local = utc.to('US/Pacific')
    # Get human time
    display_time = local.format('YYYY-MM-DD')
    return display_time


# ##### DATABASE HELPERS #####
"None"


# ##### CHANNEL HELPERS #####


def get_channel(_id):
    """ Returns one channel by ID """
    session = Session()
    channel = session.query(Channels).filter_by(id=_id).one_or_none()
    if channel:
        # Return a json dict from DB
        return channel.serialize
    else:
        # Return a false
        logging.info(f'{_id} NOT FOUND')
        return False


def get_channel_by_name(channel_name):
    """ Returns one channel by channel_name """
    session = Session()
    channel = session.query(Channels).filter_by(channel_name=channel_name).one_or_none()
    if channel:
        # Return a json dict from DB
        return channel.serialize
    else:
        # Return a false
        logging.info(f'{channel_name} NOT FOUND')
        return False


def get_channels():
    """ Returns all channels in DB as list """
    session = Session()
    channels = session.query(Channels).all()
    channel_list = []
    for channel in channels:
        channel_list.append(channel.serialize)
    return channel_list


def add_channel(channel_name, url):
    """ Adds one channel to DB """
    session = Session()
    exists = session.query(Channels).filter_by(channel_name=channel_name).scalar() is not None
    if exists:
        logging.info(f'{channel_name} EXISTS')
        return False
    channel = Channels(channel_name, url)
    session.add(channel)
    session.commit()
    return True


def update_channel(_id, **kwargs):
    """ Updates Channel by ID """
    session = Session()
    exists = session.query(Channels).filter_by(id=_id).scalar() is not None
    if exists:
        channel = session.query(Channels).filter_by(id=_id).first()
        channel.update(**kwargs)
        session.commit()
    else:
        logging.info(f'{_id} NOT FOUND')
        return False
    return True


def delete_channel(_id):
    """ Deletes Channel by ID """
    session = Session()
    exists = session.query(Channels).filter_by(id=_id).scalar() is not None
    if exists:
        session.query(Channels).filter_by(id=_id).delete()
        session.commit()
    else:
        logging.info(f'{_id} NOT FOUND')
        return False
    return True


# ##### VIDEO HELPERS #####

def get_video(_id):
    """ Returns one video by ID """
    session = Session()
    vid = session.query(Videos).filter_by(id=_id).one_or_none()
    if vid:
        # Return a json dict from DB
        return vid.serialize
    else:
        # Return a false
        logging.info(f'{_id} NOT FOUND')
        return False


def get_videos():
    """ Returns all video in DB as list """
    session = Session()
    vids = session.query(Videos).all()
    vid_list = []
    for vid in vids:
        vid_list.append(vid.serialize)
    return vid_list


def get_today_videos(today):
    """ Returns all video in DB as list from var today """
    session = Session()
    vids = session.query(Videos).filter_by(date_published=today)
    vid_list = []
    for vid in vids:
        vid_list.append(vid.serialize)
    return vid_list


def add_video(**kwargs):
    """ Adds one video to DB """
    session = Session()
    c = kwargs['channel']
    channel = session.query(Channels).filter_by(channel_name=c).one_or_none()
    if channel:
        logging.info(channel.serialize)
        channel_id = channel.id
        channel_name = channel.channel_name
        logging.info(channel_id)
        logging.info(channel_name)
    else:
        # Bail out since there is no channel ID
        logging.info(f"{kwargs['channel']} NOT FOUND")
        logging.info('Use add_channel() command to add a new channel')
        return False
    exists = session.query(Videos).filter_by(video_title=kwargs['video_title']).scalar() is not None
    if exists:
        logging.info(f'{kwargs["video_title"]} ALREADY EXISTS')
        return False
    else:
        # Being explicit in adding of data to DB
        vid_dict = {
            "channel_id": channel_id,
            "video_title": kwargs['video_title'],
            "video_id": kwargs['video_id'],
            "video_url": kwargs['video_url'],
            "date_published": kwargs['date_published'],
            "summary": kwargs['summary'],
            "media_thumbnail": kwargs['media_thumbnail'],
            }
        logging.info(vid_dict)

        vid = Videos(**vid_dict)
        vid.channel_name = channel_name
        session.add(vid)
        session.commit()
        return True


def update_video(_id, **kwargs):
    """ Updates video by ID """
    session = Session()
    exists = session.query(Videos).filter_by(id=_id).scalar() is not None
    if exists:
        vid = session.query(Videos).filter_by(id=_id).first()
        vid.update(**kwargs)
        session.commit()
    else:
        logging.info(f'{_id} NOT FOUND')
        return False
    return True


def delete_video(_id):
    """ Deletes video by ID """
    session = Session()
    exists = session.query(Videos).filter_by(id=_id).scalar() is not None
    if exists:
        session.query(Videos).filter_by(id=_id).delete()
        session.commit()
    else:
        logging.info(f'{_id} NOT FOUND')
        return False
    return True


# #### VIDEO UTILS ####

def download_video(download_dir, channel_name, url):
    """ Downloads the YT video to the _feed_videos """
    ydl_opts = {
        # New File output:
        'embedthumbnail': True,
        'writethumbnail': True,
        # This doesnt seem to work?
        'addmetadata': True,
        ''
        # Example Output: <channel_name>/<video_title video_id.mp4>
        # video_id
        'outtmpl': f'{download_dir}/{channel_name}/%(id)s.%(ext)s',
        # Download the best mp4 video available, or the best video if no mp4 available
        'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b',
        # No color in terminal
        'no_color': True,
        # Send to ffmpeg for MP4
        'postprocessors': [
            {'key': 'FFmpegMetadata'},
            {'key': 'EmbedThumbnail'}
        ],
        # Number of retries
        'retries': 2,
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except:
            # TODO find exceptions and write code for them
            logging.info("DOH! YoutubeDL issue")
            return False
    return True


def get_videos_details(url, channel_name, today):
    """ Grabs the video data from YouTube feed, writes it to DB """
    feed_entries = feedparser.parse(url)
    for entry in feed_entries['entries']:
        a = arrow.get(entry['published'])
        date_published = a.format('YYYY-MM-DD')
        if date_published == today:
            # Run it through the video filter
            cold_filtered = vfilter(_channel=channel_name, _video_title=entry['title'])
            if cold_filtered:
                # Check if entry exists in DB
                session = Session()
                vid = session.query(Videos).filter_by(video_title=entry['title']).one_or_none()
                if vid:
                    logging.info(f"{entry['title']} ALREADY IN DB")
                else:
                    add_vid = {
                        "channel": channel_name,
                        "video_title": entry['title'],
                        "video_id": entry['yt_videoid'],
                        "video_url": entry['link'],
                        "date_published": date_published,
                        "summary": entry['summary'],
                        "media_thumbnail": entry['media_thumbnail'][0]['url'],
                    }
                    added = add_video(**add_vid)
                    if added:
                        logging.info(f"{entry['title']} ADDED TO DB")
                    else:
                        logging.info(f"{entry['title']} NOT ADDED TO DB, DOH!")
            else:
                logging.info("Video does NOT pass the filter, discarding.")
                logging.info(f"Video title: {entry['title']}")
        else:
            logging.info(f"Video was published in the past, skipping.")
            logging.info(f"Video title: {entry['title']}")
            logging.info(f"Video Date: {date_published}")
    return True


def get_old_videos(last_week):
    """ Returns a list of all old videos in DB """
    session = Session()
    old_vids = session.query(Videos).filter_by(date_published=last_week).all()
    vid_list = []
    for vid in old_vids:
        vid_list.append(vid.serialize)
    # Send a list of dicts back
    return vid_list


def find_video_file(video_id, path):
    """ Find a video in the path returns a list """
    result = []
    # print(video_id)
    # print(path)
    for root, dirs, files in os.walk(path):
        # print(files)
        for name in files:
            if fnmatch.fnmatch(name, f'*{video_id}*'):
                result.append(os.path.join(root, name))
    return result


# ##### VIDEO FILTER HELPERS #####


def get_filter(_id):
    """ Returns one filter  by ID """
    session = Session()
    filt = session.query(VideoFilters).filter_by(id=_id).one_or_none()
    if filt:
        # Return a json dict from DB
        return filt.serialize
    else:
        # Return a false
        logging.info(f'{_id} NOT FOUND')
        return False


def get_all_filters():
    """ Returns all filters in DB as list """
    session = Session()
    flts = session.query(VideoFilters).all()
    flt_list = []
    for flt in flts:
        flt_list.append(flt.serialize)
    return flt_list


def get_channel_filters(channel_id):
    """ Returns all filters in DB as list """
    session = Session()
    channel = session.query(Channels).filter_by(channel_id=channel_id).one_or_none()
    if channel:
        # Get all the video filters attached to the channel
        flts = session.query(VideoFilters).filter_by(channel_id=channel_id).all()
        flt_list = []
        for flt in flts:
            flt_list.append(flt.serialize)
        return flt_list
    else:
        # Bail out since there is no channel ID
        logging.info(f"{channel_id} NOT FOUND")
        logging.info('Use add_channel() command to add a new channel')
        return False


def add_filter(**kwargs):
    """ Adds one filter to DB """
    session = Session()
    c = kwargs['channel']
    channel = session.query(Channels).filter_by(channel_name=c).one_or_none()
    if channel:
        logging.info(channel.serialize)
        channel_id = channel.id
        channel_name = channel.channel_name
        logging.info(channel_id)
        logging.info(channel_name)
    else:
        # Bail out since there is no channel ID
        logging.info(f"{kwargs['channel']} NOT FOUND")
        logging.info('Use add_channel() command to add a new channel')
        return False
    exists = session.query(VideoFilters).filter_by(filter_name=kwargs['filter_name']).scalar() is not None
    if exists:
        logging.info(f'{kwargs["filter_name"]} ALREADY EXISTS')
        return False
    else:
        # Being explicit in adding of data to DB
        flt_dict = {
            "channel_id": channel_id,
            "channel_name": channel_name,
            "filter_name": kwargs['filter_name'],
            "filter_text": kwargs['filter_text'],
            "enabled": kwargs['enabled']
            }
        logging.info(flt_dict)

        flt = VideoFilters(**flt_dict)
        flt.channel_name = channel_name
        session.add(flt)
        session.commit()
        return True


def update_filter(_id, **kwargs):
    """ Updates filter by ID """
    session = Session()
    exists = session.query(VideoFilters).filter_by(id=_id).scalar() is not None
    if exists:
        flt = session.query(VideoFilters).filter_by(id=_id).first()
        flt.update(**kwargs)
        session.commit()
    else:
        logging.info(f'{_id} NOT FOUND')
        return False
    return True


def delete_filter(_id):
    """ Deletes filter by ID """
    session = Session()
    exists = session.query(VideoFilters).filter_by(id=_id).scalar() is not None
    if exists:
        session.query(VideoFilters).filter_by(id=_id).delete()
        session.commit()
    else:
        logging.info(f'{_id} NOT FOUND')
        return False
    return True


# ##### JELLYFIN HELPERS #####


def refresh_jellyfin_library(server_ip, api_key):
    url = f"http://{server_ip}:8096/Library/Refresh"
    headers = {
        "X-Emby-Token": api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)
    # TODO Add try/except for failure
    return True

