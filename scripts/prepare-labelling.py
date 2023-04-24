import shutil

if __name__ == "__main__":
    filename = input("Please enter the filename of your .csv file from the folder: ../data/comments/: ")
    if filename[-4:] != '.csv':
        filename += '.csv'
    filename = "../data/comments/" + filename

    new_filename = filename.replace("../data/comments/", "")
    new_filename = "../data/labelled/" + new_filename.replace(".csv", "") + "-labelled.csv"


    print(f"Use this filename when prompted for a filename: {filename}\n")

    print("Running add-parent-reply.py:")
    exec(open("add-parent-reply.py").read())
    print("\nRunning add-channel-name.py:")
    exec(open("add-channel-name.py").read())
    print("\n")

    shutil.copy(filename, new_filename)
    print(f"Created new file: {new_filename}")