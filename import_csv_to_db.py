import csv
import config
from utils import add_channel, get_channel_by_name

# Takes an CSV file from Google export subscriptions.csv and adds all feeds to DB


def main():
    # Open the CSV file
    with open(config.CSV_FILE, 'r') as csvfile:
        # Create a CSV reader
        csvreader = csv.reader(csvfile)
        # Read the header row to get the column names
        header = next(csvreader)
        # Iterate through the rows in the CSV
        for row in csvreader:
            print(row)
            channel_id = row[0]
            channel_title = row[2]
            exists = get_channel_by_name(channel_name=channel_title)
            if exists:
                print(f"{channel_title} ALREADY IN DB")
            else:
                # Add each feed to DB
                feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
                added = add_channel(channel_name=channel_title, url=feed_url)
                if added:
                    # It worked
                    print(f"Added: {channel_title}")
                else:
                    print(f'Something failed:  {channel_title}')
    print("Finished")


if __name__ == '__main__':
    main()
