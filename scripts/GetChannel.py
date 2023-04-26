import unstaged.config as config
import googleapiclient.discovery

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = config.api_key

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

def getChannel(videoId):
    # Get the data for the video from the YouTube Data API
    request = youtube.videos().list(
        part="snippet",
        id=videoId
    )
    response = request.execute()

    for item in response["items"]:
        return item["snippet"]["channelTitle"]