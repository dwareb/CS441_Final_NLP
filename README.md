# CS441_Final_NLP

Natural language processing project for CS441. We use both a naive bayes with bag of words, and an RNN model for sentiment analysis on the large movie review dataset (https://ai.stanford.edu/~amaas/data/sentiment/). 

To run, unzip the mrdb, then the tar file into the directory. A path to the data from the base directory should look like this: "./mrdb/train/neg/"

Then either model can be executed by running the nb.py, or rnn.py scripts. The rnn.py script requires the preprocess.py script be run first though. Preprocessing can be used to tailor the dataset's vocabulary and review sizes.

A note on the RNN script, it requires the tensorflow library, as well as numpy.
