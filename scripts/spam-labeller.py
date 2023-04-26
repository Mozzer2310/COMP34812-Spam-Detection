import tkinter as tk
import csv
from tempfile import NamedTemporaryFile
import shutil

fields = ["video_id", "video_name", "channel_name",
          "comment_id", "comment", "username", "class"]
index = 0
max_length = 400


def truncateComment(commentText):
    """Truncates a comment to reduce its length so it fits inside the GUI

    Args:
        commentText (_type_): The tkiner StringVar that holds the text of the comment

    Returns:
        _type_: A truncated string to shorten the length of the comment
    """
    partition = commentText.partition("[REPLY]")
    if partition[1] == '':
        return (commentText[:max_length*2] + '..(TRUNCATED)') if len(commentText) > max_length*2 else commentText
    else:
        mainText = (partition[0][:max_length] + '..(TRUNCATED)') if len(
            partition[0]) > max_length else partition[0]
        replyText = (partition[2][:max_length] + '..(TRUNCATED)') if len(
            partition[2]) > max_length else partition[2]
        return f"{mainText} [REPLY] {replyText}"


def btnHam(commentIDText, commentText, authorText, contextText, titleText, classText, countText, channelText):
    """Updates the row in the csv for the current comment with the class set to 'ham'

    Args:
        commentIDText (_type_): The tkiner StringVar that holds the comment ID
        commentText (_type_): The tkiner StringVar that holds the comment text
        authorText (_type_): The tkiner StringVar that holds the author of the comment
        contextText (_type_): The tkiner StringVar that holds the context of the video
        titleText (_type_): The tkiner StringVar that holds the title of the video
        classText (_type_): The tkiner StringVar that holds the class of the video
        countText (_type_): The tkiner StringVar that holds the count of labelled comments text
        channelText (_type_): The tkiner StringVar that holds the channel name text
    """
    global comment_count
    print("Ham.")

    # Creates a temporary file
    tempfile = NamedTemporaryFile(mode='w', delete=False)

    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)

        # Finds the row in the csv matching the current comment from the GUI and set its class to 'ham'
        for row in reader:
            if row['comment_id'] == str(commentIDText.get()):
                print('updating row', row['comment_id'])
                row['class'] = "ham"
                classes[index-1] = "ham"
            row = {
                'video_id': row['video_id'],
                'video_name': row['video_name'],
                'channel_name': row['channel_name'],
                'comment_id': row['comment_id'],
                'comment': row['comment'],
                'username': row['username'],
                'class': row['class']}
            writer.writerow(row)

    # Moves the temp file to the current file
    shutil.move(tempfile.name, filename)

    # Increments the count of labelled comments and sets the text
    comment_count += 1
    countText.set(f"{comment_count}/{total_comments}")

    # Goes to the next comment
    btnNext(commentIDText, commentText, authorText, contextText,
            titleText, classText, countText, channelText)


def btnSpam(commentIDText, commentText, authorText, contextText, titleText, classText, countText, channelText):
    global comment_count
    """Updates the row in the csv for the current comment with the class set to 'spam'

    Args:
        commentIDText (_type_): The tkiner StringVar that holds the comment ID
        commentText (_type_): The tkiner StringVar that holds the comment text
        authorText (_type_): The tkiner StringVar that holds the author of the comment
        contextText (_type_): The tkiner StringVar that holds the context of the video
        titleText (_type_): The tkiner StringVar that holds the title of the video
        classText (_type_): The tkiner StringVar that holds the class of the video
        countText (_type_): The tkiner StringVar that holds the count of labelled comments text
        channelText (_type_): The tkiner StringVar that holds the channel name text
    """
    print("Spam.")

    # Creates a temporary file
    tempfile = NamedTemporaryFile(mode='w', delete=False)

    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)

        # Finds the row in the csv matching the current comment from the GUI and set its class to 'spam'
        for row in reader:
            if row['comment_id'] == str(commentIDText.get()):
                print('updating row', row['comment_id'])
                row['class'] = "spam"
                classes[index-1] = "spam"
            row = {
                'video_id': row['video_id'],
                'video_name': row['video_name'],
                'channel_name': row['channel_name'],
                'comment_id': row['comment_id'],
                'comment': row['comment'],
                'username': row['username'],
                'class': row['class']}
            writer.writerow(row)

    # Moves the temp file to the current file
    shutil.move(tempfile.name, filename)

    # Increments the count of labelled comments and sets the text
    comment_count += 1
    countText.set(f"{comment_count}/{total_comments}")

    # Goes to the next comment
    btnNext(commentIDText, commentText, authorText, contextText,
            titleText, classText, countText, channelText)


