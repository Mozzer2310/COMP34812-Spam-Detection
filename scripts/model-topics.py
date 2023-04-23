import csv
import pandas as pd
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import preprocess_string, strip_punctuation,strip_numeric
import spacy
import pyLDAvis
import pyLDAvis.gensim 

# NLTK Stop words
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])


def get_comments_from_csv(file_name):
    """Retrieve comment data from a specified .csv file
    Args:
        file_name (str): .csv file name
    Returns:
        comments_by_videoid (dict): dictionary mapping from video ID to its list of comments
        video_name_dict (dict): dictionary mapping from video ID its video name
    """
    # Read CSV file
    DATA_PATH = '../data/labelled/'
    if file_name[-4:] != '.csv':
        file_name += '.csv'
    df = pd.read_csv(DATA_PATH+file_name)
    
    # Create a dictionary mapping from video_id to their comments
    comments_by_videoid = dict()
    video_name_dict = dict()
    video_ids = list(df['video_id'].unique())
    for video_id in video_ids:
        query = f"video_id=='{video_id}'"
        comments = list(df.query(query)['comment'])
        video_name = df.query(query)['video_name'].iloc[0]
        video_name_dict[video_id] = video_name
        comments.append(video_name)
        comments_by_videoid[video_id] = comments

    return comments_by_videoid, video_name_dict

def tokenize_sentences(sentences):
    """Tokenize a list of a sentences
    Args:
        sentences (list): list of sentences (str)
    Returns:
        (generator): generator object of tokenized sentences
    """
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True)) # deacc=True removes punctations

def lemmatize_bigrams(comments_bigrams, allowed_postags=['NOUN', 'ADJ']):
    """Lemmatize a list of bigrams
    Args:
        comments_bigrams (list): list of bigrams (str)
        allowed_postags (list): list of allowed part-of-speech tags
    Returns:
        lemmatized (list): list of lemmatized tokens
    """
    # run  if you don't have the en_core_web_sm model:
    # `python -m spacy download en_core_web_sm`
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

    lemmatized = []
    for comment in comments_bigrams:
        comments_all = nlp(" ".join(comment)) 
        lemmatized.append([token.lemma_ for token in comments_all if token.pos_ in allowed_postags])
    return lemmatized

def get_topics(comments_dict):
    """Retrieve a list of topic keywords
    Args:
        comments_dict (dict): dictionary mapping from video ID to its list of comments
    Returns:
        topics_dict (dict):  dictionary mapping from video ID to a list of topic keywords
    """
    topics_dict = dict()
    video_ids = comments_dict.keys()
    filters = [lambda x: x.lower(), strip_punctuation, strip_numeric]

    # Total number of keywords for a video is NUM_TOPICS * WORDS_PER_TOPIC
    NUM_TOPICS = 5
    WORDS_PER_TOPIC = 20
    
    for i,video_id in enumerate(video_ids):
        print(f"Processing {i+1}/{len(video_ids)} ({video_id})")
        # Tokenize comments
        comments_tokenized = list(tokenize_sentences(comments_dict[video_id]))
        
        # Build bigram models
        bigram = gensim.models.Phrases(comments_tokenized, min_count=5, threshold=100)
        bigram_mod = gensim.models.phrases.Phraser(bigram)
        
        # Remove stop words
        comments = [[word for word in simple_preprocess(str(comment)) if word not in stop_words] for comment in comments_tokenized]

        # Form Bigrams
        comments_bigrams = [bigram_mod[comment] for comment in comments]

        # Do lemmatization keeping only noun, adj, vb, adv
        comments_lemmatized = lemmatize_bigrams(comments_bigrams, allowed_postags=['NOUN', 'ADJ'])
        
        # Create Dictionary
        id2word = corpora.Dictionary(comments)

        # Term Document Frequency
        corpus = [id2word.doc2bow(comment) for comment in comments_lemmatized]

        # Create LDA topic model
        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                   id2word=id2word,
                                                   num_topics=NUM_TOPICS, 
                                                   random_state=100,
                                                   update_every=1,
                                                   chunksize=100,
                                                   passes=10,
                                                   alpha='auto',
                                                   per_word_topics=True)

        # Get all the topics
        lda_topics = lda_model.show_topics(num_words=WORDS_PER_TOPIC)
        topics = [preprocess_string(topic[1], filters) for topic in lda_topics]
        combined_topics = [item for topic in topics for item in topic]
        
        topics_dict[video_id] = combined_topics
        
    return topics_dict

def output_to_csv(topics_dict, video_name_dict, file_name='topics'):
    """Write topics dictionary to a .csv file
    Args:
        comments_dict (dict): dictionary mapping from video ID to its list of comments
        video_name_dict (dict):  dictionary mapping from video ID to its video name
        file_name (str): output file name
    """
    # Specify output path
    OUTPUT_PATH = '../data/'
    file_path = OUTPUT_PATH+file_name

    # Write to .csv file
    with open(f"{file_name}_topics.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["video_id", "video_name", "topic_keywords"])
        for video_id in topics_dict.keys():
            writer.writerow([video_id, video_name_dict[video_id], ','.join(topics_dict[video_id])])

if __name__ == "__main__":
    csv_filename = input("Please enter a filename for the CSV: ")     
    comments_dict, video_name_dict = get_comments_from_csv(csv_filename)
    topics_dict = get_topics(comments_dict)
    output_to_csv(topics_dict, video_name_dict, file_name=csv_filename)


