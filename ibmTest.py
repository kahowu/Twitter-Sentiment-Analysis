# -*- coding: utf-8 -*-

# ibmTest.py
# 
# This file tests all 11 classifiers using the NLClassifier IBM Service
# previously created using ibmTrain.py
# 

import json
import subprocess
import urllib
import cPickle as pickle
import numpy as np
import os

# Retrieves a list of classifier ids from a NLClassifier service 
# an outputfile named ibmTrain#.csv (where # is n_lines_to_extract).
#
# Inputs: 
# 	username - username for the NLClassifier to be used, as a string
#
# 	password - password for the NLClassifier to be used, as a string
#
#		
# Returns:
#	a list of classifier ids as strings
#
# Error Handling:
#	This function should throw an exception if the classifiers call fails for any reason
#
def get_classifier_ids(username,password):
	cmd = r'curl -u "' + username + r'":"' + password + r'" "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers" 2>/dev/null'
	output = json.loads(subprocess.check_output(cmd, shell=True))
	if 'error' in output:
		raise Exception(output['error'] + " - " + output['description'])
		return
	id_list = []
	for classifier in output['classifiers']:
		 id_list.append(classifier['classifier_id'])
	return id_list	

# Asserts all classifiers in the classifier_id_list are 'Available' 
#
# Inputs: 
# 	username - username for the NLClassifier to be used, as a string
#
# 	password - password for the NLClassifier to be used, as a string
#
#	classifier_id_list - a list of classifier ids as strings
#		
# Returns:
#	None
#
# Error Handling:
#	This function should throw an exception if the classifiers call fails for any reason AND 
#	It should throw an error if any classifier is NOT 'Available'
#
def assert_all_classifiers_are_available(username, password, classifier_id_list):
	for classifier_id in classifier_id_list:
		cmd = r'curl -u "' + username + r'":"' + password + r'" "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/' + classifier_id + r'" 2>/dev/null'
		output = json.loads(subprocess.check_output(cmd, shell=True))
		if 'error' in output:
			raise Exception(output['error'] + " - " + output['description'])
		if 'status' in output and output['status'] != 'Available':
			raise Exception(output['status_description'])	
	return

# Classifies a given text using a single classifier from an NLClassifier 
# service
#
# Inputs: 
# 	username - username for the NLClassifier to be used, as a string
#
# 	password - password for the NLClassifier to be used, as a string
#
#	classifier_id - a classifier id, as a string
#		
#	text - a string of text to be classified, not UTF-8 encoded
#		ex. "Oh, look a tweet!"
#
# Returns:
#	A "classification". Aka: 
#	a dictionary containing the top_class and the confidences of all the possible classes 
#	Format example:
#		{'top_class': 'class_name',
#		 'classes': [
#					  {'class_name': 'myclass', 'confidence': 0.999} ,
#					  {'class_name': 'myclass2', 'confidence': 0.001}
#					]
#		}
#
# Error Handling:
#	This function should throw an exception if the classify call fails for any reason 
#
def classify_single_text (username, password, classifier_id,text):
	cmd = r'curl -u "' + username + r'":"' + password + r'" "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/' + classifier_id + '/classify?text=' + text + r'" 2>/dev/null'
	output = json.loads(subprocess.check_output(cmd, shell=True))
	if 'error' in output:
		raise Exception(output['error'] + " - " + output['description'])
	return output