def btnNeutral(commentIDText, commentText, authorText, contextText, titleText, classText, countText, channelText):
    """Updates the row in the csv for the current comment with the class set to 'neutral'

    Args:
        commentIDText (_type_): The tkiner StringVar that holds the comment ID
        commentText (_type_): The tkiner StringVar that holds the comment text
        authorText (_type_): The tkiner StringVar that holds the author of the comment
        contextText (_type_): The tkiner StringVar that holds the context of the video
        titleText (_type_): The tkiner StringVar that holds the title of the video
        classText (_type_): The tkiner StringVar that holds the class of the video
        countText (_type_): The tkiner StringVar that holds the count of labelled comments text
        channelText (_type_): The tkiner StringVar that holds the channel name text
    """
    global comment_count
    print("Neutral.")

    # Creates a temporary file
    tempfile = NamedTemporaryFile(mode='w', delete=False)

    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)

        # Finds the row in the csv matching the current comment from the GUI and set its class to 'neutral'
        for row in reader:
            if row['comment_id'] == str(commentIDText.get()):
                print('updating row', row['comment_id'])
                row['class'] = "neutral"
                classes[index-1] = "neutral"
            row = {
                'video_id': row['video_id'],
                'video_name': row['video_name'],
                'channel_name': row['channel_name'],
                'comment_id': row['comment_id'],
                'comment': row['comment'],
                'username': row['username'],
                'class': row['class']}
            writer.writerow(row)

    # Moves the temp file to the current file
    shutil.move(tempfile.name, filename)

    # Increments the count of labelled comments and sets the text
    comment_count += 1
    countText.set(f"{comment_count}/{total_comments}")

    # Goes to the next comment
    btnNext(commentIDText, commentText, authorText, contextText,
            titleText, classText, countText, channelText)


def btnNext(commentIDText, commentText, authorText, contextText, titleText, classText, channelText):
    """Displays the next comment from the csv

    Args:
        commentIDText (_type_): The tkiner StringVar that holds the comment ID
        commentText (_type_): The tkiner StringVar that holds the comment text
        authorText (_type_): The tkiner StringVar that holds the author of the comment
        contextText (_type_): The tkiner StringVar that holds the context of the video
        titleText (_type_): The tkiner StringVar that holds the title of the video
        classText (_type_): The tkiner StringVar that holds the class of the video
        channelText (_type_): The tkiner StringVar that holds the channel name text
    """
    global index
    print("Next.")

    # Sets the textvariable of the relevant parts of the comment to the next comment
    commentIDText.set(commentIDs[index])
    commentText.set(truncateComment(comments[index]))
    authorText.set(authors[index])
    contextText.set(contexts[index])
    titleText.set(titles[index])
    classText.set(classes[index])
    channelText.set(channels[index])

    # increments the index value
    index += 1


def btnPrev(commentIDText, commentText, authorText, contextText, titleText, classText, channelText):
    """Displays the previous comment from the csv

    Args:
        commentIDText (_type_): The tkiner StringVar that holds the comment ID
        commentText (_type_): The tkiner StringVar that holds the comment text
        authorText (_type_): The tkiner StringVar that holds the author of the comment
        contextText (_type_): The tkiner StringVar that holds the context of the video
        titleText (_type_): The tkiner StringVar that holds the title of the video
        classText (_type_): The tkiner StringVar that holds the class of the video
        channelText (_type_): The tkiner StringVar that holds the channel name text
    """
    global index
    print("Prev.")
    # Decrements the index value to the previous comment (-2 as the current index is 1 ahead)
    index += -2

    # Sets the textvariable of the relevant parts of the comment to the next comment
    commentIDText.set(commentIDs[index])
    commentText.set(truncateComment(comments[index]))
    authorText.set(authors[index])
    contextText.set(contexts[index])
    titleText.set(titles[index])
    classText.set(classes[index])
    channelText.set(channels[index])

    # increments the index value
    index += 1


