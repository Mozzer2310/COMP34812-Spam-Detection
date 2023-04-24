Use this folder along with spam labeler, put you `.csv` file in the labelled folder and running `spam-labeler.py` will allow you to label the comments.

## Rules Followed when Labelling

**HAM:**
- [MAIN]: comment contains context relevant to the video
- [MAIN] [REPLY]: replied comment contains context relevant to a video, or is obviously related to main comment

**SPAM:**
- [MAIN]: comment or username attempts to direct people away from the content
- [MAIN] [REPLY]:  replied comment or username attempts to direct people away from the content regardless of main comment

**NEUTRAL:**
- [MAIN]:  comment does not contain context relevant to the video but is not harmful
- [MAIN] [REPLY]: replied comment does not contain context relevant to the video but is not harmful, or its relationship to the main comment cannot be easily inferred but is still not harmful