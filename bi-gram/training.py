import nltk
import json
import time
from nltk.corpus import stopwords
import re
import pickle
import string

def removeURL(stringS):
	return re.sub(r"(https?\://)\S+", "", stringS)

def removePuncuations(stringS):
	pun = string.punctuation
	#pun = pun[:2]+pun[3:21]+pun[22:]
	regex=re.compile('[%s]' % re.escape(pun))
	return regex.sub(" ",stringS)

def processTweet(stringS, minlength=2, bigram=True, removeStopWords=True, stemming=True):
	lowerCaseSentence = removePuncuations(removeURL(stringS.lower()))
	sentenceTokens = nltk.word_tokenize(lowerCaseSentence)
	sentenceTokensFinal = []
	porter = nltk.PorterStemmer()
	i = 0;
	while i < len(sentenceTokens):
		try : 
			str(sentenceTokens[i]) #to remove unicode words
			if stemming:
				word = porter.stem(sentenceTokens[i])
			else: 
				word = sentenceTokens[i]
			if removeStopWords:
				if (not (word in stopwords.words('english'))) and len(word) > minlength: 
					sentenceTokensFinal.append(word)					
			elif len(word) > minlength:
				sentenceTokensFinal.append(word)
		except UnicodeEncodeError:
			pass
		i = i + 1
	return sentenceTokensFinal

def preprocessing(filename, minlength = 2 ,removeStopWords=True, stemming=True):
	f = open(filename,"r")
	fwrite = 0
	fwrite = open(filename[:-5]+"-processedTweets.json",'w')
	refinedTweets = []
	count = 0
	for line in f:
		jsonObj = json.loads(line)
		processedTweet = processTweet(jsonObj['text'], minlength, removeStopWords, stemming)
		count = count + 1
		fwrite.write(json.dumps(processedTweet)+"\n")
		print count
	fwrite.close()
	return refinedTweets

if __name__ == '__main__':
	filename = "goldenglobes.json"
	preprocessing(filename, minlength=2, removeStopWords=False, stemming=False)

#Best actress, Best actor, Best motion picture, Best animated film, Best supporting actress, Best director, Best screenplay, 
#Best original score, Best original song, Best TV series, Best actor in TV series, Best actress in TV series,
#Best TV/ mini series, Best actor, Best 
#Best supporting actress, Best supporting actor
#http://www.hollywoodreporter.com/race/golden-globes-2013-winners-revealed-411840
#honoured, win, big


#c21df69f3053cecc78d0f04ea1119becb69bed6d
#6d7d21f7e686a570495337175542f2ead8becb2b