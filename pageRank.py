# this algorithm is according to https://en.wikipedia.org/wiki/PageRank
from lxml import html,etree
from urlparse import urlparse, parse_qs, urljoin
import requests
import Queue
import time
def getUrl(URL):
	try:
		r = requests.get("http://" + URL.replace(',',''))  # get the urlResponse from URL
		data = r.text           # raw data in the page
		root = html.fromstring(data)
		outputLinks = []        # store the links in this page
		base_url = URL
		for _, _, link, _ in root.iterlinks():
			url = urljoin(base_url, link).split('?')    # rebuild the relative URL
 			outputLinks.append(url[0])
 	except:
 		return []
	return outputLinks

def IO_map(inputs):    # input is query result, a list of url

    inOutMap = dict()  # url : outLinks, set(in_Links)

    # init the number of outLink for each url to 0
    for url in inputs:
        inMap = set()
        inOutMap[url] = [0, inMap]
       # print url
    for url in inputs:
        out_link = getUrl(url)  # get all links in this page
        if not out_link:
        	continue
        total_out = 0
        for out in out_link:
            if inOutMap.has_key(out):
                total_out = total_out + 1
                inOutMap[out][1].add(url.replace("'",""))   # add url to the set that is in the map
            #print out
        inOutMap[url][0] = total_out
    return inOutMap
def pageRank(urlMap, acc):
	d = 0.85
	PR = dict();#pageRank map
		# Initialization: all PR is 1/N
	#urlMap = dict()
	#urlMap[0] = [2, 4]
	#urlMap[1] = [1, 0]
	#urlMap[2] = [2, 0]
	#urlMap[3] = [1, 1, 2]
	#urlMap[4] = [1,2,3]
	# urlMap's key is url, the value is an array with first element is 
	# the outLinkNumberm, then all the elements after are all the links connects to 
	# the key
	N = len(urlMap)
	for url in urlMap:
		PR[url] =  1
	 
	while True:
		for url in urlMap:
			#print url
			oldData = PR[url]
			score = 0
			for inLink in urlMap[url][1]:
				outLinkNumber = urlMap[inLink][0]
				score = score + PR[inLink]/outLinkNumber
			PR[url] = (1-d)/N + d*score
		if PR[url] - oldData < acc: # when the difference is smaller than accuarcy, end
			break
	return PR

def main(inputs):
    urlMap = IO_map(inputs)
    res = pageRank(urlMap,0.01)
    return res

