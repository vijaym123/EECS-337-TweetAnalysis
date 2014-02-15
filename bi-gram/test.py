import re
import json
import nltk
from nltk.corpus import wordnet as wn
from collections import defaultdict
import math

def bigrams(words):
    wprev = None
    for w in words:
    	if wprev!=None:
	        yield (wprev, w)
        wprev = w

def getFreqDistribution(filename,freqDict):
	f = open(filename,'r')
	base = defaultdict(int)
	count = 0
	for line in f:
		count += 1
		tweet = json.loads(line)
		for word in tweet:
			base[word]+=1
		print count
	for word in freqDict:
		print len(freqDict.keys())-1/base[word]
		freqDict[word]=math.log10(freqDict[word])*1.0*math.log10(len(freqDict.keys())-1/base[word])
	return freqDict

def buildHistogram(filename,tags):
	f = open(filename,'r')
	freqDict = defaultdict(int)
	print filename,tags
	#porter = nltk.PorterStemmer()
	for line in f:
		tweet = json.loads(line)
		if len(tweet)>=2 and all(any(e in word for word in tweet) for e in tags):
			print tweet
			bigramList = bigrams(tweet)
			for i in bigramList:
				freqDict[i[0]+" "+i[1]] += 1
	return freqDict

def getAnswer(filename,tags):
	freqDict = buildHistogram(filename,tags)
	freqList = sorted([(freqDict[key],key) for key in freqDict],reverse=True)
	return freqList

def filterResults(result,tags):
	newResult = []
	for i in result:
		if i[1].split(" ")[0] in tags or i[1].split(" ")[1] in tags:
			continue
		newResult.append(i)
	return newResult

if __name__ == "__main__":
	filename = "goldenglobes-processedTweets.json"
	question = "best presenter"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	print filterResults(getAnswer(filename,tags)[:20],tags)

