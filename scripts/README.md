# Scripts Explained

| Script | Purpose |
| ------ | ------- |
| `model-topics.py` | |
| `retrieve-comments.py` | This scripts allows the user to input YouTube video IDs, then all the comments of that video are retrieved and their useful data is put into a `.csv` file in `data/comments`. |
| `retrieve-top-comments.py` | This script does the same as the above except only the top 50 comments of a video are obtained |
| `add-parent-reply.py` | This script runs on the output `csv` of either `retrive` files, it takes the parent comment of a reply and embeds it before the comment text of the reply. In the form [MAIN] Parent [REPLY] Child |
| `add-channel-name.py` | This script runs on the output `csv` of either `retrive` scripts (after `add-parent-reply.py`) and adds a new field `channel_name`, which holds the name of the YouTube channel which published the video the comment is on. |
| `prepare-labelling.py` | This script automatically creates a `csv` file in the `../data/labelled/` folder from the output `csv` of either `retrive` scripts. It then runs `add-parent-reply.py` and `add-channel-name.py` for that file. |
| `spam-labeler.py` | This is a tool that reads a `.csv` from `data/labelled`, allowing a user to manually label the comment as 'spam' or 'ham'. |
| `data-reliability-generation.py` | This script generates a `csv` file for labelling from the labelled files created by each of the annotaters, the purpose of these files is so that they can be re-labelled by the other annotater in order to test the reliability of the annotations.|