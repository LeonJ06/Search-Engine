
import math
import re
from urlparse import urlparse

hm = dict()
googleNum = 0
idcglist=[]


def searchGoogle(query, number):
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")
    result = list()
    for i in search(query+" site:ics.uci.edu", tld='com', lang='en', num=number, start=0, stop=number, pause=2.0):
        l = str(i)
        parsed = urlparse(l)
        if not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                         + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                         + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                         + "|thmx|mso|arff|rtf|jar|csv" \
                         + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):
            l = l.split("//")
            result.append(l[1])
    return result

    #query = 'machine learning site:ics.uci.edu'
    #number = 50
    #result = searchGoogle(query,number)
    #print len(result)


def googleScore(googleLink):
    global googleNum
    global hm
    if (len(googleLink) > 50):
        googleLink = googleLink[0:50]
    googleNum = len(googleLink)
    reset = len(googleLink) / 5
    lvl = len(googleLink) / 5
    score = 5
    for l in googleLink :
        #print score
        hm[l] = 2**score - 1
        #hm[l] = score
        lvl = lvl-1
        if lvl==0:
            score = score-1
            if score<0:
               score=0
            lvl = reset


def dcg(myRes):
    global googleNum
    global idcglist
    if googleNum>len(myRes):
        googleNum = len(myRes)
    print googleNum
    global hm
    print hm
    res = 0
    for i in range(0,googleNum):
        print myRes[i]
        url = myRes[i].replace("'", "")
        if hm.has_key(url):
            res = res + float(hm[url]) / math.log(i+2,2)
            idcglist.append(float(hm[url]))
        if hm.has_key(url+"/"):
            res = res + float(hm[url+"/"]) / math.log(i+2,2)
            idcglist.append(float(hm[url+"/"]))
    return res

def idcg():
    global idcglist
    res = 0.00000000000001
    idcglist.sort(reverse=True)
    for i in range(len(idcglist)):
        res = res + idcglist[i] / math.log(i + 2, 2)

    return res





def main(query, myRes):
    global hm,googleNum,idcglist
    googleScore(searchGoogle(query,len(myRes)))
    res = dcg(myRes)/idcg()
    hm.clear()
    googleNum = 0
    idcglist = []
    return res
