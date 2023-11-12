import opml
import config
from utils import add_channel, get_channel_by_name

# Takes an opml file from Google export and adds all feeds to DB


def main():
    # Get our feeds
    feeds = opml.parse(config.OPML_FILE)
    for feed in feeds:
        feed_url = feed.xmlUrl
        feed_title = feed.title
        exists = get_channel_by_name(channel_name=feed_title)
        if exists:
            print(f"{feed_title} ALREADY IN DB")
        else:
            # Add each feed to DB
            added = add_channel(channel_name=feed_title, url=feed_url)
            if added:
                # It worked
                print(f"Added: {feed_title}")
            else:
                print(f'Something failed:  {feed_title}')
    print("Finished")


if __name__ == '__main__':
    main()
