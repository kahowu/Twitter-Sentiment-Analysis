

import re
from scipy import stats
import numpy as np


def accuracy (confusion_matrix):
	diag = np.diag (confusion_matrix)
	total = np.sum (confusion_matrix)
	return np.sum (diag) / float (total)

def precision (confusion_matrix):
	diag = np.diag (confusion_matrix)
	pres = [] 
	for col in range (confusion_matrix.shape[1]):
		current_value = diag [col]
		c = confusion_matrix[:, col]
		pres.append (current_value / float (np.sum(c)))
	return np.mean(pres)

def recall (confusion_matrix):
	diag = np.diag (confusion_matrix)
	recs = []
	for row in range (confusion_matrix.shape[0]):
		current_value = diag [row]
		r = confusion_matrix[row, :]
		recs.append (current_value / float (np.sum(r)))
	return np.mean(recs)


if __name__ == "__main__":
	file_names = ['cross_valid_SMO', 'cross_valid_bayes', 'cross_valid_dtree']
	acc_results = []
	matrices_results = []
	for name in file_names:
		acc_accept = False
		pipe_count = 0
		result = []
		matrices = []
		t = []
		count = 0
		f = open (name, 'r')
		for line in f:
			if line.startswith("Correctly Classified"):
				if acc_accept:
					result.append(float(re.search(r'\d+\.\d+', line).group()))
				acc_accept ^= True
			if '|' in line:
				if count % 4 == 2 or count % 4 == 3:
					line = line[:line.index('|')].strip().split()
					if count % 4 == 2:
						t = [int(x) for x in line]
					else:
						matrices.append(np.matrix([t, [int(x) for x in line]]))
				count += 1

		f.close()
		acc_results.append([result, name])
		matrices_results.append([matrices, name])
	
	for matrices, name in matrices_results:
		print name
		# cumul_acc = 0
		# cumul_prec = 0
		# cumul_rec = 0
		for matrix in matrices:
			print '\t', accuracy(matrix), precision(matrix), recall(matrix)
		# for matrix in matrices:
			# cumul_acc += accuracy(matrix)
			# cumul_prec += precision(matrix)
			# cumul_rec += recall(matrix)
		# print '\tAccuracy:',  float(cumul_acc) / len(matrices)
		# print '\tPrecision:', float(cumul_prec) / len(matrices)
		# print '\tRecall:', + float(cumul_rec) / len(matrices)
	

	print
	for i in range(len(acc_results)):
		for j in range(i + 1, len(acc_results)):
			# print acc_results[i][0]
			S = stats.ttest_rel(acc_results[i][0], acc_results[j][0])
			print acc_results[i][1], acc_results[j][1], S


