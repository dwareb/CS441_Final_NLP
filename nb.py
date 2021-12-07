#CS441 Final Project, Movie review Sentiment analysis.
#Naive Bayes version
__author__ = "Michael Fulton, Cera Oh, Matthew Twete, Zach Grow"

#Need OS for file input.
import os, math


#Get the totals of words in each training data pos and negative.
def word_likelihood(process_func, get_vocab_dict_func):
    pos_count = 0
    neg_count = 0
    pos_total = get_vocab_dict_func()
    neg_total = get_vocab_dict_func()
    pos_files = os.scandir(path='./mrdb/train/pos/')
    neg_files = os.scandir(path='./mrdb/train/neg/')

    #Add frequency of each word in each file
    for p in pos_files:
        f = open(p.path, "r", encoding="utf8")
        pos_count = process_func(f,pos_total,pos_count)
        f.close()


    #calculate for the liklihood of each word. Adding one for each value in the dict because there was a default 1 for each
    for i in pos_total:
        pos_total[i] /= (pos_count + len(pos_total))

    #Add frequency of each word in each file
    for n in neg_files:
        neg_count += 1
        f = open(n.path, "r", encoding="utf8")
        neg_count = process_func(f,neg_total,neg_count)
        f.close()

    #calculate for the liklihood of each word. Adding one for each value in the dict because there was a default 1 for each
    for i in neg_total:
        neg_total[i] /= (neg_count + len(neg_total))

    return [pos_total,neg_total]




def evaluate_reviews(likelihoods, predict_func):
    pos_files = os.scandir(path='./mrdb/test/pos/')
    neg_files = os.scandir(path='./mrdb/test/neg/')

    correct_pos = 0
    incorrect_pos = 0

    #Predict outcome for each positive review
    for p in pos_files:
        f = open(p.path, "r", encoding="utf8")
        result = predict_func(f,likelihoods)
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
        result = predict_func(f,likelihoods)
        if result == 0:
            correct_neg += 1
        else:
            incorrect_neg += 1
        f.close()

    neg_percent = correct_neg / (correct_neg + incorrect_neg)
    overall = (correct_pos + correct_neg) / (correct_pos + correct_neg + incorrect_neg + incorrect_pos)

    return [pos_percent, neg_percent, overall]


#Get every word in the dictonary and set it to 1, only consider max_words of words
def get_vocab_dict_limited(max_words = 3000):
    vocab_file = open("./mrdb/imdb.vocab", "r", encoding="utf8")
    vocab = {}
    counter = 0
    for w in vocab_file:
        if counter < max_words:
            vocab[w.rstrip()] = 1
            counter += 1
        else:
            vocab_file.close()
            return vocab
    vocab_file.close()
    return vocab

#Get every word in the dictonary and set it to 1, ignore first skip_words words
def get_vocab_dict_ignore_first(skip_words = 40):
    vocab_file = open("./mrdb/imdb.vocab", "r", encoding="utf8")
    vocab = {}
    counter = 0
    for w in vocab_file:
        if counter > skip_words:
            vocab[w.rstrip()] = 1
            counter += 1
        else:
            counter += 1
    vocab_file.close()
    return vocab

#Get every word in the dictonary and set it to 1, only consider max_words of words
def get_vocab_dict_limit_both(max_words = 3000, skip_words = 40):
    vocab_file = open("./mrdb/imdb.vocab", "r", encoding="utf8")
    vocab = {}
    counter = 0
    counter2 = 0
    for w in vocab_file:
        if counter < max_words:
            if counter > skip_words:
                vocab[w.rstrip()] = 1
                counter += 1
            else:
                counter += 1
        else:
            vocab_file.close()
            return vocab
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

#Takes a file, a vocabulary dict, and returns the vocab dict with word frequency added to it but double the weight for last 15 words
def nb_process_file_weight_end(infile,vocab,count):
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
        for w in line[-15:]:
            #Try block, in case word isn't in the vocab
            try:
                vocab[str(w)] += 2
                count += 2
            except:
                pass
    return count

#__TODO__ In process. Need to make this return a list of words in the line. Essentially strip out punctuation, and split words into their own item.
def process_line(line, exclude):
    line = line.translate(exclude).replace("!"," ! ").replace("?"," ? ")
    return line.lower().split()

def predict_weight_end(review, freq):
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
        for w in line[-15:]:
            try:
                #log is taken to prevent underflow
                pos += math.log(freq[0][str(w)])*2
                neg += math.log(freq[1][str(w)])*2
            except:
                pass
    if pos > neg:
        return 1
    return 0

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
    #likelihoods = word_likelihood(nb_process_file, get_vocab_dict_1)
    #results = evaluate_reviews(likelihoods, predict)
    #print("Accuracy results:\nPositive: " + str(results[0]) + "\nNegative: " + str(results[1]) + "\nOverall: " + str(results[2]))

    #likelihoods = word_likelihood(nb_process_file_weight_end, get_vocab_dict_1)
    #results = evaluate_reviews(likelihoods, predict_weight_end)
    #print("Accuracy results:\nPositive: " + str(results[0]) + "\nNegative: " + str(results[1]) + "\nOverall: " + str(results[2]))

    #likelihoods = word_likelihood(nb_process_file, get_vocab_dict_limited)
    #results = evaluate_reviews(likelihoods, predict_weight_end)
    #print("Accuracy results:\nPositive: " + str(results[0]) + "\nNegative: " + str(results[1]) + "\nOverall: " + str(results[2]))

    #likelihoods = word_likelihood(nb_process_file_weight_end, get_vocab_dict_limited)
    #results = evaluate_reviews(likelihoods, predict_weight_end)
    #print("Accuracy results:\nPositive: " + str(results[0]) + "\nNegative: " + str(results[1]) + "\nOverall: " + str(results[2]))

    likelihoods = word_likelihood(nb_process_file, get_vocab_dict_ignore_first)
    results = evaluate_reviews(likelihoods, predict)
    print("Accuracy results:\nPositive: " + str(results[0]) + "\nNegative: " + str(results[1]) + "\nOverall: " + str(results[2]))

    likelihoods = word_likelihood(nb_process_file_weight_end, get_vocab_dict_ignore_first)
    results = evaluate_reviews(likelihoods, predict)
    print("Accuracy results:\nPositive: " + str(results[0]) + "\nNegative: " + str(results[1]) + "\nOverall: " + str(results[2]))

    likelihoods = word_likelihood(nb_process_file, get_vocab_dict_limit_both)
    results = evaluate_reviews(likelihoods, predict)
    print("Accuracy results:\nPositive: " + str(results[0]) + "\nNegative: " + str(results[1]) + "\nOverall: " + str(results[2]))

    likelihoods = word_likelihood(nb_process_file_weight_end, get_vocab_dict_limit_both)
    results = evaluate_reviews(likelihoods, predict)
    print("Accuracy results:\nPositive: " + str(results[0]) + "\nNegative: " + str(results[1]) + "\nOverall: " + str(results[2]))
    

if __name__ == '__main__':
    main()
