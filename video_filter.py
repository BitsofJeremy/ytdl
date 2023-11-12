# video_filter.py

# TODO refactor to make it easier to add filters
# TODO make filtering a table in the DB
# TODO make filtering smarter

import logging
import logging.handlers

# Log the things
LOG_FILENAME = 'vfilter.log'
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

# A simple filter for channels that have too many videos per day
# follow the rule: be explicit
# Returns True for videos we want to download


def vfilter(_channel, _video_title):
    logger.info(_channel)
    logger.info(_video_title)

    # The Hockey Guy
    # Only grab the main content, not the Meetups or Live Streams
    if 'The Hockey Guy' in _channel:
        if 'Meetup' in _video_title:
            logger.info('The Hockey Guy skip Meetups, dont care')
            return False
        elif 'Live Stream' in _video_title:
            logger.info('The Hockey Guy skip Live Stream, dont care')
            return False
        else:
            logger.info('The Hockey Guy Downloading')
            return True

    # Olivio Sarikas
    # Only grab the main content, not the Meetups or Live Streams
    if 'Olivio Sarikas' in _channel:
        if 'Live Stream' in _video_title:
            logger.info('Olivio Sarikas skip Live Stream, dont care')
            return False
        else:
            logger.info('The Hockey Guy Downloading')
            return True

    # Ozzy Man Reviews
    # Only grab the main content, not the Amber Heard crap
    if 'Ozzy Man Reviews' in _channel:
        if 'Amber Heard' in _video_title:
            logger.info('Ozzy Man Reviews skip Amber Heard, dont care')
            return False
        if 'Quickies' in _video_title:
            logger.info('Ozzy Man Quickies skip')
            return False
        else:
            logger.info('Ozzy Man Reviews Downloading')
            return True

    # FX Evolution
    # Only grab the daily, not the LIVE show
    if 'FX Evolution' in _channel:
        if '[LIVE]' in _video_title:
            logger.info('FX Evolution [LIVE] show skip')
            return False
        else:
            logger.info('FX Evolution Downloading')
            return True

    # Sportsnet
    # Only show Avs or NHL game recaps
    # Discard the rest
    if 'SPORTSNET' in _channel:
        if 'Steve' in _video_title:
            logger.info('Steve D big dumb head remove')
            return False
        elif 'Avalanche' in _video_title:
            logger.info('Avs game recap')
            return True
        elif 'NHL' in _video_title:
            logger.info('NHL game recap')
            return True
        else:
            logger.info('All Other Sportsnet, dont care')
            return False

    # DPCcars
    # Only grab the Porsche things
    if 'DPCcars' in _channel:
        if 'Porsche' in _video_title:
            logger.info('Porsche only from DPCcars')
            return True
        else:
            logger.info('meh, other cars')
            return False

    # Guinness Six Nations
    # Only grab the highlights
    if 'Guinness Six Nations' in _channel:
        if 'Extended Highlights' in _video_title:
            logger.info('Guinness Six Nations Extended Highlights')
            return True
        else:
            logger.info('meh')
            return False

    # Extra Credits
    # Only grab the Extra Mythology and Extra History
    if 'Extra Credits' in _channel:
        if 'Extra Mythology' in _video_title:
            logger.info('Extra Credits: Extra Mythology')
            return True
        elif 'Extra History' in _video_title:
            logger.info('Extra Credits: Extra History')
            return True
        elif 'EXTRA HISTORY' in _video_title:
            logger.info('Extra Credits: Extra History')
            return True
        else:
            logger.info('meh')
            return False

    # Otherwise return True
    logger.info('Passed through the whole filter')
    return True


if __name__ == '__main__':
    vfilter(_channel='', _video_title='')

