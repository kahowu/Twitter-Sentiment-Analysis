import os

# os.system("python twtt.py /u/cs401/A1/tweets/training.1600000.processed.noemoticon.csv 19 train.twt")
#execfile ("twtt.py /u/cs401/A1/tweets/testdata.manualSUBSET.2009.06.14.csv -1 test.twt")
#execfile ("buildarff.py train.twt train.arff")
#execfile ("buildarff.py test.twt test.arff") 
#execfile ("print_stuff.py") 
#os.system ("print_stuff.py")
#os.system ("twtt.py")

if __name__ == '__main__':
	data_size = 500 
	while data_size <= 5500: 
		train_data_name = "train" + str(data_size) + ".arff"
		exec_string = "python buildarff.py train.twt " + train_data_name + " " + str(data_size)
		data_size += 500 
		# os.system (exec_string)
		java_exec_string = "java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 -t " + train_data_name + " -T test.arff"
		# os.system (java_exec_string)
		info_exec_string = "sh /u/cs401/WEKA/infogain.sh " + train_data_name 
		os.system (info_exec_string)

	# 	os.system("python buildarff.py train.twt train.arff")
	# 	# python buildarff.py train.twt all.arff 

	# 	# exec_string = "python twtt.py /u/cs401/A1/tweets/training.1600000.processed.noemoticon.csv 19 train.twt"
	# 	os.system("python twtt.py /u/cs401/A1/tweets/training.1600000.processed.noemoticon.csv 19 train.twt")
	# os.system("python twtt.py /u/cs401/A1/tweets/testdata.manualSUBSET.2009.06.14.csv -1 test.twt")
	# os.system("python buildarff.py test.twt test.arff")
	

