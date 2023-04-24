# Data Generation Process

1. Run `retrieve-comments.py` or `retrieve-top-comments.py` to get the comments from your specified video(s).
2. Run `add-parent-reply.py` and give it your file generated above to give replies their parents comment text. Run `add-channel-name.py` to add the relevant channel names to each lines of the `csv`
3. Copy your `.csv` file into the `labelled` folder and run `spam-labeller.py` to label the comments.