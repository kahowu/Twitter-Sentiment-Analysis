import csv 
from A1data import *

def convert_training_csv_to_watson_csv_format(input_csv_name, group_id, output_csv_name): 
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
	
	#TODO: Fill in this function
	input_csv = open (input_csv_name)
	output_csv = open (output_csv_name)
	lines = input_csv.readlines()
	class_4_start = 800000
	class_0_lower = group_ID * 5500
	class_0_upper = (group_ID + 1) * 5500
	class_4_lower = class_4_start + group_ID * 5500
	class_4_upper = class_4_start + (group_ID + 1) * 5500
	class_0 = lines[class_0_lower: class_0_upper]
	class_4 = lines[class_4_lower: class_4_upper]


	
	return


if __name__ == '__main__':
	input_csv = sys.argv[1]
    group_ID = int(sys.argv[2])
    output_csv = sys.argv[3]


    convert_training_csv_to_watson_csv_format (input_csv, group_ID, output_csv)
    

