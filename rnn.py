#!/usr/bin/env python3
__author__ = "Zach Grow, others" #add your name

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def main():
	#model = keras.Sequential() # 1:1 i/o tensors
	#model.add(layers.Embedding(input_dim=1000, output_dim=64))
	#model.add(layers.SimpleRNN(128))
	#model.add(layers.Dense(10))
	#model.summary()
	from keras.datasets import imdb #pulls in the Stanford Large IMDB dataset
	vocabSize = 5000 #NOTE: why this vocab size?

	# Load training and testing data samples
	(xTraining, yTraining), (xTesting, yTesting) = imdb.load_data(num_words = vocabSize)
	print("Loaded dataset:\n{} training samples\n{} test samples".format(len(xTraining), len(xTesting)))
	# Set up some translation dictionaries
	# Note that the IDs are the internal values pre-assigned from the dataset
	wordToIDDict = imdb.get_word_index()
	idToWordDict = {i: word for word, i in wordToIDDict.items()}

	# Display an example of a review and a label
	print("Example label:")
	print(yTraining[2])
	print("Example review:")
	print(xTraining[2])
	print("Example review, translated:")
	print([idToWordDict.get(i, ' ') for i in xTraining[2]])
	
	# All inputs to the RNN must be of the same length
	# Therefore, we must truncate and pad any long/short inputs
	from keras.preprocessing import sequence
	maxWords = 500
	xTraining = sequence.pad_sequences(xTraining, maxlen = maxWords)
	xTesting = sequence.pad_sequences(xTesting, maxlen = maxWords)

	# Set up the actual RNN model
	from keras import Sequential
	from keras.layers import Embedding, LSTM, Dense, Dropout
	embeddingSize = 32
	model = Sequential()
	model.add(Embedding(vocabSize, embeddingSize, input_length = maxWords))
	model.add(LSTM(100))
	model.add(Dense(1, activation = 'sigmoid'))
	print(model.summary())

	# Begin training
	model.compile(loss = 'binary_crossentropy',
			optimizer = 'adam',
			metrics = ['accuracy'])
	batchSize = 64
	numEpochs = 3
	xValid, yValid = xTraining[:batchSize], yTraining[:batchSize]
	xTraining2, yTraining2 = xTraining[batchSize:], yTraining[batchSize:]
	model.fit(xTraining2, yTraining2, validation_data = (xValid, yValid),
			batch_size = batchSize, epochs = numEpochs)

	# Test the model's accuracy:
	print("Evaluating model accuracy... ", end='')
	scores = model.evaluate(xTesting, yTesting, verbose = 0)
	print(scores[1])

if __name__ == '__main__':
	main()
