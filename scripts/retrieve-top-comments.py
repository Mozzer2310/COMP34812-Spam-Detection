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


# csv_filename = 'data/comments.csv'
fieldnames = ["video_id", "video_name",
              "comment_id", "comment", "username", "class"]


def getComments(videoId: str):

    request = youtube.videos().list(
        part="snippet",
        id=videoId
    )
    response = request.execute()

    videoTitle = response["items"][0]["snippet"]["title"]

    request = youtube.commentThreads().list(
        part="snippet",
        maxResults=50,
        order="relevance",
        videoId=videoId
    )
    response = request.execute()

    comments = response["items"]

    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        total_replies = 0
        for item in comments:
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
            if not total_replies >= 50:
                numreplies = item['snippet']['totalReplyCount']
                if numreplies > 0:
                    request = youtube.comments().list(
                        part="snippet",
                        maxResults=10,
                        parentId=useful['id']
                    )
                    response = request.execute()
                    replies = response["items"]

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
                total_replies += numreplies


if __name__ == "__main__":
    global csv_filename
    global num_comments
    num_comments = 0

    csv_filename = input("Please enter a filename for the CSV: ")
    if csv_filename[-4:] != '.csv':
        csv_filename += '.csv'
    csv_filename = "../data/comments/" + csv_filename

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
    while(True):
        input_video_id = input("(Press Enter to skip) Enter a video ID: ")
        if(input_video_id == ""):
            break
        getComments(videoId=input_video_id)
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

    with open(csv_filename, mode='r', encoding='utf8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            line_count += 1
    print(f"Total No. Comments: {line_count}")
