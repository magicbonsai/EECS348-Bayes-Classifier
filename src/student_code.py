from __future__ import print_function
import math

class Bayes_Classifier:
	
	# Alex Zhu, EECS 348, Winter 2018
	# Stemming and Neutral Words methods should be in both Train and Classify
	# Currently this implementation tries to increase accuracy with Neutral word trimming,
	# Simple Porter Stemming, and removal of punctuation and spaces. 
	# Current scores from given data is 0.93, ratio of positive to negative scores is similar
	# to ratio of false positive to false negative scores.  

    def __init__(self):
	#print('init')
	# predict - the return array of scores
	# positive - the dictionary of positive words
	# negative - the dictionary of negative words
	# neutral - the array of neutral words to ignore
	# probgood - the probability a review is good based on total num of reviews
	# numpos - number of positive reviews
	# numneg - number of negative reviews
	global predict 
	global positive
	global negative
	global neutral
	global probgood
	global numpos
	global numneg
	global punc
	self.predict = []
	self.positive = dict()
	self.negative = dict()
	self.neutral = ['!','"','#','&','(',')','*',',','-','--','.','/','1','10','2',
			'20','3','4','5',':',';','?','a',
			'about',"after","again","along","also",'all','an','and','are','as',
			"acting","action","actor","actors","actually","almost","always","am",
			'at','bad','be','because','but','by','can','could','even', 
			'ever','film','first','for','from',"films","find",
			'get','good','had','has','have','he','his','i',
			"i'm","i've","it's","its","job","john","kids",
                        "long","look","lot","makes","man","many","may","mind",
			"most","much","music",'if','in','is','it', "must","never",
			"new","now","off","old","once","other","our","out","over","own","part",
			"  it's",'just','like','made','make','me','more','movie','movies',
			'my','no','not','of','on','one','only','or','out  ',
			'people','plot','really','see','seen','so','some',
			'than','that','the','there','they','this','time',
			'  to','up','very','was','were','what','when','who','with',
			"well","went","where","which","while","whole","why","will",
			'would','you','young','your']
	# Yes I'm lazy and didn't bother to merge these two togther.  Bite me.
	self.stopwords = [ 'a','about','above','after','again','against','all','am','an','and',
                           'any','are','arent','as','at','be','because','been','before','being',
                           'below','between','both','but','by','cant','cannot','could','couldnt',
                           'did','didnt','do','does','doesnt','doing','dont','down','during','each',
                           'few','for','from','further','had','hadnt','has','hasnt','have','havent',
                           'having','he','hed','hell','hes','her','here','heres','hers','herself',
                           'him','himself','his','how','hows','i','id','ill','im','ive','if','in',
                           'into','is','isnt','it','its','its','itself','lets','me','more','most',
                           'mustnt','my','myself','no','nor','not','of','off','on','once','only',
                           'or','other','ought','our','ours','ourselves','out','over','own',
                           'same','shant','she','shed','shell','shes','should','shouldnt','so',
                           'some','such','than','that','thats','the','their','theirs','them',
                           'themselves','then','there','theres','these','they','theyd','theyll',
                           'theyre','theyve','this','those','through','to','too',
                           'under','until','up','very','was','wasnt','we','wed','well','were',
                           'weve','were','werent','what','whats','when','whens','where',
                           'wheres','which','while','who','whos','whom','why','whys','with',
                           'wont','would','wouldnt','you','youd','youll','youre','youve','your',
                           'yours','yourself','yourselves' ]
	self.probgood = 0
	self.numpos = 0
	self.numneg = 0
    def dumbStem(self, word):
	#print('Not implemented yet')
	word_orig = word
	if len(word) > 2:
		#print('Run algo on word.')
		#print(word)
		temp = word
		#First step of porter algorithm
                if len(word) > 5 and word[-4:] == 'sses':
                    word = word[:-2]
                elif len(word) > 4 and word[-3:] == 'ies':
            	   word = word[:-2] + 's'
                elif len(word) > 2 and word[-1:] == 's':
            	   word = word[:-1]

		#second step of Porter
                if len(word) > 5 and word[-3:] == 'eed':
                    word = word[:-1]
                elif len(word) > 4 and word[-2:] == 'ed':
                    word = word[:-2]
                elif len(word) > 5 and word[-3:] == 'ing':
                    word = word[:-3]

		#print(word)

                #if word_orig != word:
                    #print( 'dumbStem ' + word_orig + ' -> ' + word )
	return word
	
    def remove_spaces(self, word):
	#Will attempt to expand to include punctuation, just apostrophes.
	#for i in range(0, len(word)):
		#if word[i] == ' ':
			#word = word[:i]+ word[i+1:]
	word.replace(" ", "")
	word.replace("'", "")
	return word

    def train(self,filename):
	
	#print('not implemented yet')
	# code to be completed by students to extract features from training file, and
	# to train naive bayes classifier.
	# Assign frequencies in dictionary where keywoard = word
	# lowercase everything
	# neutral words ignore / add to both dictionaries
	# remove puncuation
	# positive['example'] = 3
	# positive.update('word' = 1)
	# positive['word'] = 1 ;  updates word otherwise adds word with mag 1
	# sampledict['newword'] = 1
	# if 'word' in dict { true or false }
	# stop words - punctuation 
	# stem 
	# td idf
	 
	
	self.numpos = 0
	self.numneg = 0
	self.positive = dict()
	self.negative = dict()
	self.probgood = 0
			
	with open(filename, 'rt') as f:
		lines = f.readlines()	
	
	for line in lines:
		line = line.replace('\n', '')
		fields = line.split('|')
		wID = int(fields[0])
		review = fields[1]
		words = fields[2].lower()		
		if fields[1] == '5':
			self.numpos += 1
		else:
			self.numneg += 1

		for word in words.split():
			word = self.remove_spaces(word)
			word = self.dumbStem(word)
			if word not in self.neutral and word not in self.stopwords: 
				if fields[1] == '5':
					#if word in self.positive and word not in self.neutral2:
					if word in self.positive:
						self.positive[word] += 1
			 		else:
						self.positive[word] = 1
				else:
					#if word in self.negative and word not in self.neutral:	
					if word in self.negative:
							self.negative[word] += 1
					else:
							self.negative[word] = 1
		self.probgood = (self.numpos / float(self.numpos + self.numneg))
			#review over total reviews	
	
	
	#print (self.probgood)
	#for w , f in sorted(self.positive.items()):
		#if f < 75 and f > 50 :
			#print('"' + w + '"'+ ',',  end = '')
	print('')
    def classify(self,filename):
	#print('not implemented yet')
	# code to be completed by student to classifier reviews in file using naive bayes
	# classifier previously trains.  member function must return a list of predicted
	# classes with '5' = positive and '1' = negative
	# given freq of word / all words in positive/negative dictionary = prob
	# mult all given probs of words in line = pos/neg prob - is pos or neg based on magnitude
	# 5 or 1 add to predict[]
	#print(len(self.positive))
	#print(len(self.negative))
	prob = self.probgood   
	posreviews = self.numpos
	negreviews = self.numneg 

	with open(filename, 'rt') as f:
		lines = f.readlines()
	
	for line in lines:
		line = line.replace('\n', '')
		fields = line.split('|')
		wID = int(fields[0]) 
		review = fields[1]
		words = fields[2].lower()
		tpg = math.log(prob)
		tpb= math.log(1 - prob)	
		for word in words.split():
			word = self.remove_spaces(word)
			word = self.dumbStem(word)
			if word not in self.neutral and word not in self.stopwords:
				#if word in self.positive and word not in self.neutral2:
				if word in self.positive: 
					pg = math.log((self.positive[word]+1)/float(posreviews + len(self.positive)))	
				else:
					pg = math.log( 1 / float( posreviews + len(self.positive)))
				tpg += pg
				
				#if word in self.negative and word not in self.neutral: 
				if word in self.negative:
					pb = math.log((self.negative[word]+1)/float(negreviews + len(self.negative)))
				else:
					pb = math.log(1 / float(negreviews+len(self.negative)))
				tpb += pb	
		if tpg > tpb:
			self.predict.append('5')
			#print(self.predict[-1])
		else:
			self.predict.append('1')
			#print(self.predict[-1])
	
	return self.predict
