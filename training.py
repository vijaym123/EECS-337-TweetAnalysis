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
	pun = pun[:2]+pun[3:21]+pun[22:]
	regex=re.compile('[%s]' % re.escape(pun))
	return regex.sub(" ",stringS)

def matchScore(string1,string2):
	score = 0
	if string1 in string2:
		score = len(string1)
	elif string2 in string1:
		score = len(string2)
	return score

def long_substr(data):
    substr = ''
    if len(data) > 1 and len(data[0]) > 0:
        for i in range(len(data[0])):
            for j in range(len(data[0])-i+1):
                if j > len(substr) and all(data[0][i:i+j] in x for x in data):
                    substr = data[0][i:i+j]
    return substr

def processTweet(stringS, minlength = 2, removeStopWords=True, stemming=True):
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
			if sentenceTokens[i] in ['#', '@' ]:
				try :
					sentenceTokensFinal.append(sentenceTokens[i]+sentenceTokens[i+1])
					i = i + 1
				except IndexError:
					pass
			if removeStopWords:
				if (not (word in stopwords.words('english'))) and len(word) > minlength: 
					sentenceTokensFinal.append(word)					
			else:
				sentenceTokensFinal.append(word)
		except UnicodeEncodeError:
			pass
		i = i + 1
	return sentenceTokensFinal

def getKeywords(stringS):
	alchemyapi = AlchemyAPI()
	stringS = removeURL(stringS)
	try :
		result = alchemyapi.keywords('text',str(stringS))
	except UnicodeEncodeError:
		return []
	while result['status']!='OK':
		time.sleep(5)
		print result['status']
		result = alchemyapi.keywords('text',stringS)
	return [k['text'] for k in result['keywords']]


def preprocessing(filename, minlength = 2, removeStopWords=True, stemming=True, alchemy=False):
	f = open(filename,"r")
	fwrite = open(filename[:-5]+"-processedTweets-withoutStopwords.json",'w')
	refinedTweets = []
	count = 0
	for line in f:
		jsonObj = json.loads(line)
		if alchemy:
			print jsonObj['text'],count
			processedTweet = getKeywords(jsonObj['text'])
			print processedTweet
		else:
			processedTweet = processTweet(jsonObj['text'], minlength, removeStopWords, stemming)
		count = count + 1
		fwrite.write(json.dumps(processedTweet)+"\n")
		print count
	fwrite.close()
	return refinedTweets

if __name__ == '__main__':
	filename = "goldenglobes.json"
	preprocessing(filename,minlength=2, removeStopWords=True, stemming=False, alchemy=False)

#Best actress, Best actor, Best motion picture, Best animated film, Best supporting actress, Best director, Best screenplay, 
#Best original score, Best original song, Best TV series, Best actor in TV series, Best actress in TV series,
#Best TV/ mini series, Best actor, Best 
#Best supporting actress, Best supporting actor
#http://www.hollywoodreporter.com/race/golden-globes-2013-winners-revealed-411840
#honoured, win, big


#c21df69f3053cecc78d0f04ea1119becb69bed6d
#6d7d21f7e686a570495337175542f2ead8becb2b