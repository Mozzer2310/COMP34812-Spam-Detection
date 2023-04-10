import tkinter as tk

comments = ["comment1", "comment2", "comment3"]
authors = ["author1", "author2", "author3"]
contexts = ["1", "1", "2"]
titles = ["title1", "title1", "title2"]
index = 0

def btnHam():
    '''if button is clicked, display message'''
    print("Ham.")


def btnSpam():
    '''if button is clicked, display message'''
    print("Spam.")

def btnNext(commentText, authorText, contextText, titleText):
    global index
    '''if button is clicked, display message'''
    print("Next.")
    commentText.set(comments[index])
    authorText.set(authors[index])
    contextText.set(contexts[index])
    titleText.set(titles[index])
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

    commentText = tk.StringVar()
    authorText = tk.StringVar()
    contextText = tk.StringVar()
    titleText = tk.StringVar()

    # Buttons
    tk.Button(bottom_frame, text="SPAM", command=btnSpam, bg='firebrick3', activebackground='firebrick1').grid(
        row=0, column=0, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Button(bottom_frame, text="HAM", command=btnHam, bg='chartreuse4', activebackground='chartreuse3').grid(
        row=0, column=1, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Button(bottom_frame, text="NEXT", command=lambda: btnNext(commentText, authorText, contextText, titleText)).grid(
        row=0, column=2, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')

    # Comment Information
    # Video Title
    title_frame = tk.Frame(top_frame)
    title_frame.grid(row=0, column=0, padx=5, pady=5)

    tk.Label(title_frame, text="Video Title:").grid(
        row=0, column=0, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Label(title_frame, textvariable=titleText, wraplength=500, justify=tk.LEFT).grid(
        row=0, column=1, padx=5,  pady=5, sticky='w'+'e'+'n'+'s')

    # Video Context
    context_frame = tk.Frame(top_frame)
    context_frame.grid(row=1, column=0, padx=5, pady=5)

    tk.Label(context_frame, text="Video Context:").grid(
        row=0, column=0, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Label(context_frame, textvariable=contextText, wraplength=500, justify=tk.LEFT).grid(
        row=0, column=1, padx=5,  pady=5, sticky='w'+'e'+'n'+'s')

    # Comment Author
    user_frame = tk.Frame(top_frame)
    user_frame.grid(row=2, column=0, padx=5, pady=5)

    tk.Label(user_frame, text="Username:").grid(
        row=0, column=0, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Label(user_frame, textvariable=authorText, wraplength=500, justify=tk.LEFT).grid(
        row=0, column=1, padx=5,  pady=5, sticky='w'+'e'+'n'+'s')

    # Comment
    comment_frame = tk.Frame(top_frame)
    comment_frame.grid(row=3, column=0, padx=5, pady=5)

    tk.Label(comment_frame, text="Comment:").grid(
        row=0, column=0, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
    tk.Label(comment_frame, textvariable=commentText,
             wraplength=500, justify=tk.LEFT).grid(row=0, column=1, padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')

    root.mainloop()


if __name__ == "__main__":
    createWindow()