def btnClear(commentIDText, classText, countText):
    """Sets the class of the current comment to 0 (undefined)

    Args:
        commentIDText (_type_): The tkiner StringVar that holds the comment ID
        classText (_type_): The tkiner StringVar that holds the class of the video
        countText (_type_): The tkiner StringVar that holds the count of labelled comments text
    """
    global comment_count
    '''if button is clicked, display message'''
    print("Clear.")

    # Creates a temporary file
    tempfile = NamedTemporaryFile(mode='w', delete=False)

    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        # Finds the row in the csv matching the current comment from the GUI and set its class to '0'
        for row in reader:
            if row['comment_id'] == str(commentIDText.get()):
                print('updating row', row['comment_id'])
                row['class'] = "0"
                classes[index-1] = "0"
            row = {
                'video_id': row['video_id'],
                'video_name': row['video_name'],
                'channel_name': row['channel_name'],
                'comment_id': row['comment_id'],
                'comment': row['comment'],
                'username': row['username'],
                'class': row['class']}
            writer.writerow(row)

    classText.set(classes[index-1])

    # Decrements the labelled counter and displays the result
    comment_count -= 1
    countText.set(f"{comment_count}/{total_comments}")

    # Moves the temp file to the current file
    shutil.move(tempfile.name, filename)


