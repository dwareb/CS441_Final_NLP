#CS441 Final Project, Movie review Sentiment analysis.
#Naive Bayes version
__author__ = "Michael Fulton, add others here"

#Need OS for file input.
import os



#Get every word in the dictonary and set it to 0
def get_vocab_dict():
    vocab_file = open("./mrdb/imdb.vocab", "r", encoding="utf8")
    vocab = {}
    for w in vocab_file:
        vocab[w.rstrip()] = 0
    return vocab

#Get every word in the dictonary and set it to 1. Useful for NB
def get_vocab_dict_1():
    vocab_file = open("./mrdb/imdb.vocab", "r", encoding="utf8")
    vocab = {}
    for w in vocab_file:
        vocab[w.rstrip()] = 1
    return vocab


#Takes a file, a vocabulary dict, and returns the vocab dict with word frequency added to it.
def nb_process_file(infile,vocab):
    for l in infile:
        line = process_line(l)
        for w in line():
            vocab[w] += 1
    return vocab


#__TODO__ In process. Need to make this return a list of words in the line. Essentially strip out punctuation, and split words into their own item.
def process_line(line):
    ln = line.split()


def main():
    voc = get_vocab_dict()
    print(voc)

if __name__ == '__main__':
    main()