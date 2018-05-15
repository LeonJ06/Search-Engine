import Tkinter as tk
import re
import string
import math
import Queue
import os
import DCG
import pageRankP
import time

TextFilePath = "/Users/pengfei/Documents/Course/INFO RETRIEVAL/project 3/Index/"
def indexRetrive (query):
    res = []
    for word in query:
        #search the term in file
        first = word[0]
        second = word[1]
        posting = []

        path = TextFilePath + (first+"/"+second+".txt")
        file = open(path, 'r')

        for buf in iter(file.readline,''):

            if buf.startswith(word+","):
                buf = buf.replace("[","").replace("]","")
                buf = buf.split(", ")

                for i in range(1, len(buf)-1,4):

                    obj = []
                    obj.append(buf[i])
                    obj.append(buf[i+1])
                    obj.append(buf[i+2])
                    obj.append(buf[i+3])

                    posting.append(obj)


        res.append(posting)

    return res





class ComparableObj:
    url = ""
    tfidf = 0
    count = 0
    position = 0
    filepos = ""
    def __init__(self, url, tfidf, count, position, filepos):
        self.url = url
        self.tfidf = tfidf
        self.count = count
        self.position = position
        self.filepos = filepos

    def __cmp__(self, other):
        if self.count > other.count:
            return True
        elif self.count < other.count:
            return False
        elif self.count == other.count:
            if self.tfidf>other.tfidf:
                return True
            else:
                return False


def search(query):
    max = 0
    list = []
    res = []
    qwords = query.lower().split()
    list = indexRetrive(qwords)


    querysize = len(list)
    tfidfMap = dict()
    que = Queue.PriorityQueue()
    for i in range(0,querysize):
        for obj in list[i]:
            if not tfidfMap.has_key(obj[0]):
                tfidfMap[obj[0]] = [float(obj[2]), 1, obj[1], obj[3]] #obj[2] is tf-idf
            else:
                tfidfMap[obj[0]] = [tfidfMap[obj[0]][0] + float(obj[2]), tfidfMap[obj[0]][1]+1, obj[1], obj[3]]

    for key in tfidfMap.keys():

        que.put_nowait(ComparableObj(key, tfidfMap.get(key)[0], tfidfMap.get(key)[1], tfidfMap.get(key)[2], tfidfMap.get(key)[3]))

    length = que.qsize()

    reslist = []
    resobj = []
    for i in range(0,length):
        obj = que.get_nowait()
        resobj.append(obj.url)
        reslist.append(obj)
    resobj.reverse()
    reslist.reverse()
    reslist = reslist[1:1000]
    pList = pageRankP.main(resobj[0:min(1000,length)])
    print pList
   # print reslist
    for obj in reslist:
        obj.tfidf = obj.tfidf*0.65 + pList[obj.url]*0.35
        print 'done------------------'
    pList = reslist
    #pList = reslist


    for obj in pList:

        res.append(obj.url.replace("'", ""))
        file1 = open('/Users/pengfei/Documents/Course/INFO RETRIEVAL/project 3/WEBPAGES_CLEAN/' + obj.filepos.replace("'","").replace("\n",""), 'r')
        c = 1
        for line in iter(file1.readline, ''):
            if c == int(obj.position):
                l = line

                res.append(l)
                break
            c = c + 1
        file1.close()



    result = res[0:25]


    result.append("NDCG is: ")
    result.append(DCG.main(query, res[0:len(res):2]))


    return result





window = tk.Tk()
window.title("Baidu")
window.geometry("600x600")

e = tk.Entry(window,show=None)
e.pack()


def input_query():
    t.delete(0.0, "end")
    var=e.get()

    for i in search(var):
        t.insert("end",str(i)+"\n"+"\n")






b=tk.Button(window,text="Search",width=15,height=2,command = input_query)

b.pack()


t=tk.Text(window,height=40)
t.pack()


window.mainloop()