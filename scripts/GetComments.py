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

def getComments(videoId: str) -> tuple:
    """Takes a video ID of a YouTube video and retrieves the top 100 comments, and their replies, as well as the video title

    Args:
        videoId (str): The video ID of a YouTube video

    Returns:
        tuple: a list holding the comments of the video, and a string holding the title of the video
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

    output_comments = []
    # Loop over the top level comments
    for item in comments:
        useful = item["snippet"]["topLevelComment"]
        output_comments.append(useful['snippet']['textOriginal'])

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

            # Loop over the replies and write them to the csv
            for reply in replies:
                useful = reply["snippet"]
                replyText = useful['textOriginal']
                output_comments.append(replyText)

    return output_comments, videoTitle

if __name__ == "__main__":
    print(getComments("JspWFbynlmk"))