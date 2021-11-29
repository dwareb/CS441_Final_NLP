#CS441 Final Project, Movie review Sentiment analysis.
#Naive Bayes version
__author__ = "Michael Fulton, add others here"

#Need OS for file input.
import os, math


#Get the totals of words in each training data pos and negative.
def word_likelihood():
    pos_count = 0
    neg_count = 0
    pos_total = get_vocab_dict_1()
    neg_total = get_vocab_dict_1()
    pos_files = os.scandir(path='./mrdb/train/pos/')
    neg_files = os.scandir(path='./mrdb/train/neg/')

    #Add frequency of each word in each file
    for p in pos_files:
        f = open(p.path, "r", encoding="utf8")
        pos_count = nb_process_file(f,pos_total,pos_count)
        f.close()


    #calculate for the liklihood of each word. Adding one for each value in the dict because there was a default 1 for each
    for i in pos_total:
        pos_total[i] /= (pos_count + len(pos_total))

    #Add frequency of each word in each file
    for n in neg_files:
        neg_count += 1
        f = open(n.path, "r", encoding="utf8")
        neg_count = nb_process_file(f,neg_total,neg_count)
        f.close()

    #calculate for the liklihood of each word. Adding one for each value in the dict because there was a default 1 for each
    for i in neg_total:
        neg_total[i] /= (neg_count + len(neg_total))

    return [pos_total,neg_total]




def evaluate_reviews(likelihoods):
    pos_files = os.scandir(path='./mrdb/test/pos/')
    neg_files = os.scandir(path='./mrdb/test/neg/')

    correct_pos = 0
    incorrect_pos = 0

    #Predict outcome for each positive review
    for p in pos_files:
        f = open(p.path, "r", encoding="utf8")
        result = predict(f,likelihoods)
        if result == 1:
            correct_pos += 1
        else:
            incorrect_pos += 1
        f.close()

    pos_percent = correct_pos / (correct_pos + incorrect_pos)

    correct_neg = 0
    incorrect_neg = 0

    #Predict outcome for each negative review
    for n in neg_files:
        f = open(n.path, "r", encoding="utf8")
        result = predict(f,likelihoods)
        if result == 0:
            correct_neg += 1
        else:
            incorrect_neg += 1
        f.close()

    neg_percent = correct_neg / (correct_neg + incorrect_neg)
    overall = (correct_pos + correct_neg) / (correct_pos + correct_neg + incorrect_neg + incorrect_pos)

    return [pos_percent, neg_percent, overall]


#Get every word in the dictonary and set it to 0
def get_vocab_dict():
    vocab_file = open("./mrdb/imdb.vocab", "r", encoding="utf8")
    vocab = {}
    for w in vocab_file:
        vocab[w.rstrip()] = 0
    vocab_file.close()
    return vocab

#Get every word in the dictonary and set it to 1. Useful for NB
def get_vocab_dict_1():
    vocab_file = open("./mrdb/imdb.vocab", "r", encoding="utf8")
    vocab = {}
    for w in vocab_file:
        vocab[w.rstrip()] = 1
    vocab_file.close()
    return vocab


#Takes a file, a vocabulary dict, and returns the vocab dict with word frequency added to it.
def nb_process_file(infile,vocab,count):
    exc = "\"#$%&()*+,./:;<=>@[\]^_`{|}~"
    blank = "                            "
    exclude = exc.maketrans(exc,blank)
    for l in infile:
        #Format each line into list of words.
        line = process_line(l, exclude)
        for w in line:
            #Try block, in case word isn't in the vocab
            try:
                vocab[str(w)] += 1
                count += 1
            except:
                pass
    return count


#__TODO__ In process. Need to make this return a list of words in the line. Essentially strip out punctuation, and split words into their own item.
def process_line(line, exclude):
    line = line.translate(exclude).replace("!"," ! ").replace("?"," ? ")
    return line.lower().split()

def predict(review, freq):
    exc = "\"#$%&()*+,./:;<=>@[\]^_`{|}~"
    blank = "                            "
    exclude = exc.maketrans(exc,blank)
    pos = 1
    neg = 1
    for l in review:
        line = process_line(l, exclude)
        for w in line:
            try:
                #log is taken to prevent underflow
                pos += math.log(freq[0][str(w)])
                neg += math.log(freq[1][str(w)])
            except:
                pass
    if pos > neg:
        return 1
    return 0
    


def main():
    likelihoods = word_likelihood()
    results = evaluate_reviews(likelihoods)
    print("Accuracy resuts:\nPositive: " + str(results[0]) + "\nNegative: " + str(results[1]) + "\nOverall: " + str(results[2]))


if __name__ == '__main__':
    main()