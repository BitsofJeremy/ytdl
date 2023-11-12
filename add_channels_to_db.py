import argparse
import sys

from utils import add_channel, get_channel_by_name

# Takes 2 args channel_name and channel_url, then adds them to the DB
# Example:
# add_channels_to_db.py --channel_name "SlivkiShow EN"
# --channel_url "https://www.youtube.com/feeds/videos.xml?channel_id=UC37D-JTE7-V-L-VIrxzzZpQ"


def main(**kwargs):
    channel_name = kwargs.get('channel_name')
    channel_url = kwargs.get('channel_url')

    print(channel_name)
    print(channel_url)
    exists = get_channel_by_name(channel_name=channel_name)
    if exists:
        print(f"{channel_name} ALREADY IN DB")
    else:
        added = add_channel(channel_name=channel_name, url=channel_url)
        if added:
            # It worked
            print("it worked!")
            return True
        else:
            print('Something failed.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--channel_name',
        help='Enter the Channel Name [title]',
        required=True
    )

    parser.add_argument(
        '--channel_url',
        help='Enter the Chanel URL',
        required=True
    )
    args = parser.parse_args()

    # Convert the argparse.Namespace to a dictionary: vars(args)
    arg_dict = vars(args)
    # pass dictionary to main
    main(**arg_dict)
    sys.exit(0)


