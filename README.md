# COMP34812-Spam-Detection
The implementation for the project outlined in the proposal:

[A BERT Approach to YouTube Comment Spam Detection as a PairwiseSequence Classification Task](https://github.com/Mozzer2310/COMP34812-Spam-Detection/blob/main/pdfs/NLU_proposal.pdf)

## Data
We created our own dataset for the task, using the method proposed in our proposal. One **revision** we made from our proposal was the inclusion of another class for the comments, this class was the 'neutral' class. This represents when a comment does not contain content relevant to the video but is not harmful. The different classes and their definitions for labelling are defined in the [data/labelled README](data/labelled/README.md).

### Comments
Our data was gathered by ourselves making use of the [YouTube Data API](https://developers.google.com/youtube/v3). We wrote scripts to retrieve the YouTube comments, and store the information needed as `csv` files. The relevant scripts are detailed in the [script README](scripts/README.md), and the videos selected as well as the labelling process is explained in the [data/comments README](data/comments/README.md) and the [data README](data/README.md).

### Context
<!-- Explain what the context/topic modelling any deviations from the proposal does -->

## Model/Network
<!-- Explain the general model, any deviations from the proposal -->

## Showcase
<!-- Explain what the demo is, and its purpose -->
The showcase loads our pretrained model, allowing a user to provide example data for a specified YouTube video, so that the model can make predictions in real-time and classify the user provided examples.

## Achievements
<!-- Short overview of the achievement of the project -->
