# parse.py written for CS441 Fall '21
# Group Project: Movie Review Sentiment Analysis
__author__ = "Zach Grow" # add add'tl

import os
import string

class Parser:
	def extractWords(self, inputFile):
		# Given a *.txt (utf8, 1+ newline-separated lines) file as inputFile:
		# Build a list of lines broken at the file's newlines
		# Break that list down to a list of lines broken at sentence ends
		rawLines = []
		wordList = []
		endings = string.punctuation
		for line in inputFile:
			rawLines.append(line)
		for line in rawLines:
			wordList.append(line.lower().split())
		return wordList

	def cleanupWordList(self, inputWords):
		# Given a list of words:
		# Subtract all punctuation from all words in the list,
		# Then, remove all blanks/nonwords from list (empty vals, numbers etc),
		# Then, return the cleaned-up list of words
		# Note that the IMDB vocab file contains contractions:
		# therefore we do not strip out mid-word punctuation
		outputWords = []
		for listItem in inputWords:
			for word in listItem:
				newWord = word.strip(string.punctuation)
				if newWord != "":
					outputWords.append(newWord)
		return outputWords

