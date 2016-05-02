# ibmTrain.py
# 
# This file produces 11 classifiers using the NLClassifier IBM Service
# 

###IMPORTS###################################
import sys
import re
import os
import commands
import subprocess
import json
import os.path

# Converts an existing training csv file. The output file should
# contain only the 11,000 lines of your group's specific training set.
#
# Inputs:
#	input_csv - a string containing the name of the original csv file
#		ex. "my_file.csv"
#
#	output_csv - a string containing the name of the output csv file
#		ex. "my_output_file.csv"
#
# Returns:
#	None
def convert_training_csv_to_watson_csv_format(input_csv_name, group_id, output_csv_name): 
	input_csv = open (input_csv_name)
	output_csv = open (output_csv_name, "w")
	lines = input_csv.readlines()
	class_4_start = 800000
	class_0_lower = group_id * 5500
	class_0_upper = (group_id + 1) * 5500
	class_4_lower = class_4_start + group_id * 5500
	class_4_upper = class_4_start + (group_id + 1) * 5500
	class_0 = lines[class_0_lower: class_0_upper]
	class_4 = lines[class_4_lower: class_4_upper]
	process_class (class_0, output_csv)
	process_class (class_4, output_csv)
	
	return

# Extracts n_lines_to_extract lines from a given csv file and writes them to 
# an outputfile named ibmTrain#.csv (where # is n_lines_to_extract).
#
# Inputs: 
#	input_csv - a string containing the name of the original csv file from which
#		a subset of lines will be extracted
#		ex. "my_file.csv"
#	
#	n_lines_to_extract - the number of lines to extract from the csv_file, as an integer
#		ex. 500
#
#	output_file_prefix - a prefix for the output csv file. If unspecified, output files 
#		are named 'ibmTrain#.csv', where # is the input parameter n_lines_to_extract.
#		The csv must be in the "watson" 2-column format.
#		
# Returns:
#	None
def extract_subset_from_csv_file(input_csv_file, n_lines_to_extract, output_file_prefix='ibmTrain'):
	input_csv_file.seek(0, 0)
	lines = input_csv_file.readlines()
	class_0 = lines[0:5500]
	class_4 = lines[5501:] 
	subset_0 = class_0 [0 : n_lines_to_extract]
	subset_4 = class_4 [0: n_lines_to_extract]
	new_filename = output_file_prefix + str(n_lines_to_extract)
	new_subset_file = open (new_filename + '.csv', "w")
	write_to_file (subset_0, new_subset_file)
	write_to_file (subset_4, new_subset_file)

	return

# Creates a classifier using the NLClassifier service specified with username and password.
# Training_data for the classifier provided using an existing csv file named
# ibmTrain#.csv, where # is the input parameter n.
#
# Inputs:
# 	username - username for the NLClassifier to be used, as a string
#
# 	password - password for the NLClassifier to be used, as a string
#
#	n - identification number for the input_file, as an integer
#		ex. 500
#
#	input_file_prefix - a prefix for the input csv file, as a string.
#		If unspecified data will be collected from an existing csv file 
#		named 'ibmTrain#.csv', where # is the input parameter n.
#		The csv must be in the "watson" 2-column format.
#
# Returns:
# 	A dictionary containing the response code of the classifier call, will all the fields 
#	specified at
#	http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/natural-language-classifier/api/v1/?curl#create_classifier
#   
#
# Error Handling:
#	This function should throw an exception if the create classifier call fails for any reason
#	or if the input csv file does not exist or cannot be read.
#
def create_classifier(username, password, n, input_file_prefix='ibmTrain'):
	filename = input_file_prefix + str(n) + '.csv'
	if not os.path.isfile(filename):
	    raise IOError("Input file " + filename + " does not exist")
	
	#TODO: Fil in this function
	cmd = r'curl -u "' + username + r'":"' + password + r'" -F training_data=@' + filename + r' -F training_metadata="{\"language\":\"en\",\"name\":\"Classifier ' + str(n) + r'\"}" "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers" 2>/dev/null'
	output = json.loads(subprocess.check_output(cmd, shell=True))
	if 'error' in output:
		raise Exception(output['error'] + " - " + output['description'])	
	return output

# Create test set from input csv file
def create_test_set (input_csv_name, output_csv_name):
	input_csv = open (input_csv_name)
	output_csv = open (output_csv_name, "w")
	lines = input_csv.readlines()
	process_class (lines, output_csv)

# Write tweets to a file
def write_to_file (tweets, input_file):
	for tweet in tweets:
		input_file.write (tweet) 

# Process tweets into bluemix format
def process_class (tweet_list, output_csv):
	for item in tweet_list:
		tweet_content = item.split("\",\"")
		tweet_class = tweet_content[0][1:]
		current_tweet =  (tweet_content[5])[:-2]
		current_tweet = current_tweet.replace ('"', '""')
		current_tweet = re.sub("\s\s+", "\\\\t", current_tweet)
		if "," in current_tweet:
			current_tweet = '"' + current_tweet + '"'
		processed_tweet = current_tweet + "," + tweet_class + "\n"
		output_csv.write (processed_tweet)
	
if __name__ == "__main__":
	input_csv_name = 'training.1600000.processed.noemoticon.csv'
	data = None # Put in the directory of the data
	test_csv_name = 'testdata.manualSUBSET.2009.06.14.csv'
	output_csv_name = 'training_11000_watson_style.csv'
	# STEP 1: Convert csv file into two-field watson format
	test_output_csv_name = 'test_data.csv'
	input_csv_path = data + input_csv_name
	test_csv_path = data + test_csv_name
	group_id = 19

	convert_training_csv_to_watson_csv_format (input_csv_path, group_id, output_csv_name)
	create_test_set (test_csv_path, test_output_csv_name)

	input_watson_csv = open (output_csv_name)
	num_samples = [500, 2500, 5000]
	
	# STEP 2: Save 3 subsets in the new format into ibmTrain#.csv files and create classifiers
	username = None # Bluemix username
	password = None # Bluemix password

	for num in num_samples:
		extract_subset_from_csv_file(input_watson_csv, num)
		create_classifier(username, password, num)
