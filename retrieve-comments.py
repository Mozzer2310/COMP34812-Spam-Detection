import config
import csv
import googleapiclient.discovery

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = config.api_key

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)


csv_filename = 'data/comments.csv'
fieldnames = ["video_id", "video_name",
              "comment_id", "comment", "username", "class"]


def getNextPageTopLevel(nextpage: str, comments: list, videoId: str) -> list:
    request = youtube.commentThreads().list(
        part="snippet",
        maxResults=100,
        order="relevance",
        pageToken=nextpage,
        videoId=videoId
    )
    response = request.execute()

    try:
        nextpage = response["nextPageToken"]
    except KeyError:
        nextpage = ""

    comments = comments + (response["items"])

    if nextpage:
        comments = getNextPageTopLevel(nextpage, comments, videoId)

    return comments


def getNextPageReplies(nextpage: str, replies: list, parentId: str) -> list:
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
    try:
        nextpage = response["nextPageToken"]
    except KeyError:
        nextpage = ""

    if nextpage:
        comments = getNextPageTopLevel(nextpage, comments, videoId)

    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

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
            numreplies = item['snippet']['totalReplyCount']
            if numreplies > 0:
                request = youtube.comments().list(
                    part="snippet",
                    maxResults=100,
                    parentId=useful['id']
                )
                response = request.execute()
                replies = response["items"]
                try:
                    nextpage = response["nextPageToken"]
                except KeyError:
                    nextpage = ""

                if nextpage:
                    replies = getNextPageReplies(
                        nextpage, replies, useful['id'])

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
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    getComments(videoId="9ehTRKTXheI")
    getComments(videoId="vfs9GW488pM")
