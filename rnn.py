import os

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


def convert_files_to_arrays():
    exc = "\"#$%&()*+,./:;<=>@[\]^_`{|}~"
    blank = "                            "
    exclude = exc.maketrans(exc,blank)
    neg_files = os.scandir(path='./mrdb/train/neg/')
    pos_files = os.scandir(path='./mrdb/train/pos/')
    neg_files_test = os.scandir(path='./mrdb/test/neg/')
    pos_files_test = os.scandir(path='./mrdb/test/pos/')

    wordmax = 500
    paddin

    for p in pos_files:
        f = open(p.path, "r", encoding="utf8")
        for l in f:
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



def process_line(line, exclude):
    line = line.translate(exclude).replace("!"," ! ").replace("?"," ? ")
    return line.lower().split()


def main():
    # result = testing()  <- Results were 2509 word max, and confirm every review is fed in a single line.
    print(result)


if __name__ == "__main__":
    main()