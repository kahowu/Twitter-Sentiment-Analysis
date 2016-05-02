import sys
import argparse
import string
import math
import importlib

# Change cross_validation flag to True for 10-fold cross validation
cross_validation = False
feature_pkg = 'features'
demar_prefix = '<A='
demar_suffix = '>'

# Process a single tweet using a set of feature extracters
# Modular features extracters need to defined beforehand
# See the README inside "./features/" directory
def process_tweet (tweet, extracters):
	class_type = get_class (tweet[0])
	sents = tweet[1:]
	sents_processed = []
	for sent in sents:
		sent_processed = []
		if not sent:
			continue
		words = sent.split()
		for word in words:
			token, tag = word.rsplit('/', 1)
			sent_processed.append([token.lower(), tag])
		sents_processed.append(sent_processed)

	feature_vector = []
	for extracter in extracters:
		feature_vector.append(extracter.extract(sents_processed))
	feature_vector.append(class_type)

	return feature_vector

# Return tweet class given a class tag
def get_class (class_tag):
	return int(filter(str.isdigit, class_tag))

# Create data points from input training data. Set 'True' for the 3rd
# argument to prepare 10-fold cross validation training / testing sets
def create_data_points (train_fd, num_data, cross_validation=False): 
	tweets_list = [ ]
	curr_class = -1
	class_dict = {}
	COUNT = 0
	IS_RECORDING = 1
	FOLD_INDEX = 2
	line = train_fd.readline()
	while line:
		if line.startswith(demar_prefix):
			curr_class = line[line.index(demar_prefix) + 1 : line.rfind(demar_suffix)]
			if curr_class not in class_dict:
				class_dict[curr_class] = [0, True, 0] # [count, isRecording, foldIndex]

			if class_dict[curr_class][COUNT] >= num_data:
				if cross_validation:
					class_dict[curr_class][COUNT] = 0
					class_dict[curr_class][FOLD_INDEX] += 1
				else:
					class_dict[curr_class][IS_RECORDING] = False

			if class_dict[curr_class][COUNT] < num_data:
				class_dict[curr_class][COUNT] += 1
				if class_dict[curr_class][FOLD_INDEX] >= len(tweets_list):
					tweets_list.append([])
				tweets_list[class_dict[curr_class][FOLD_INDEX]].append([])


		if class_dict[curr_class][IS_RECORDING]:
			tweets_list[class_dict[curr_class][FOLD_INDEX]][-1].append(line.rstrip('\n'))

		line = train_fd.readline()

	return tweets_list

# Process all tweets 
def process_tweets (tweets, feature_extracters):
	vectors = []
	for tweet in tweets: 
		feature_vector = process_tweet (tweet, feature_extracters)
		vectors.append (feature_vector)
	return vectors

# Create arff base on feature vectors and their corresponding types
def create_arff (vectors, file_name, relation_name, vector_names, vector_types):
	arff_fd = open (file_name, 'w')
	arff_fd.write ("@RELATION " + relation_name + "\n")
	arff_fd.write ("\n")

	for i in range(len(vector_names)):
		arff_fd.write ("@ATTRIBUTE " + vector_names[i] + " " + vector_types[i] + "\n")
	arff_fd.write('@ATTRIBUTE class_type {0,4}\n')

	arff_fd.write ("\n")
	arff_fd.write ("@DATA\n")

	for vector in vectors:
		s = ",".join(str(v) for v in vector)
		arff_fd.write (s + "\n")

# Find total number of tweets given a tweet file descriptor
def find_num_tweets (twt_fd):
	count = 0
	line = twt_fd.readline() 
	types = []
	while line:
		if line.startswith(demar_prefix):
			curr_class = line[line.index(demar_prefix) + 1 : line.rfind(demar_suffix)]
			if curr_class not in types:
				types.append (curr_class)
			count += 1 
		line = train_fd.readline()

	return count / len (types)

# Load all the feature extractors and features from the configuration file 'config'
# NOTE: Please see 'config' file in the features folder  
def load_features_and_extracters():
	f = open('features/config', 'r')
	feature_names = []
	feature_extracters = []
	feature_types = []
	for line in f:
		line = line.strip()
		if line and line[0] != '#':
			words = line.split()
			feature_names.append(words[0])
			feature_types.append(words[1])
			mod = importlib.import_module(feature_pkg + '.' + words[2])
			c = getattr(mod, words[2])
			feature_extracters.append(c(*words[3:]))
	return feature_names, feature_extracters, feature_types


if __name__ == "__main__":
	# Parse input arguments 
	parser = argparse.ArgumentParser()
	parser.add_argument('twt', type=str, help='Input twt file')
	parser.add_argument('arff', type=str, help='Output arff file')
	parser.add_argument('data', nargs='?', type=int, const=0, help='Number of data points')
	args = parser.parse_args()
	train_twt = args.twt
	train_fd = open (train_twt)
	train_arff = args.arff 
	if args.data != None:
		num_data = int (args.data)
	else: 
		num_data = find_num_tweets (train_fd)
		train_fd.seek(0, 0)

	# Load feature names, extracters, and their types from the configuration file 
	# under 'features/config'
	feature_names, feature_extracters, feature_types = load_features_and_extracters()
	tweets_list = create_data_points (train_fd, int(num_data), cross_validation)
	if not cross_validation:
		feature_vectors = process_tweets (tweets_list[0], feature_extracters)
		create_arff (feature_vectors, train_arff, 'tweet', feature_names, feature_types)
	else:
		index = 0
		for i in range(len(tweets_list)):
			comb_tweets = []
			for j in range(len(tweets_list)):
				if i != j:
					comb_tweets.extend(tweets_list[j])
			feature_vectors = process_tweets (comb_tweets, feature_extracters)
			create_arff (feature_vectors, 'comb' + str(index) + '.arff', 'tweet', feature_names, feature_types)
			feature_vectors = process_tweets (tweets_list[i], feature_extracters)
			create_arff (feature_vectors, 'valid' + str(index) + '.arff', 'tweet', feature_names, feature_types)
			index += 1
