# filter_videos.py
from dbconfig import Channels, VideoFilters

# A simple filter for channels that have too many videos per day
# follow the rule: be explicit
# Returns True for videos we want to download

# TODO THIS IS NOT WORKING YET.....video filtering

def vfilter(_video_array):
    """ Expecting an array of video titles and channels
        Example: [{"The Hockey Guy": "Meetup"}]
    """

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

