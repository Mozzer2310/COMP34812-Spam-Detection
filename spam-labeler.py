import tkinter as tk
import csv
from tempfile import NamedTemporaryFile
import shutil

filename = "data/comments.csv"
fields = ["video_id", "video_name",
              "comment_id", "comment", "username", "class"]
index = 0

def btnHam(commentIDText, commentText, authorText, contextText, titleText, classText):
    '''if button is clicked, display message'''
    print("Ham.")

    tempfile = NamedTemporaryFile(mode='w', delete=False)

    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row['comment_id'] == str(commentIDText.get()):
                print('updating row', row['comment_id'])
                row['class'] = "ham"
                classes[index-1] = "ham"
            row = {'video_id': row['video_id'], 'video_name': row['video_name'], 'comment_id': row['comment_id'], 'comment': row['comment'], 'username': row['username'], 'class': row['class']}
            writer.writerow(row)

    shutil.move(tempfile.name, filename)

    btnNext(commentIDText, commentText, authorText, contextText, titleText, classText)


def btnSpam(commentIDText, commentText, authorText, contextText, titleText, classText):
    '''if button is clicked, display message'''
    print("Spam.")

    tempfile = NamedTemporaryFile(mode='w', delete=False)

    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row['comment_id'] == str(commentIDText.get()):
                print('updating row', row['comment_id'])
                row['class'] = "spam"
                classes[index-1] = "spam"
            row = {'video_id': row['video_id'], 'video_name': row['video_name'], 'comment_id': row['comment_id'], 'comment': row['comment'], 'username': row['username'], 'class': row['class']}
            writer.writerow(row)

    shutil.move(tempfile.name, filename)

    btnNext(commentIDText, commentText, authorText, contextText, titleText, classText)

def btnNext(commentIDText, commentText, authorText, contextText, titleText, classText):
    global index
    '''if button is clicked, display message'''
    print("Next.")
    commentIDText.set(commentIDs[index])
    commentText.set(comments[index])
    authorText.set(authors[index])
    contextText.set(contexts[index])
    titleText.set(titles[index])
    classText.set(classes[index])
    index += 1

def btnPrev(commentIDText, commentText, authorText, contextText, titleText, classText):
    global index
    '''if button is clicked, display message'''
    print("Prev.")
    index += -2
    commentIDText.set(commentIDs[index])
    commentText.set(comments[index])
    authorText.set(authors[index])
    contextText.set(contexts[index])
    titleText.set(titles[index])
    classText.set(classes[index])
    index += 1

def createWindow():
    root = tk.Tk()  # create root window
    root.title("Label Comments")
    root.maxsize(900,  600)  # width x height

    # The comment information goes in this frame
    top_frame = tk.Frame(root,  width=790,  height=395,  bg='grey')
    top_frame.grid(row=0,  column=0,  padx=10,  pady=5)

    # The buttons go in this frame
    bottom_frame = tk.Frame(root,  width=790,  height=195,  bg='grey')
    bottom_frame.grid(row=1,  column=0,  padx=10,  pady=5)

    commentIDText = tk.StringVar()
    commentText = tk.StringVar()
    authorText = tk.StringVar()
    contextText = tk.StringVar()
    titleText = tk.StringVar()
    classText = tk.StringVar()

    # Buttons
    tk.Button(bottom_frame, text="PREV", command=lambda: btnPrev(commentIDText, commentText, authorText, contextText, titleText, classText)).grid(
        row=0, column=0, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Button(bottom_frame, text="SPAM", command=lambda: btnSpam(commentIDText, commentText, authorText, contextText, titleText, classText), bg='firebrick3', activebackground='firebrick1').grid(
        row=0, column=1, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Button(bottom_frame, text="HAM", command=lambda: btnHam(commentIDText, commentText, authorText, contextText, titleText, classText), bg='chartreuse4', activebackground='chartreuse3').grid(
        row=0, column=2, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Button(bottom_frame, text="NEXT", command=lambda: btnNext(commentIDText, commentText, authorText, contextText, titleText, classText)).grid(
        row=0, column=3, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')

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

    # Video Context
    context_frame = tk.Frame(top_frame)
    context_frame.grid(row=2, column=0, padx=5, pady=5)

    tk.Label(context_frame, text="Video Context:").grid(
        row=0, column=0, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Label(context_frame, textvariable=contextText, wraplength=500, justify=tk.LEFT).grid(
        row=0, column=1, padx=5,  pady=5, sticky='w'+'e'+'n'+'s')

    # Comment Author
    user_frame = tk.Frame(top_frame)
    user_frame.grid(row=3, column=0, padx=5, pady=5)

    tk.Label(user_frame, text="Username:").grid(
        row=0, column=0, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Label(user_frame, textvariable=authorText, wraplength=500, justify=tk.LEFT).grid(
        row=0, column=1, padx=5,  pady=5, sticky='w'+'e'+'n'+'s')

    # Current Label
    class_frame = tk.Frame(top_frame)
    class_frame.grid(row=4, column=0, padx=5, pady=5)

    tk.Label(class_frame, text="CURRENT CLASS:").grid(
        row=0, column=0, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Label(class_frame, textvariable=classText,
             wraplength=500, justify=tk.LEFT).grid(row=0, column=1, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')

    # Comment
    comment_frame = tk.Frame(top_frame)
    comment_frame.grid(row=5, column=0, padx=5, pady=5)

    tk.Label(comment_frame, text="Comment:").grid(
        row=0, column=0, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Label(comment_frame, textvariable=commentText,
             wraplength=500, justify=tk.LEFT).grid(row=0, column=1, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')

    root.mainloop()
    btnNext(commentIDText, commentText, authorText, contextText, titleText, classText)


if __name__ == "__main__":
    global commentIDs, comments, authors, contexts, titles
    commentIDs = []
    comments = []
    authors = []
    contexts = []
    titles = []
    classes = []
    with open(filename, mode='r', encoding='utf8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if row["class"] == "0":
                commentIDs.append(row["comment_id"])
                comments.append(row["comment"])
                authors.append(row["username"])
                titles.append(row["video_name"])
                classes.append(row["class"])
                # TODO: Add code to read contexts when thats done
                # - Probably store as video_id context pair of some form
                # - when next/prev is pressed display the context per video_id
                contexts.append("")

    createWindow()