# COMP34812-Spam-Detection
The implementation for the project outlined in the proposal:

[A BERT Approach to YouTube Comment Spam Detection as a PairwiseSequence Classification Task](https://github.com/Mozzer2310/COMP34812-Spam-Detection/blob/main/pdfs/NLU_proposal.pdf)

## Data
We created our own dataset for the task, using the method proposed in our proposal. One **revision** we made from our proposal was the inclusion of another class for the comments, this class was the 'neutral' class. This represents when a comment does not contain content relevant to the video but is not harmful. The different classes and their definitions for labelling are defined in the [data/labelled README](data/labelled/README.md).

### Comments
Our data was gathered by ourselves making use of the [YouTube Data API](https://developers.google.com/youtube/v3). We wrote scripts to retrieve the YouTube comments, and store the information needed as `csv` files. The relevant scripts are detailed in the [script README](scripts/README.md), and the videos selected as well as the labelling process is explained in the [data/comments README](data/comments/README.md) and the [data README](data/README.md).

### Context
<!-- Explain what the context/topic modelling any deviations from the proposal does -->
We retreieved the context for each video using the Latent Dirichlet Allocation (LDA) algorithm, passing a collection of 50-100 pre-processed comments from each video as input. The algorithm produces N topics, each represented by a list of M key words, resulting in a total of N*M keywords for a single video (including duplicates). Duplicate keywords are removed from this list and extra pre-processed keywords from the video title and channel name are added the list. The resulting list is a representation of the video's context as a list of 'topic key words'. We could not account for video captions in the context as outlined in the proposal, since this would consume too many (limited) units available from the YouTube Data API for each video processed. Ultimately, we'd also considered to ignore the use of the video description as part of the context as videos would include irrelevant details to the content of the video more often than not.

## Model/Network
<!-- Explain the general model, any deviations from the proposal -->
Link to the model: https://drive.google.com/drive/folders/1pHuce6PcagUx5yLnpwqBz4XdZe1Y5lbM?usp=share_link

The model used in the implementation is created from fine-tuning DistilBERT (a smaller and faster version of the BERT model) to our custom dataset for a pair-wise sequence classification task. The two inputs to the model are: a tokenized, padded format of the comment (including username, comment and reply) and the list of topic keywords. A parsed format of the comment looks like one of the two following examples (one with no reply and one with a reply):

  * [CLS] [USER] username [MAIN] main comment [SEP] keyword1, keywordd2, keyword 3, ... [SEP] [PAD] [PAD] ...
  * [CLS] [USER] username [MAIN] main comment [REPLY] replied comment [SEP] keyword1, keyword2, keyword 3, ... [SEP] [PAD] [PAD]  ...

Custom tokens ([USER], [MAIN] and [REPLY]) were added to the pre-existing DistilBERT tokenizer in order to separate the contents of the comment. 

## Showcase
<!-- Explain what the demo is, and its purpose -->
The showcase loads our pretrained model, allowing a user to provide example data for a specified YouTube video, so that the model can make predictions in real-time and classify the user provided examples.
