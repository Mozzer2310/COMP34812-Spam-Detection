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


def getNextPageTopLevel(nextpage: str, comments: list, videoId: str) -> list:
    """Recursive function that continually makes requests to the YouTube Data API until no nextPageToken is returned

    Args:
        nextpage (str): This is the next page token returned by the YouTube Data API
        comments (list): This is the current list of top level comments
        videoId (str): This is the Video ID of the YouTube video

    Returns:
        list: the list of the top level comments from video with id videoId
    """
    request = youtube.commentThreads().list(
        part="snippet",
        maxResults=100,
        order="relevance",
        pageToken=nextpage,
        videoId=videoId
    )
    response = request.execute()

    # If there is no nextPageToken then set it to empty string
    try:
        nextpage = response["nextPageToken"]
    except KeyError:
        nextpage = ""

    comments = comments + (response["items"])

    # If there is a nextpage then recurse the function
    if nextpage:
        comments = getNextPageTopLevel(nextpage, comments, videoId)

    return comments


def getNextPageReplies(nextpage: str, replies: list, parentId: str) -> list:
    """_summary_

    Args:
        nextpage (str): This is the next page token returned by the YouTube Data API
        replies (list): This is the current list of replies
        parentId (str): The ID of the parent comment of the replies

    Returns:
        list: the list of the replies to parent with id parentId
    """
    request = youtube.comments().list(
        part="snippet",
        maxResults=100,
        pageToken=nextpage,
        parentId=parentId
    )
    response = request.execute()

    try:
        nextpage = response["nextPageToken"]
    except KeyError:
        nextpage = ""

    replies = replies + (response["items"])

    if nextpage:
        replies = getNextPageReplies(nextpage, replies, parentId)

    return replies


def getComments(videoId: str):
    """Retrives all the comments from a YouTube video and stores them in a .csv file

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

    # Check is a nextPageToken exists
    try:
        nextpage = response["nextPageToken"]
    except KeyError:
        nextpage = ""

    # If a next page exists then run the getNextPageTopLevel function
    if nextpage:
        comments = getNextPageTopLevel(nextpage, comments, videoId)

    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Loop over the top level comments
        for item in comments:
            useful = item["snippet"]["topLevelComment"]
            commentID = useful['id']
            commentText = useful['snippet']['textOriginal']
            username = useful['snippet']['authorDisplayName']
            # Write the top level comment to the csv
            writer.writerow({
                "video_id": videoId,
                "video_name": videoTitle,
                "comment_id": commentID,
                "comment": commentText,
                "username": username,
                "class": 0
            })
            # Check the number of replies, if there is replies then retrieve them
            numreplies = item['snippet']['totalReplyCount']
            if numreplies > 0:
                request = youtube.comments().list(
                    part="snippet",
                    maxResults=100,
                    parentId=useful['id']
                )
                response = request.execute()
                replies = response["items"]

                # Check is a nextPageToken exists
                try:
                    nextpage = response["nextPageToken"]
                except KeyError:
                    nextpage = ""

                # If a next page exists then run the getNextPageTopLevel function
                if nextpage:
                    replies = getNextPageReplies(
                        nextpage, replies, useful['id'])

                # Loop over the replies and write them to the csv
                for reply in replies:
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