def createWindow():
    """Creates the tkinter GUI for the program
    """
    root = tk.Tk()  # create root window
    root.title("Label Comments")
    root.maxsize(900,  600)  # width x height

    # The comment information goes in this frame
    top_frame = tk.Frame(root,  width=790,  height=595,  bg='grey')
    top_frame.grid(row=0,  column=0,  padx=10,  pady=5)

    # The buttons go in this frame
    bottom_frame = tk.Frame(root,  width=790,  height=195,  bg='grey')
    bottom_frame.grid(row=1,  column=0,  padx=10,  pady=5)

    # Counter in this frame
    count_frame = tk.Frame(root,  width=790,  height=100,  bg='grey')
    count_frame.grid(row=2,  column=0,  padx=10,  pady=5)

    commentIDText = tk.StringVar()
    commentText = tk.StringVar()
    authorText = tk.StringVar()
    contextText = tk.StringVar()
    titleText = tk.StringVar()
    classText = tk.StringVar()
    channelText = tk.StringVar()
    countText = tk.StringVar()
    countText.set(f"{comment_count}/{total_comments}")

    # Counter
    internal_count_frame = tk.Frame(count_frame)
    internal_count_frame.grid(row=0, column=0, padx=5, pady=5)
    tk.Label(internal_count_frame, text="Number of Labelled Comments: ").grid(
        row=0, column=0, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Label(internal_count_frame, textvariable=countText).grid(
        row=0, column=1, padx=5, pady=5, sticky='w'+'e'+'n'+'s')

    # Buttons
    tk.Button(bottom_frame, text="CLEAR", command=lambda: btnClear(commentIDText, commentText, authorText, contextText, titleText, classText, countText, channelText)).grid(
        row=0, column=0, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Button(bottom_frame, text="PREV", command=lambda: btnPrev(commentIDText, commentText, authorText, contextText, titleText, classText, countText, channelText)).grid(
        row=0, column=1, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Button(bottom_frame, text="SPAM", command=lambda: btnSpam(commentIDText, commentText, authorText, contextText, titleText, classText, countText, channelText), bg='firebrick3', activebackground='firebrick1').grid(
        row=0, column=2, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Button(bottom_frame, text="HAM", command=lambda: btnHam(commentIDText, commentText, authorText, contextText, titleText, classText, countText, channelText), bg='chartreuse4', activebackground='chartreuse3').grid(
        row=0, column=3, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Button(bottom_frame, text="NEUTRAL", command=lambda: btnNeutral(commentIDText, commentText, authorText, contextText, titleText, classText, countText, channelText), bg='slate blue', activebackground='light slate blue').grid(
        row=0, column=4, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Button(bottom_frame, text="NEXT", command=lambda: btnNext(commentIDText, commentText, authorText, contextText, titleText, classText, countText, channelText)).grid(
        row=0, column=5, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')

    # Comment Information
    # Comment ID
    id_frame = tk.Frame(top_frame)
    id_frame.grid(row=0, column=0, padx=5, pady=5)

    tk.Label(id_frame, text="Comment ID:").grid(
        row=0, column=0, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Label(id_frame, textvariable=commentIDText, wraplength=500, justify=tk.LEFT).grid(
        row=0, column=1, padx=5,  pady=5, sticky='w'+'e'+'n'+'s')

    # Video Title
    title_frame = tk.Frame(top_frame)
    title_frame.grid(row=1, column=0, padx=5, pady=5)

    tk.Label(title_frame, text="Video Title:").grid(
        row=0, column=0, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Label(title_frame, textvariable=titleText, wraplength=500, justify=tk.LEFT).grid(
        row=0, column=1, padx=5,  pady=5, sticky='w'+'e'+'n'+'s')

    # Video Channel Name
    channel_frame = tk.Frame(top_frame)
    channel_frame.grid(row=2, column=0, padx=5, pady=5)

    tk.Label(channel_frame, text="Channel Name:").grid(
        row=0, column=0, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Label(channel_frame, textvariable=channelText, wraplength=500, justify=tk.LEFT).grid(
        row=0, column=1, padx=5,  pady=5, sticky='w'+'e'+'n'+'s')

    # Video Context
    context_frame = tk.Frame(top_frame)
    context_frame.grid(row=3, column=0, padx=5, pady=5)

    tk.Label(context_frame, text="Video Context:").grid(
        row=0, column=0, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Label(context_frame, textvariable=contextText, wraplength=500, justify=tk.LEFT).grid(
        row=0, column=1, padx=5,  pady=5, sticky='w'+'e'+'n'+'s')

    # Comment Author
    user_frame = tk.Frame(top_frame)
    user_frame.grid(row=4, column=0, padx=5, pady=5)

    tk.Label(user_frame, text="Username:").grid(
        row=0, column=0, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Label(user_frame, textvariable=authorText, wraplength=500, justify=tk.LEFT).grid(
        row=0, column=1, padx=5,  pady=5, sticky='w'+'e'+'n'+'s')

    # Current Label
    class_frame = tk.Frame(top_frame)
    class_frame.grid(row=5, column=0, padx=5, pady=5)

    tk.Label(class_frame, text="CURRENT CLASS:").grid(
        row=0, column=0, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Label(class_frame, textvariable=classText,
             wraplength=500, justify=tk.LEFT).grid(row=0, column=1, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')

    # Comment
    comment_frame = tk.Frame(top_frame)
    comment_frame.grid(row=6, column=0, padx=5, pady=5)

    tk.Label(comment_frame, text="Comment:").grid(
        row=0, column=0, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Label(comment_frame, textvariable=commentText,
             wraplength=500, justify=tk.LEFT).grid(row=0, column=1, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')

    # Runs the loop of the GUI
    root.mainloop()


if __name__ == "__main__":
    global commentIDs, comments, authors, contexts, titles, channels, filename, total_comments, comment_count
    commentIDs = []
    comments = []
    authors = []
    contexts = []
    titles = []
    classes = []
    channels = []
    comment_count = 0

    # Take user input for the file name and append folder path
    filename = input("Please enter a filename for the CSV: ")
    if filename[-4:] != '.csv':
        filename += '.csv'
    filename = "../data/labelled/" + filename

    # Read in all the comments from the csv and store the relevant parts in their respective lists
    with open(filename, mode='r', encoding='utf8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        total_comments = 0
        for row in csv_reader:
            total_comments += 1
            if row["class"] == "0":
                commentIDs.append(row["comment_id"])
                comments.append(row["comment"])
                authors.append(row["username"])
                titles.append(row["video_name"])
                classes.append(row["class"])
                channels.append(row['channel_name'])
                # TODO: Add code to read contexts when thats done
                # - Probably store as video_id context pair of some form
                # - when next/prev is pressed display the context per video_id
                contexts.append("")
            else:
                comment_count += 1

    # Creates the tkinter window
    createWindow()
