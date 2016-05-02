
import os

separator = '*' * 50

if __name__ == "__main__":
	for i in range(10):
		res_file = 'cross_valid_dtree'
		os.system("echo '" + separator + "' >> " + res_file)
		os.system ("java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 -t comb" + str(i) + \
			".arff -T valid" + str(i) + ".arff | tail -n 40 >> " + res_file)

		# res_file = 'cross_valid_SMO'
		# os.system("echo '" + separator + "' >> " + res_file)
		# os.system ("java -cp /u/cs401/WEKA/weka.jar weka.classifiers.functions.SMO -t comb" + str(i) + \
		# 	".arff -T valid" + str(i) + ".arff | tail -n 40 >> " + res_file)

		# res_file = 'cross_valid_bayes'
		# os.system("echo '" + separator + "' >> " + res_file)
		# os.system ("java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t comb" + str(i) + \
		# 	".arff -T valid" + str(i) + ".arff | tail -n 40 >> " + res_file)