# Classifies all texts in an input csv file using all classifiers for a given NLClassifier
# service.
#
# Inputs:
#       username - username for the NLClassifier to be used, as a string
#
#       password - password for the NLClassifier to be used, as a string
#      
#       input_csv_name - full path and name of an input csv file in the 
#              6 column format of the input test/training files
#
# Returns:
#       A dictionary of lists of "classifications".
#       Each dictionary key is the name of a classifier.
#       Each dictionary value is a list of "classifications" where a
#       "classification" is in the same format as returned by
#       classify_single_text.
#       Each element in the main dictionary is:
#       A list of dictionaries, one for each text, in order of lines in the
#       input file. Each element is a dictionary containing the top_class
#       and the confidences of all the possible classes (ie the same
#       format as returned by classify_single_text)
#       Format example:
#              {‘classifiername’:
#                      [
#                              {'top_class': 'class_name',
#                              'classes': [
#                                        {'class_name': 'myclass', 'confidence': 0.999} ,
#                                         {'class_name': 'myclass2', 'confidence': 0.001}
#                                          ]
#                              },
#                              {'top_class': 'class_name',
#                              ...
#                              }
#                      ]
#              , ‘classifiername2’:
#                      [
#                      …      
#                      ]
#              …
#              }
#
# Error Handling:
#       This function should throw an exception if the classify call fails for any reason
#       or if the input csv file is of an improper format.
#
def classify_all_texts(username, password, input_csv_file_name):
	if not os.path.isfile(input_csv_file_name):
	    raise IOError("Input file " + input_csv_file_name + " does not exist")
	input_csv = open (input_csv_file_name)

	tweets = input_csv.readlines()
	classifiers_dict = dict ()
	all_classifier_results = []
	for classifier_id in current_classifier_id_list:
		print "The current classifier is " + classifier_id
		single_classifier_results = []
		for tweet_content in tweets:
			tweet_dict = dict ()
			index = tweet_content.rfind (",")
			tweet = tweet_content [:index]
			tweet = urllib.quote (tweet)
			# Error handling already exists in classify_single_text!
			tweet_json = classify_single_text (username,password,classifier_id,tweet)
			top_class = tweet_json ['top_class']
			classes = tweet_json ['classes']
			tweet_dict['top_class'] =  top_class
			tweet_dict['classes'] = classes
			single_classifier_results.append (tweet_dict)
		classifiers_dict [classifier_id] = single_classifier_results
	return classifiers_dict

def compute_accuracy_of_single_classifier(classifier_dict, input_csv_file_name):
	# Given a list of "classifications" for a given classifier, compute the accuracy of this
	# classifier according to the input csv file
	#
	# Inputs:
	# 	classifier_dict - A list of "classifications". Aka:
	#		A list of dictionaries, one for each text, in order of lines in the 
	#		input file. Each element is a dictionary containing the top_class
	#		and the confidences of all the possible classes (ie the same
	#		format as returned by classify_single_text) 	
	# 		Format example:
	#			[
	#				{'top_class': 'class_name',
	#			 	 'classes': [
	#						  	{'class_name': 'myclass', 'confidence': 0.999} ,
	#						  	{'class_name': 'myclass2', 'confidence': 0.001}
	#							]
	#				},
	#				{'top_class': 'class_name',
	#				...
	#				}
	#			]
	#
	#	input_csv_file_name - full path and name of an input csv file in the  
	#		6 column format of the input test/training files
	#
	# Returns:
	#	The accuracy of the classifier, as a fraction between [0.0-1.0] (ie percentage/100). \
	#	See the handout for more info.
	#
	# Error Handling:
	# 	This function should throw an error if there is an issue with the 
	#	inputs.
	#
	if not os.path.isfile(input_csv_file_name):
	    raise IOError("Input file " + input_csv_file_name + " does not exist")
	if classifier_dict is None:
		raise Exception ("Empty dictionary")

	input_csv = open (input_csv_file_name)
	tweets = input_csv.readlines ()
	tweets_size = len (tweets)
	match_vector = [0] * tweets_size
	curr_index = 0 

	while curr_index < tweets_size:
		tweet_content = tweets[curr_index]
		tweet_dict = classifier_dict[curr_index]
		index = tweet_content.rfind (",")
		tweet_class = int (tweet_content [index + 1:].strip('\n') )
		top_class = int (tweet_dict ['top_class'])
		if tweet_class == top_class:
			match_vector[curr_index] = 1
		else:
			match_vector[curr_index] = 0 

		curr_index += 1

	return sum (match_vector) / float(tweets_size)

