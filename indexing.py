import re
import string
import math
import Queue
import os


# the rule for how to compare two different term, the terms which include more key word in the query will have higher
# rank, if the number of key words is same, then compare their tfidf
class ComparableObj:
    url = ""
    tfidf = 0
    count = 0

    def __init__(self, url, tfidf, count):
        self.url = url
        self.tfidf = tfidf
        self.count = count

    def __cmp__(self, other):
        if self.count > other.count:
            return True
        elif self.count < other.count:
            return False
        elif self.count == other.count:
            if self.tfidf > other.tfidf:
                return True
            else:
                return False


# process the query from the user
def search(query):
    global hm
    max = 0
    list = []
    res = []
    qwords = query.lower().split()  # get every key word in the query
    for word in qwords:             # make those key words as a list
        list.append(hm[word])       # term : [doc1], [doc2], .........
    # print list

    querysize = len(list)
    tfidfMap = dict()
    que = Queue.PriorityQueue()
    for i in range(0, querysize):
        for obj in list[i]:         # obj : [URL, line pos, tfidf]
            if not tfidfMap.has_key(obj[0]):
                tfidfMap[obj[0]] = [obj[2], 1]  # obj[2] is tf-idf, 1 means freq = 1
            else:
                tfidfMap[obj[0]] = [tfidfMap[obj[0]][0] + obj[2], tfidfMap[obj[0]][1] + 1]
                # update the map :  new tfidf                   , frequency++

    for key in tfidfMap.keys():
        que.put_nowait(ComparableObj(key, tfidfMap.get(key)[0], tfidfMap.get(key)[1]))

    length = que.qsize()
    print length
    for i in range(0, length):
        iii = que.get_nowait()
        res.append(iii.url) # query result
        if i > length - 20:
            print iii.tfidf
            print iii.count
            print "\n"
    res.reverse()           # reverse because priority que in python return the last value in que, instead of the first
    print res[0:5]          # show the top 5


# indexing the data file, store them into the map
def indexing(word, link, position, tf, filepos):
    global hm

    obj = [link, position, tf, filepos]
    if not hm.has_key(word):
        list = []
        list.append(obj)
        hm[word] = list
    else:
        hm[word].append(obj)


# update the Idf
def updateIdf(filecount):
    global hm
    for key in hm.keys():
        idf = math.log10(filecount / len(hm[key]))
        for obj in hm[key]:
            obj[2] = obj[2] * idf


# write the result into the file
def writeWord():
    writecount = 0;
    global hm
    for word in iter(hm):
        #	print word
        fileName = "C:/Users/akail/PycharmProjects/project3/Index/" + word[0] + "/"
        if not os.path.exists(fileName):
            os.makedirs(fileName)
        fileName = fileName + word[1] + ".txt"
        #	print fileName
        file = open(fileName, 'a')
        file.write(word + ', ' + str(hm[word]) + '\n')
        file.close()
        writecount = writecount + 1
        print writecount


TextFilePath = 'C:/Users/akail/PycharmProjects/project3/WEBPAGES_CLEAN/bookkeeping.tsv'
file = open(TextFilePath, 'r')
link = str()
doc = str()
hm = dict()
filecount = 0;
endcount = 0;
for doc in iter(file.readline, ''):
    endcount = endcount + 1;
    #	if endcount == 2	:
    #		break;
    tfMap = dict()  # the total number of a word in this document
    wordCount = 0  # the total number of this document
    s = doc.split()
    #	print s[0]
    testPath2 = ('C:/Users/akail/PycharmProjects/project3/WEBPAGES_CLEAN/' + s[0])
    file2 = open(testPath2, 'r');
    line2 = str()
    linePos = 0;
    for line2 in iter(file2.readline, ''):
        delset = string.punctuation
        line2 = line2.translate(None, delset)
        line2 = line2.replace("_", " ")
        wordlist = re.sub("[^\w]", " ", line2).lower().split();
        if wordlist:  # if wordlist is not null
            linePos = linePos + 1
            for word in wordlist:
                if len(word) == 1:
                    continue
                wordCount = wordCount + 1
                if tfMap.has_key(word):
                    tfMap[word][0] = tfMap[word][0] + 1
                else:
                    tfMap[word] = [1, linePos, s[0]]
                        #key : freq, linePosition, doc index
    #	print hm
    count = 0
    for word in iter(tfMap):
        tfMap[word][0] = tfMap[word][0] / float(wordCount)
        indexing(word, s[1], tfMap[word][1], tfMap[word][0], tfMap[word][2])
        count = count + 1
    filecount = filecount + 1;
    print filecount
print len(hm)

updateIdf(filecount)

#	print count
#	print hm
print "\n"
# search('machine learning')
print "\n"
# search('software engineering')
print "\n"
# search('student affairs')
print "\n"
# search('graduate courses')
print "\n"

# write the map into file
writeWord()

# print hm
print "success!"
