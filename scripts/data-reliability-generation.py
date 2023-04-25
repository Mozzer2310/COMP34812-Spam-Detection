import csv
import random

fields = ["video_id", "video_name", "channel_name",
              "comment_id", "comment", "username", "class"]
filepath = "../data/reliability/"

if __name__ == "__main__":
    labellers = ["sam", "tony"]
    # labellers = ["sam"]

    for labeller in labellers:
        spam = []
        ham = []
        neutral = []
        filename = "../data/labelled/" + labeller + "-dataset-labelled.csv"
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fields)
            for row in reader:
                if row['class'] == "spam":
                    spam.append(row)
                elif row['class'] == "neutral":
                    neutral.append(row)
                elif row['class'] == "ham":
                    ham.append(row)

        sampled_ham = random.sample(ham, 60)
        sampled_neutral = random.sample(neutral, 30)
        sampled_spam = random.sample(spam, 10)

        new_data = sampled_ham + sampled_neutral + sampled_spam
        random.shuffle(new_data)
        copy = labellers.copy()
        copy.remove(labeller)
        out_file = filepath + copy[0] + "-reliability.csv"
        with open(out_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            for item in new_data:
                writer.writerow({
                    "video_id": item["video_id"],
                    "video_name": item["video_name"],
                    "channel_name" : item["channel_name"],
                    "comment_id": item["comment_id"],
                    "comment": item["comment"],
                    "username": item["username"],
                    "class": 0
                })
