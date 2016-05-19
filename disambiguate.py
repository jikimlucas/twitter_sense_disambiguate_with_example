import os
import json
import sys 
import twittertokenizer 
from gensim.models  import Word2Vec 
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 

reload(sys)
sys.setdefaultencoding('utf-8')
file_to_write = open(sys.argv[2],"w"); 
model = Word2Vec.load_word2vec_format(sys.argv[3], binary=False)


countries_list = open("country_example.txt","r").readline().strip().split(",")
person_list = open("person.txt","r").readline().strip().split(",")

def get_centroid_vector(list_of_words, ndim):
	# all the words should have to be in the model 
	vector = np.zeros((1,ndim))
	for word in list_of_words: 
		try:
			vector = vector + model[word].reshape(1,ndim)
		except:
			pass
	vector =  vector / float(len(list_of_words))
	return vector 

def getavgsimilarity(context_words, example_list):
	sim = 0.0
	total_pass = 0
	for word in context_words:	
		for example in example_list:
			for pos in range(0,len(word)):
				word_to_search = word[:len(word)-pos]	
				
				try: 
					#print example, word_to_search
					simx = model.similarity(word_to_search,example)					
					sim = sim + simx
					total_pass = total_pass + 1
					break
				except: 
					pass 

	return sim/(total_pass+0.00001)

def getavgsimilarity_centroid(context_words, centroid): 
	sim = 0.0
	total_pass = 0
	for word in context_words:	
		for pos in range(0,len(word)):
			word_to_search = word[:len(word)-pos]	
			#print word_to_search	
			try:
				vector = model[word_to_search]	
				vector = vector.reshape(1,200)
				simx = cosine_similarity (vector, centroid)		
				sim = sim + simx
				total_pass = total_pass + 1
			except:
			    pass 	

	return sim/(total_pass+0.00001)



def get_context_words(pos, token_list):
	# We are interested in at most four tokens 
	context_words = []
	for inpos in range (0,len(token_list)):
		if "jordan" in token_list[inpos] and inpos > pos :
			break 
		if pos==inpos: 
		   continue 
		context_words.append(token_list[inpos])
	return context_words

def	getDecision(token_list):
	centroid_country = get_centroid_vector(countries_list,200)
	centroid_person = get_centroid_vector(person_list,200)

	for pos in range(0,len(token_list)):
		if "jordan" in token_list[pos]:
			context_words = get_context_words(pos, token_list)
			avg_country = getavgsimilarity(context_words,countries_list)
			avg_person = getavgsimilarity(context_words, person_list)
			avg_country_centroid = getavgsimilarity_centroid(context_words, centroid_country)
			avg_person_centroid = getavgsimilarity_centroid(context_words, centroid_person)
			break

	context_words = ",".join(context_words)
	string_to_write  = "avg_sim_country (word) = %f and avg_sim_person (word) =%f" %(avg_country, avg_person)
	string_to_write = "Context words used=%s\n%s" %(context_words, string_to_write)
	string_to_write  = "%s\navg_sim_country (centroid) = %f and avg_sim_person (centroid) =%f "\
				%(string_to_write, avg_country_centroid, avg_person_centroid)
	return string_to_write
	
def	writeText (json_string):
	parsed_json = json.loads(json_string)
	text_to_write = parsed_json['text']
	if 	"jordan"	in	text_to_write.lower():
		file_to_write.write("Actual:"+ text_to_write+os.linesep)
		token_list = twittertokenizer.get_preprocessed_twitter_tokens(text_to_write)
		file_to_write.write("Tokens:"+(",".join(token_list)) + os.linesep)
		file_to_write.write("Decision:"+str(getDecision(token_list)) + os.linesep)
		file_to_write.write(os.linesep+"######"+os.linesep) 


def	readfile (file_):	
	with open(file_) as infile:
	    for line in infile:
	        writeText(line)
	    
readfile(sys.argv[1])

