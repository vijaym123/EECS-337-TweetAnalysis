import nltk
import json
import time
from collections import defaultdict
from matplotlib import pyplot as plt

def bigrams(words):
    wprev = None
    for w in words:
    	if wprev!=None:
	        yield (wprev, w)
        wprev = w

def visuize():
	stepSize = 5000
	filename = "goldenglobes-processedTweets.json"
	count = 0
	f = open(filename,"r")
	tweetsData = defaultdict(int)
	for line in f:
		count = count + 1
		if count%stepSize < stepSize:
			data = json.loads(line)
			for word in data:
				tweetsData[word] += 1
		if count%stepSize == 0:
			solution = sorted([(tweetsData[key],key)for key in tweetsData.keys()],reverse=True)
			print "In ",str((count%stepSize)),count,"chunk, people are talking about: ", solution[4:10]
			tweetsData = defaultdict(int)


def mostTweetedPeriod(filename,tags,splits):
	f = open(filename,'r')
	freqDict = defaultdict(int)
	#print filename,tags
	buildList = []
	count = 0
	for line in f:
		count = count + 1	
		tweet = json.loads(line)
		if len(tweet)>=2 and all(any(e in word for word in tweet) for e in tags):
			buildList.append(1)
			bigramList = bigrams(tweet)
			for i in bigramList:
				freqDict[i[0]+" "+i[1]] += 1
		else:
			buildList.append(0)
	return splitBuildList(buildList,splits)

def splitBuildList(list1,splits):
	histogram = []
	count = 0
	while count < len(list1):
		sum1 = 0
		for i in range(splits):
			if count >= len(list1):
				break
			sum1 = sum1 + list1[count]
			count = count + 1
		histogram.append(sum1)
	return histogram

if __name__ == "__main__":
	filename = "goldenglobes-processedTweets.json"
	question = ["best actress comedy", "best director","best actor comedy", "best picture comedy", "best actor drama","best actress drama", "best picture drama"]

	porter = nltk.PorterStemmer()
	for q in question:
		tags = [porter.stem(i) for i in q.split()]
		Y=mostTweetedPeriod(filename,tags,800)
		X = range(0,len(Y))
		plt.bar(X,Y)
		plt.ylabel("Number of tweets related to query")
		plt.xlabel("Tweets")
		plt.title(q)
		plt.show()