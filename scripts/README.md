# Scripts Explained

| Script | Purpose |
| ------ | ------- |
| `model-topics.py` | |
| `retrieve-comments.py` | This scripts allows the user to input YouTube video IDs, then all the comments of that video are retrieved and their useful data is put into a `.csv` file in `data/comments` |
| `retrieve-top-comments.py` | This script does the same as the above except only the top 50 comments of a video are obtained |
| `spam-labeler.py` | This is a tool that reads a `.csv` from `data/labelled`, allowing a user to manually label the comment as 'spam' or 'ham' |