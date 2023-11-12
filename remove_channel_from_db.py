import argparse
import sys

from utils import delete_channel, get_channel_by_name

# Takes 2 args channel_name and channel_url, then removes them to the DB
# Example:
# remove_channel_from_db.py --channel_name "SlivkiShow EN"


def main(**kwargs):
    channel_name = kwargs.get('channel_name')
    print(channel_name)
    channel = get_channel_by_name(channel_name=channel_name)
    if channel:
        print(f"{channel_name} IN DB")
        deleted = delete_channel(_id=channel['id'])
        if deleted:
            print("Deleted Channel")
        else:
            print("Oops, delete failed.")
    else:
        print("Channel not found.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--channel_name',
        help='Enter the Channel Name [title]',
        required=True
    )
    args = parser.parse_args()

    # Convert the argparse.Namespace to a dictionary: vars(args)
    arg_dict = vars(args)
    # pass dictionary to main
    main(**arg_dict)
    sys.exit(0)


