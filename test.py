import re
import json
import nltk
from nltk.corpus import wordnet as wn
from collections import defaultdict
import math

# def removingCommonwords(filename,freqDict):
# 	f = open(filename,'r')
# 	base = defaultdict(int)
# 	count = 0
# 	for line in f:
# 		count += 1
# 		tweet = json.loads(line)
# 		for key in freqDict:
# 			if any(key in word for word in tweet):
# 				base[key]+=1
# 		print count
# 	for word in freqDict:
# 		freqDict[word] = freqDict[word]*1.0/base[word]
# 	return freqDict

def getFreqDistribution(filename,freqDict):
	f = open(filename,'r')
	base = defaultdict(int)
	count = 0
	for line in f:
		count += 1
		tweet = json.loads(line)
		for word in tweet:
			if word.startswith('@') or word.startswith('#'):
				base[word[1:]]+=1
			else:
				base[word]+=1
		print count
	for word in freqDict:
		print len(freqDict.keys())-1/base[word]
		freqDict[word]=freqDict[word]*1.0/math.log10(len(freqDict.keys())-1/base[word])/len(freqDict.keys())
	return freqDict

def buildHistogram(filename,tags):
	f = open(filename,'r')
	freqDict = defaultdict(int)
	print filename,tags
	#porter = nltk.PorterStemmer()
	for line in f:
		tweet = json.loads(line)
		if tweet and all(any(e in word for word in tweet) for e in tags):
			print tweet
			for i in set(tweet).difference(set(tags)):
				if i.startswith('@') or i.startswith('#'):
					freqDict[i[1:]] += 3
				else:
					freqDict[i] += 1
	return getFreqDistribution(filename,freqDict)
	

def getAnswer(filename,tags):
	
	freqDict = buildHistogram(filename,tags)
	freqList = sorted([(freqDict[key],key) for key in freqDict if ],reverse=True)

	return freqList

if __name__ == "__main__":
	filename = "goldenglobes-processedTweets-withoutStopwords.json"
	question = "best dressed"
	tags = question.split()
	print getAnswer(filename,tags)[:20]

