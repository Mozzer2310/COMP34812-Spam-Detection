import csv
from tempfile import NamedTemporaryFile
import shutil
import unstaged.config as config
import googleapiclient.discovery

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = config.api_key

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

fields = ["video_id", "video_name",
          "comment_id", "comment", "username", "class"]

new_fields = ["video_id", "video_name", "channel_name",
              "comment_id", "comment", "username", "class"]

if __name__ == "__main__":
    # Take user input for the file name and path
    filename = input("Please enter the filepath and filename for the CSV: ")
    if filename[-4:] != '.csv':
        filename += '.csv'

    video_ids = []
    # Read in the video ids for each comment
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        for row in reader:
            if row['video_id'] != 'video_id':
                video_ids.append(row["video_id"])

    # Remove duplicates from the list
    video_ids = list(dict.fromkeys(video_ids))

    # combine the id list into a comma separated string
    id_list = ",".join(video_ids)
    # Get the data for the video from the YouTube Data API
    request = youtube.videos().list(
        part="snippet",
        id=id_list
    )
    response = request.execute()

    # Create a list of channel names
    channel_names = []
    for item in response["items"]:
        channel_names.append(item["snippet"]["channelTitle"])

    # Create a temporary file
    tempfile = NamedTemporaryFile(mode='w', delete=False)

    # Inset the headers of the csv file at the front of each list
    video_ids.insert(0, 'video_id')
    channel_names.insert(0, 'channel_name')

    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=new_fields)

        # For each row in the file add a new field which has the channel name of the publisher of the video which the comment was made on
        for row in reader:
            for id in video_ids:
                if id == row['video_id']:
                    index = video_ids.index(id)
                    new_row = {
                        'video_id': row['video_id'],
                        'video_name': row['video_name'],
                        'channel_name': channel_names[index],
                        'comment_id': row['comment_id'],
                        'comment': row['comment'],
                        'username': row['username'],
                        'class': row['class']
                    }
            writer.writerow(new_row)

    # Move the temp file to the original file
    shutil.move(tempfile.name, filename)
