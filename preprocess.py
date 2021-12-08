#Preprocessing script to convert the movie reviews into vectors, save them to files.
__author__ = "Michael Fulton, Cera Oh, Matthew Twete, Zach Grow"

import os

#takes the open copy of the file, and inputs it into an array.
def import_to_array(in_file):
    review_set = []
    for l in in_file:
        if l != "\n":
            review_set.append(l.rstrip().split())
    return review_set


#This just counts the length of the longest review, and makes sure they're all on a single line, returns the totals.
def testing():
    exc = "\"#$%&()*+,./:;<=>@[\]^_`{|}~"
    blank = "                            "
    exclude = exc.maketrans(exc,blank)
    neg_files = os.scandir(path='./mrdb/train/neg/')
    pos_files = os.scandir(path='./mrdb/train/pos/')
    neg_files_test = os.scandir(path='./mrdb/test/neg/')
    pos_files_test = os.scandir(path='./mrdb/test/pos/')
    wordmax = 0
    linemax = 0
    for p in pos_files:
        linecount = 0
        f = open(p.path, "r", encoding="utf8")
        for l in f:
            linecount += 1
            line = process_line(l, exclude)
            if len(line) > wordmax:
                wordmax = len(line)
        if linecount > linemax:
            linemax = linecount
        f.close()

    for p in neg_files:
        linecount = 0
        f = open(p.path, "r", encoding="utf8")
        for l in f:
            linecount += 1
            line = process_line(l, exclude)
            if len(line) > wordmax:
                wordmax = len(line)
        if linecount > linemax:
            linemax = linecount
        f.close()

    for p in pos_files_test:
        linecount = 0
        f = open(p.path, "r", encoding="utf8")
        for l in f:
            linecount += 1
            line = process_line(l, exclude)
            if len(line) > wordmax:
                wordmax = len(line)
        if linecount > linemax:
            linemax = linecount
        f.close()

    for p in neg_files_test:
        linecount = 0
        f = open(p.path, "r", encoding="utf8")
        for l in f:
            linecount += 1
            line = process_line(l, exclude)
            if len(line) > wordmax:
                wordmax = len(line)
        if linecount > linemax:
            linemax = linecount
        f.close()

    return [wordmax, linemax]



#creates a vocab dict for word->number association per the maximum number of words.
def vocab_dict(max):
    vocab_file = open("./mrdb/imdb.vocab", "r", encoding="utf8")
    vocab = {}
    count = 0
    for w in vocab_file:
        vocab[w.rstrip()] = count
        count += 1
        if count >= max:
            vocab_file.close()
            return vocab
    vocab_file.close()
    return vocab


#Converts all the reviews to number arrays and saves them to files.
def convert_files_to_arrays(wordmax,vocabmax):
    vocab = vocab_dict(vocabmax)
    exc = "\"#$%&()*+,./:;<=>@[\]^_`{|}~"
    blank = "                            "
    exclude = exc.maketrans(exc,blank)
    neg_train_files = os.scandir(path='./mrdb/train/neg/')
    pos_train_files = os.scandir(path='./mrdb/train/pos/')
    neg_test_files = os.scandir(path='./mrdb/test/neg/')
    pos_test_files = os.scandir(path='./mrdb/test/pos/')


    #Convert, and save to a file
    w = open("pos_train", "w")
    write_to_file(pos_train_files, w, wordmax, vocab)
    w.close()
    w = open("neg_train", "w")
    write_to_file(neg_train_files, w, wordmax, vocab)
    w.close()
    w = open("pos_test", "w")
    write_to_file(pos_test_files, w, wordmax, vocab)
    w.close()
    w = open("neg_test", "w")
    write_to_file(neg_test_files, w, wordmax, vocab)
    w.close()
    return


#This actually does the writing to each file
def write_to_file(to_scan, write_to, wordmax, vocab):

    #This bit is to define excluded characters
    exc = "\"#$%&()*+,./:;<=>@[\]^_`{|}~"
    blank = "                            "
    exclude = exc.maketrans(exc,blank)

    #process every file
    for p in to_scan:
        f = open(p.path, "r", encoding="utf8")
        i = 0
        written = 0
        review = []

        #Convert each review file into numbers, and write them to the write_to file
        for l in f:
            review = process_line(l, exclude) #only includes up to wordmax
            while written < wordmax and i < len(review):

                #This try block makes it check if its in the vocab. If it not, fail gracefully and check the next word
                try:
                    write_to.write(str(vocab[review[i]]) + " ")
                    written += 1
                    i += 1
                except:
                    i += 1

            write_to.write("\n")
        f.close()


#Returns the words in the line as an array, excluding characters contained in the exclude dict.
def process_line(line, exclude):
    line = line.translate(exclude).replace("!"," ! ").replace("?"," ? ")
    return line.lower().split()


def main():
    #Converts reviews to numbers, saves them to files.
    #Wordmax is the point at which a review gets truncated
    wordmax = 500
    #Vocabmax defines the size of the vocabulary. Most common words are included. The full vocab is around 100000 at its max.
    vocabmax = 5000
    convert_files_to_arrays(wordmax, vocabmax)


    #example of how to import one of the files:
    # w = open("pos_train", "r")
    # test = import_to_array(w)
    # w.close()

    # Validation:
    
    # print("First 20\n")
    # print(test[:20])
    # print("Last 20\n")
    # print(test[-20:])


    #####
    # result = testing()  <- Results were 2509 word max, and confirm every review is fed in a single line

if __name__ == "__main__":
    main()