# Given a list of "classifications" for a given classifier, compute the average 
# confidence of this classifier wrt the selected class, according to the input
# csv file. 
#
# Inputs:
# 	classifier_dict - A list of "classifications". Aka:
#		A list of dictionaries, one for each text, in order of lines in the 
#		input file. Each element is a dictionary containing the top_class
#		and the confidences of all the possible classes (ie the same
#		format as returned by classify_single_text) 	
# 		Format example:
#			[
#				{'top_class': 'class_name',
#			 	 'classes': [
#						  	{'class_name': 'myclass', 'confidence': 0.999} ,
#						  	{'class_name': 'myclass2', 'confidence': 0.001}
#							]
#				},
#				{'top_class': 'class_name',
#				...
#				}
#			]
#
#	input_csv_file_name - full path and name of an input csv file in the  
#		6 column format of the input test/training files
#
# Returns:
#	The average confidence of the classifier, as a number between [0.0-1.0]
#	See the handout for more info.
#
# Error Handling:
# 	This function should throw an error if there is an issue with the 
#	inputs.
#
def compute_average_confidence_of_single_classifier(classifier_dict, input_csv_file_name):
	if not os.path.isfile(input_csv_file_name):
	    raise IOError ("Input file " + input_csv_file_name + " does not exist")
	if classifier_dict is None:
		raise Exception ("Empty dictionary") 

	input_csv = open (input_csv_file_name)
	tweets = input_csv.readlines ()
	tweets_size = len (tweets)
	match_vector = [0] * tweets_size
	curr_index = 0
	correct_cons = [] 
	incorrect_cons = []
	while curr_index < tweets_size:
		tweet_content = tweets[curr_index]
		tweet_dict = classifier_dict[curr_index]
		index = tweet_content.rfind (",")
		tweet_class = tweet_content [index + 1:].strip('\n') 
		classes = tweet_dict['classes']
		top_class = tweet_dict['top_class']
		# Correct case
		if tweet_class == top_class:
			for c in classes:
				if c['class_name'] == top_class:	
					correct_cons.append (c['confidence'])
					break
		# Incorrect case
		else:
			for c in classes:
				if c['class_name'] == top_class:	
					incorrect_cons.append (c['confidence'])
					break 

		curr_index += 1

	correct_cons = np.mean (correct_cons)
	incorrect_cons = np.mean (incorrect_cons) 
	return (correct_cons, incorrect_cons)

# Computer accuracy for each classifier and its incorrect / correct confidences
def compute_accuracy_and_confidence_of_all_classifiers (classifiers_dict, input_csv_file_name): 
	accuracies = [] 
	confidences = [] 
	for classifier_key in classifiers_dict.keys():
		classifier_dict = classifiers_dict [classifier_key]
		accuracy = compute_accuracy_of_single_classifier(classifier_dict, input_csv_file_name)
		confidence = compute_average_confidence_of_single_classifier (classifier_dict, input_csv_file_name)
		print "-----------------------------------------"
		print "Current classifier is " + classifier_key
		print "The accuracy is " + str(accuracy)
		print "The average correct and incorrect confidences are"
		print confidence
		print "-----------------------------------------"
		print 
		accuracies.append (accuracy)
		confidences.append (confidence)

	avg_accuracy = sum (accuracies) / float (len(accuracies))
	return avg_accuracy, confidences

# Save picked classifier dictionaries (for recording classification results)
def save_classifier_results (classifier_results, results_file):
	fpickle = open (results_file, "w")
	pickle.dump (classifier_results, fpickle)

# Load picked classifier dictionaries 
def load_classifier_results (results_file):
	content = pickle.load (open (results_file, "r"))
	return content
	
if __name__ == "__main__":
	username = None # Enter bluemix username
	password =  None # Enter bluemix password
	fpickle_name = "results.pkl"
	input_csv_file_name = "test_data.csv"
	
	#STEP 1: Ensure all 11 classifiers are ready for testing
	current_classifier_id_list = get_classifier_ids(username, password)

	#STEP 2: Test the test data on all classifiers
	assert_all_classifiers_are_available(username, password, current_classifier_id_list)

	#STEP 3: Compute the accuracy for each classifier
	all_classifier_results = classify_all_texts(username, password,input_csv_file_name)

	# Save and then load the pickled data
	save_classifier_results (all_classifier_results, fpickle_name)
	classifiers_dict = load_classifier_results (fpickle_name)

	#STEP 4: Compute the accuracy and confidence of each class for each classifier
	average_accuracies, confidences = compute_accuracy_and_confidence_of_all_classifiers (classifiers_dict, input_csv_file_name)
	print "-----------------------------------------"
	print "Average accuracies over all classifiers"
	print average_accuracies
	print "All correct and incorrect confidences"
	print confidences
	print "-----------------------------------------"
	

	
	