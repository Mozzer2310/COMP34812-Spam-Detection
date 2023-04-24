import csv
from tempfile import NamedTemporaryFile
import shutil

fields = ["video_id", "video_name",
              "comment_id", "comment", "username", "class"]


if __name__ == "__main__":
    filename = input("Please enter the filepath and filename for the CSV: ")
    if filename[-4:] != '.csv':
        filename += '.csv'

    comment_ids = []
    comments = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        for row in reader:
            if not "." in row['comment_id']:
                if row['comment_id'] != 'comment_id':
                    comment_ids.append(row["comment_id"])
                    comments.append(row['comment'])

    tempfile = NamedTemporaryFile(mode='w', delete=False)

    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            for id in comment_ids:
                if id in row['comment_id'] and id != row["comment_id"]:
                    index = comment_ids.index(id)
                    print('updating row', row['comment_id'])
                    row['comment'] = "{" + comments[index] + "}{" + row["comment"] + "}"
            row = {'video_id': row['video_id'], 'video_name': row['video_name'], 'comment_id': row['comment_id'], 'comment': row['comment'], 'username': row['username'], 'class': row['class']}
            writer.writerow(row)

    shutil.move(tempfile.name, filename)