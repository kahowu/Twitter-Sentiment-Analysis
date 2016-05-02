#!/bin/sh
# python twtt.py /u/cs401/A1/tweets/training.1600000.processed.noemoticon.csv 19 train.twt
# python twtt.py /u/cs401/A1/tweets/testdata.manualSUBSET.2009.06.14.csv test.twt
# python buildarff.py train.twt all.arff 
# python buildarff.py test.twt test.arff
# java -cp /u/cs401/WEKA/weka.jar weka.classifiers.functions.SMO -t train.arff -T test.arff
# java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t train.arff -T test.arff
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 -t all.arff -T test.arff > 3.1output.txt

