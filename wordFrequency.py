import re
import json
import nltk

def getFreqDistribution(filename):
	f = open(filename,'r')
	base = defaultdict(int)
	count = 0
	for line in f:
		count += 1
		tweet = json.loads(line)
		for word in tweet:
			if word.startswith('@') or word.startswith('#'):
				base[word[1:]]+=1
			else
				base[word]+=1
		print count
	return base