import unstaged.config as config
import csv
import googleapiclient.discovery
from datetime import datetime
import os.path

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = config.api_key

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)


fieldnames = ["video_id", "video_name",
              "comment_id", "comment", "username", "class"]


def getComments(videoId: str):
    """Retrives the top 50 comments from a YouTube video and stores them in a .csv file

    Args:
        videoId (str): The YouTube video ID of a video
    """
    request = youtube.videos().list(
        part="snippet",
        id=videoId
    )
    response = request.execute()

    videoTitle = response["items"][0]["snippet"]["title"]

    request = youtube.commentThreads().list(
        part="snippet",
        maxResults=100,
        order="relevance",
        videoId=videoId
    )
    response = request.execute()

    comments = response["items"]

    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        index = 0
        total_replies = 0

        # Loop over the top level comments
        for item in comments:
            # If 50 comments have been written exit the function
            if index >= 50:
                return
            useful = item["snippet"]["topLevelComment"]
            commentID = useful['id']
            commentText = useful['snippet']['textOriginal']
            username = useful['snippet']['authorDisplayName']
            writer.writerow({
                "video_id": videoId,
                "video_name": videoTitle,
                "comment_id": commentID,
                "comment": commentText,
                "username": username,
                "class": 0
            })
            index += 1
            # Check the number of replies, if there is replies then retrieve the top 8
            if not total_replies >= 50:
                numreplies = item['snippet']['totalReplyCount']
                if numreplies > 0:
                    request = youtube.comments().list(
                        part="snippet",
                        maxResults=8,
                        parentId=useful['id']
                    )
                    response = request.execute()
                    replies = response["items"]

                    # Loop over the replies and write them to the csv
                    for reply in replies:
                        # If 50 comments have been written exit the function
                        if index >= 50:
                            return
                        useful = reply["snippet"]
                        replyId = reply["id"]
                        replyText = useful['textOriginal']
                        username = useful['authorDisplayName']
                        writer.writerow({
                            "video_id": videoId,
                            "video_name": videoTitle,
                            "comment_id": replyId,
                            "comment": replyText,
                            "username": username,
                            "class": 0
                        })
                        index += 1
                total_replies += numreplies


if __name__ == "__main__":
    global csv_filename
    global num_comments
    num_comments = 0

    # Take user input for the file name and append folder path
    csv_filename = input("Please enter a filename for the CSV: ")
    if csv_filename[-4:] != '.csv':
        csv_filename += '.csv'
    csv_filename = "../data/comments/" + csv_filename

    # If the file doesn't exist then write it and its header, if it does exist count the number of existing comments
    file_exists = os.path.isfile(csv_filename)
    if not file_exists:
        with open(csv_filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    else:
        with open(csv_filename, mode='r', encoding='utf8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                num_comments += 1

    current_line_count = num_comments
    # Create a loop that asks the user to enter video IDs
    while (True):
        input_video_id = input("(Press Enter to skip) Enter a video ID: ")

        # If no video specified exit the loop
        if (input_video_id == ""):
            break

        # Get the comments for the video specified by the user
        getComments(videoId=input_video_id)

        # Display information about comments retrieved
        print("Complete")
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"Time: {now}")

        with open(csv_filename, mode='r', encoding='utf8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                line_count += 1
        print(f"No. Comments: {line_count - current_line_count}")
        current_line_count += line_count

    # Count the total coments in the csv file and display to the user
    with open(csv_filename, mode='r', encoding='utf8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            line_count += 1
    print(f"Total No. Comments: {line_count}")
