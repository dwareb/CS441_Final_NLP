#!/usr/bin/env python3
__author__ = "Zach Grow, Matthew Twete"  # add your name

# Import libraries
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense


# takes an opened file, reads each line and inputs it into an array.
def import_to_array(in_file):
    review_set = []
    for l in in_file:
        if l != "\n":
            review_set.append(l.rstrip().split())
    return review_set


def main():
    # Open the files containing the positive and negative reviews for the test and training sets
    # they will already be tokenized and have a vocabulary size of 5000. Read the file contents into
    # arrays.

    # Get the positive training reviews
    w = open("pos_train", "r")
    pos_train = import_to_array(w)
    w.close()
    # Get the negative training reviews
    w = open("neg_train", "r")
    neg_train = import_to_array(w)
    w.close()
    # Get the positive test reviews
    w = open("pos_test", "r")
    pos_test = import_to_array(w)
    w.close()
    # Get the negative test reviews
    w = open("neg_test", "r")
    neg_test = import_to_array(w)
    w.close()

    # Create the test set label array, and merge the negative and positive test reviews into a single array
    yTesting = np.concatenate((np.ones(len(pos_test)), np.zeros(len(neg_test))))
    xTesting = np.concatenate((pos_test, neg_test), dtype=object)
    # Create the training set label array, and merge the negative and positive test reviews into a single array
    yTraining = np.concatenate((np.ones(len(pos_train)), np.zeros(len(neg_train))))
    xTraining = np.concatenate((pos_train, neg_train), dtype=object)

    # Create a random order to shuffle the data for the test and training sets
    train = np.random.permutation(len(xTraining))
    test = np.random.permutation(len(xTesting))
    # Randomly shuffle the test and training sets
    yTesting = yTesting[test]
    xTesting = xTesting[test]
    yTraining = yTesting[train]
    xTraining = xTesting[train]

    # Pad the reviews to make sure they have a length of 500
    maxWords = 500
    xTraining = sequence.pad_sequences(xTraining, maxlen=maxWords)
    xTesting = sequence.pad_sequences(xTesting, maxlen=maxWords)

    # Set up the actual RNN model
    # Set the embedding layer size to 32
    embeddingSize = 32
    # Vocabulary size
    vocabSize = 5000
    # Number of epochs to train a model on for each batch size
    epochs = [3,4,5]
    # Batch sizes to train a model on for each number of epoch
    batch_sizes = [32,64,128]
    # Loop over the batch sizes and epochs and train a model with those hyper-paramters
    # then test the model on the test set and print out the results
    for batch in batch_sizes:
        for ep in epochs:
            # Create the network
            model = Sequential()
            # Add a embedding layer, LSTM layer with 100 nodes and a dense output layer
            model.add(Embedding(vocabSize, embeddingSize, input_length=maxWords))
            model.add(LSTM(100))
            model.add(Dense(1, activation='sigmoid'))
            # Compile the model using the adam optimizer and with binary cross-entropy for the loss
            # and when evaluating the model use accuracy, precision and recall as the metrics
            model.compile(loss='binary_crossentropy',
                           optimizer='adam',
                           metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()])

            # Set the batch size and number of epochs to train for
            batchSize = batch
            numEpochs = ep

            # Separate out the validation set, which will have a size equal to the batch size
            # Since the batch sizes are small the removal of the data points from the training
            # set will not have a significant impact on the model
            xValid, yValid = xTraining[:batchSize], yTraining[:batchSize]
            xTraining2, yTraining2 = xTraining[batchSize:], yTraining[batchSize:]

            # Train the model on the training data
            model.fit(xTraining2, yTraining2, validation_data=(xValid, yValid),
                      batch_size=batchSize, epochs=numEpochs)

            # Test the model's performance on the test set
            scores = model.evaluate(xTesting, yTesting, verbose=0)

            # Print out the model batch size and number of epochs trained for along with
            # the overall accuracy, precision and recall
            print("Model trained with a batch size of ", batchSize, " for ", numEpochs, " epochs.")
            print("Model overall accuracy: ", scores[1])
            print("Model precision: ", scores[2])
            print("Model recall: ", scores[3])



if __name__ == '__main__':
    main()
