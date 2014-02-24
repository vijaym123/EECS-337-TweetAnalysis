import re
import json
import nltk
from nltk.corpus import wordnet as wn
from collections import defaultdict
import math
from lxml import html
import requests
import sys
import unicodedata

year = raw_input("Golden Globes year: ")
pagename = "http://www.goldenglobes.com/awards/" + year


page = requests.get(pagename)
tree = html.fromstring(page.text)

winners = tree.xpath('//div[@class="views-field views-field-nominee-name gold"]/text()')
noms = tree.xpath('//div[@class="views-field views-field-nominee-name grey"]/text()')

nominees = []

for z in winners:
	nominees.append(z.replace("-"," "))
for z in noms:
	nominees.append(z.replace("-"," "))


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
 
    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)
 
    previous_row = xrange(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]

def issubstr(substr, mystr, start_index=0):
    try:
        for letter in substr:
            start_index = mystr.index(letter, start_index) + 1
        return True
    except: return False

def bigrams(words):
    wprev = None
    for w in words:
    	if wprev!=None and w != "golden" and w != "Golden" and w != "globe" and w != "Globe" and w != "globes" and w != "Globes" and w != "goldenglobes":
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
		#print count
	for word in freqDict:
		#print len(freqDict.keys())-1/base[word]
		freqDict[word]=math.log10(freqDict[word])*1.0*math.log10(len(freqDict.keys())-1/base[word])
	return freqDict

def buildHistogram(filename,tags):
	f = open(filename,'r')
	freqDict = defaultdict(int)
	#print filename,tags
	#porter = nltk.PorterStemmer()
	for line in f:
		tweet = json.loads(line)
		if len(tweet)>=2 and all(any(e in word for word in tweet) for e in tags):
			#print tweet
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

def getName(theWinner):

	minimum = 99
	best = None

	for i in nominees:
		if issubstr(theWinner.lower(), i.lower()):
			temp = levenshtein(i.lower(),theWinner.lower())
			if temp < minimum:
				best = i
				minimum = temp

	if best == None:
		firstWinner = theWinner.split()[0]
		for i in nominees:
			if issubstr(firstWinner.lower(), i.lower()):
				temp = levenshtein(i.lower(),firstWinner.lower())
				if temp < minimum:
					best = i
					minimum = temp

		firstWinner = theWinner.split()[1]
		for i in nominees:
			if issubstr(firstWinner.lower(), i.lower()):
				temp = levenshtein(i.lower(),firstWinner.lower())
				if temp < minimum:
					best = i
					minimum = temp

	if best == None:
		return theWinner
	return best


def guessWinner(results):
	return getName(results[0][1].encode('ascii', 'ignore'))

def guessSecond(results):
	return getName(results[3][1].encode('ascii', 'ignore'))

def guessNoms(results):
	print "Nominees might be: "
	print getName(results[1][1].encode('ascii', 'ignore'))
	print getName(results[2][1].encode('ascii', 'ignore'))
	print getName(results[3][1].encode('ascii', 'ignore'))
	print getName(results[4][1].encode('ascii', 'ignore'))
	return None



if __name__ == "__main__":
	filename = "goldenglobes-processedTweets.json"

	# No presenter
	question = "best picture drama"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nBest Picture - Drama: "
	temp = guessWinner(results)
	print temp
	print guessNoms(results)

	# No presenter
	question = "best actor drama"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nBest Actor - Drama: "
	temp = guessWinner(results)
	print temp
	print guessNoms(results)

	question = "best actress drama"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nBest Actress - Drama: "
	temp = guessWinner(results)
	print temp
	print guessNoms(results)

	question = "presents present " + temp.lower()
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nPresenter for Best Actress - Drama: "
	print guessWinner(results)

	# Fix
	# No presenter
	question = "best picture comedy musical"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nBest Picture - Comedy or Musical: "
	print guessWinner(results)
	print guessNoms(results)

	# No Presenter
	question = "best actor comedy"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nBest Actor - Comedy or Musical: "
	temp = guessWinner(results)
	print temp
	print guessNoms(results)

	question = "best actress comedy"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nBest Actress - Comedy or Musical: "
	print guessWinner(results)
	print guessNoms(results)

	question = "presents presenter best actress comedy musical"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nPresenter for Best Actress - Comedy or Musical: "
	print guessWinner(results)

	question = "best supporting actor"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nBest Supporting Actor: "
	temp = guessWinner(results)
	print temp
	print guessNoms(results)

	question = "presents presenter best supporting actor"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nPresenter for Best Supporting Actor: "
	print guessWinner(results)

	# No presenter
	question = "best supporting actress"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nBest Supporting Actress: "
	temp = guessWinner(results)
	print temp
	print guessNoms(results)

	question = "best director"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nBest Director: "
	print guessWinner(results)
	print guessNoms(results)

	question = "presents presenter best director"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nPresenter for Best Director: "
	print guessWinner(results)

	question = "best screenplay"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nBest Screenplay: "
	print guessWinner(results)
	print guessNoms(results)

	question = "presents present screenplay"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nPresenter for Best Screenplay: "
	print guessWinner(results)

	# No presenter
	question = "best original song"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nBest Original Song: "
	temp = guessWinner(results)
	print temp
	print guessNoms(results)

	# No presenter
	question = "best actor television series drama"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nBest Actor in a Television Series - Drama: "
	print guessWinner(results)
	print guessNoms(results)

	# No presenter
	question = "best actress television series drama"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nBest Actress in a Television Series - Drama: "
	print guessWinner(results)
	print guessNoms(results)

	# No presenter
	question = "best actor television series comedy"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nBest Actor in a Television Series - Comedy: "
	print guessWinner(results)
	print guessNoms(results)

	# No presenter
	question = "best actress performance comedy series"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nBest Actress in a Television Series - Comedy: "
	print guessWinner(results)
	print guessNoms(results)

	# No presenter
	question = "best actor miniseries"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nBest Actor - Miniseries or Television Film: "
	temp = guessWinner(results)
	print temp
	print guessNoms(results)

	# No presenter
	question = "best actress performance miniseries"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nBest Actress - Miniseries or Television Film: "
	temp = guessSecond(results)
	print temp
	print guessNoms(results)

	#Fix
	# No presenter
	question = "supporting actor television series"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nBest Supporting Actor - Miniseries or Television Film: "
	temp = guessWinner(results)
	print temp
	print guessNoms(results)

	# No presenter
	question = "best supporting actress miniseries"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:20],tags)
	print "\nBest Supporting Actress - Miniseries or Television Film: "
	temp = guessWinner(results)
	print temp
	print guessNoms(results)

	question = "host hosts"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:40],tags)
	print "\nHosts: "
	print guessWinner(results)
	print guessSecond(results)

	question = "best dress"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:40],tags)
	print "\nBest Dress: "
	print results[0][1].encode('ascii', 'ignore')


	question = "speech"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:40],tags)
	print "\nNoteworthy Speech: "
	print guessWinner(results)

	question = "awesome"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:40],tags)
	print "\nPeople Thought He/She Was Awesome: "
	print results[0][1].encode('ascii', 'ignore')

	question = "hated"
	porter = nltk.PorterStemmer()
	tags = [porter.stem(i) for i in question.split()]
	results =  filterResults(getAnswer(filename,tags)[:40],tags)
	print "\nPeople Hated: "
	print guessWinner(results)









