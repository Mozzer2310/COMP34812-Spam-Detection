import unstaged.config as config
import googleapiclient.discovery

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = config.api_key

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

def getChannel(videoId: str) -> str:
    """Takes a YouTube video ID and returns the channel name

    Args:
        videoId (str): The video ID of a YouTube video

    Returns:
        str: the channel name of the publisher of the video
    """
    # Get the data for the video from the YouTube Data API
    request = youtube.videos().list(
        part="snippet",
        id=videoId
    )
    response = request.execute()

    for item in response["items"]:
        return item["snippet"]["channelTitle"]