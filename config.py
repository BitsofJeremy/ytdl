import os

# ####### CONFIG ########
# Where do we put the video files
DL_DIR = os.getenv('DL_DIR')

JELLY_ENABLED = os.getenv('JELLY_ENABLED')
# If your JellyFin directory is different than your download directory
JELLY_DIR = os.getenv('JELLY_DIR')
# IP and API key for your JellyFin server
JELLY_IP = os.getenv('JELLY_IP')
JELLY_API_KEY = os.getenv('JELLY_API_KEY')

if DL_DIR is None:
    DL_DIR = '/tmp/'

if JELLY_ENABLED is None:
    # JellyFin not configured
    JELLY_ENABLED = False
    JELLY_DIR = '/tmp/'
else:
    JELLY_ENABLED = True

# Days back to delete
TTD = -7

# Feed OPML file
OPML_FILE = 'feeds-test.opml'

# Feed CSV file
CSV_FILE = "test_subscriptions.csv"
