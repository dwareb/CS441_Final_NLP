import os, copy


#takes the open copy of the file, and inputs it into an array.
def import_to_array(in_file):
    review_set = []
    for l in in_file:
        if l != "\n":
            review_set.append(l.rstrip().split())
    return review_set

# def testing():

#     exc = "\"#$%&()*+,./:;<=>@[\]^_`{|}~"
#     blank = "                            "
#     exclude = exc.maketrans(exc,blank)
#     neg_files = os.scandir(path='./mrdb/train/neg/')
#     pos_files = os.scandir(path='./mrdb/train/pos/')
#     neg_files_test = os.scandir(path='./mrdb/test/neg/')
#     pos_files_test = os.scandir(path='./mrdb/test/pos/')
#     wordmax = 0
#     linemax = 0
#     for p in pos_files:
#         linecount = 0
#         f = open(p.path, "r", encoding="utf8")
#         for l in f:
#             linecount += 1
#             line = process_line(l, exclude)
#             if len(line) > wordmax:
#                 wordmax = len(line)
#         if linecount > linemax:
#             linemax = linecount
#         f.close()

#     for p in neg_files:
#         linecount = 0
#         f = open(p.path, "r", encoding="utf8")
#         for l in f:
#             linecount += 1
#             line = process_line(l, exclude)
#             if len(line) > wordmax:
#                 wordmax = len(line)
#         if linecount > linemax:
#             linemax = linecount
#         f.close()

#     for p in pos_files_test:
#         linecount = 0
#         f = open(p.path, "r", encoding="utf8")
#         for l in f:
#             linecount += 1
#             line = process_line(l, exclude)
#             if len(line) > wordmax:
#                 wordmax = len(line)
#         if linecount > linemax:
#             linemax = linecount
#         f.close()

#     for p in neg_files_test:
#         linecount = 0
#         f = open(p.path, "r", encoding="utf8")
#         for l in f:
#             linecount += 1
#             line = process_line(l, exclude)
#             if len(line) > wordmax:
#                 wordmax = len(line)
#         if linecount > linemax:
#             linemax = linecount
#         f.close()

#     return [wordmax, linemax]

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

def convert_files_to_arrays():
    wordmax = 500
    vocabmax = 5000
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
    # for p in pos_train_files:
    #     f = open(p.path, "r", encoding="utf8")
    #     i = 0
    #     written = 0
    #     review = []
    #     for l in f:
    #         review = process_line(l, exclude) #only includes up to wordmax
    #         while written < wordmax and i < len(review):
    #             try:
    #                 w.write(str(vocab[review[i]]) + " ")
    #                 written += 1
    #                 i += 1
    #             except:
    #                 i += 1
    #         w.write("\n")
    #     f.close()
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

def write_to_file(to_scan, write_to, wordmax, vocab):
    exc = "\"#$%&()*+,./:;<=>@[\]^_`{|}~"
    blank = "                            "
    exclude = exc.maketrans(exc,blank)
    for p in to_scan:
        f = open(p.path, "r", encoding="utf8")
        i = 0
        written = 0
        review = []
        for l in f:
            review = process_line(l, exclude) #only includes up to wordmax
            while written < wordmax and i < len(review):
                try:
                    write_to.write(str(vocab[review[i]]) + " ")
                    written += 1
                    i += 1
                except:
                    i += 1
            write_to.write("\n")
        f.close()


def process_line(line, exclude):
    line = line.translate(exclude).replace("!"," ! ").replace("?"," ? ")
    return line.lower().split()


def main():
    # result = testing()  <- Results were 2509 word max, and confirm every review is fed in a single line
    convert_files_to_arrays()


    #example of how to import one of the files:
    # w = open("pos_train", "r")
    # test = import_to_array(w)
    # w.close()

    # Validation:
    
    # print("First 20\n")
    # print(test[:20])
    # print("Last 20\n")
    # print(test[-20:])


if __name__ == "__main__":
    main()